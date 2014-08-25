# -*- coding: utf-8 -*-
#    Asymmetric Base Framework :: Enum
#    Copyright (C) 2013  Asymmetric Ventures Inc.
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; version 2 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import absolute_import, division, print_function, unicode_literals

from django import forms
from django.core import exceptions
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import NOT_PROVIDED
from django.db.models.fields.subclassing import SubfieldBase

import six

from asymm_enum.enum import Enum, EnumItem

def _enum_coerce(self, enum, value):
	if value is None or value == '':
		return None
	
	elif isinstance(value, EnumItem) and value in enum:
		return value
	
	try:
		return enum(int(value))
	except ValueError:
		raise exceptions.ValidationError(
			self.error_messages['invalid_choice'],
			code = 'invalid_choice',
			params = {'value' : value}
		)

class EnumFormField(forms.TypedChoiceField):
	
	def __init__(self, enum, *args, **kwargs):
		self.enum = enum
		if 'choices' not in kwargs:
			kwargs['choices'] = enum.Choices.items()
		super(EnumFormField, self).__init__(*args, **kwargs)
	
	def prepare_value(self, data):
		if isinstance(data, EnumItem):
			return str(data.value)
		
		return data
	
	def valid_value(self, value):
		for k, _ in self._get_flat_choices():
			if not k and not value:
				return True
			
			if isinstance(value, EnumItem):
				if value.value == k:
					return True
		return False
	
	def to_python(self, value):
		return _enum_coerce(self, self.enum, value)
	
	def _get_flat_choices(self):
		for k, v in self.choices:
			if isinstance(v, (list, tuple)):
				for k2, v2 in v:
					yield k2, v2
			else:
				yield k, v
	
	def _has_changed(self, initial, data):
		initial_value = initial if initial is not None else ''
		try:
			data = self.to_python(data)
		except ValidationError:
			return True
		data_value = str(data.value) if data is not None else ''
		
		return initial_value != data_value
		
class EnumField(six.with_metaclass(SubfieldBase, models.IntegerField)):
	
	empty_strings_allowed = False
	validators = []
	
	def __init__(self, enum, *args, **kwargs):
		self.enum = enum
		kwargs.update(
			choices = enum.Choices.items(),
			null = False,
			blank = False
		)
		
		super(EnumField, self).__init__(*args, **kwargs)
	
	def __copy__(self, *args, **kwargs):
		return self
	
	def __deepcopy__(self, *args, **kwargs):
		return self
	
	def get_default(self):
		"""
		Returns the default value for this field.
		
		The default implementation on models.Field calls force_unicode
		on the default, which means you can't set arbitrary Python
		objects as the default. To fix this, we just return the value
		without calling force_unicode on it. Note that if you set a
		callable as a default, the field will still call it.
		
		Modified from: http://djangosnippets.org/snippets/1694/
		
		"""
		if self.has_default():
			default = self.default
			if callable(default):
				default = self.default()
			if default is None:
				return None
			if isinstance(default, six.integer_types):
				return default
			if isinstance(default, six.string_types):
				return default
			return str(default.value)
		# If the field doesn't have a default, then we punt to models.Field.
		return super(EnumField, self).get_default()
	
	def to_python(self, value):
		return _enum_coerce(self, self.enum, value)
	
	def validate(self, value, model_instance):
		return value in self.enum
	
	def get_prep_value(self, value):
		if value in (None, ''):
			return None
		
		return int(value)
	
	def formfield(self, **kwargs):
		include_blank = (self.blank or not (self.has_default() or 'initial' in kwargs))
		defaults = {
			'enum' : self.enum,
			'required' : not self.blank,
			'label' : self.verbose_name,
			'help_text' : self.help_text,
			'choices': self.get_choices(include_blank = include_blank),
			'coerce': self.to_python,
			'empty_value' : None,
		}
		if self.has_default():
			if callable(self.default):
				defaults['initial'] = self.default
				defaults['show_hidden_initial'] = True
				
			else:
				defaults['initial'] = self.get_default()
		
		for k in kwargs.keys():
			if k not in ('coerce', 'empty_value', 'choices', 'required',
						'widget', 'label', 'initial', 'help_text',
						'error_messages', 'show_hidden_initial'):
				del kwargs[k]
		
		defaults.update(**kwargs)
		
		return EnumFormField(**defaults)
	
	def deconstruct(self):
		name, path, args, kwargs = super(EnumField, self).deconstruct()
		kwargs['enum'] = self.enum
		kwargs['default'] = self.get_default()
		
		return name, path, args, kwargs

try:
	from south.modelsinspector import add_introspection_rules
	
	def enum_converter(value):
		if issubclass(value, Enum):
			return 'Migration().gf("{0}.{1}")'.format(value.__module__, value.__name__)
		
		raise ValueError("Unknown value type `{0!r}` for enum argument".format(value))
	
	def default_converter(value):
		if isinstance(value, NOT_PROVIDED) or value is NOT_PROVIDED:
			return None
		
		elif isinstance(value, EnumItem):
			return repr(value.value)
		
		raise ValueError(repr(value))

	
	add_introspection_rules(
		[
			(
				[EnumField], # Field Name
				[], # Args
				{ # kwargs
					'enum' : ['enum', {'converter' : enum_converter, 'is_django_function' : True}],
					'default' : ['default', {'converter' : default_converter, 'is_django_function' : True}],
				}
			)
		],
		['^asymm_enum\.fields\.enumfield\.EnumField']
	)
except ImportError:
	pass
