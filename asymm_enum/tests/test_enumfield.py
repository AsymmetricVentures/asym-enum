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

import unittest

import django
from django.conf import settings
from django.core.management import call_command
from django.core import exceptions
from django.db import models
#from django.db.models import loading
from django.test import TestCase


import asymm_enum #@UnusedImport #This is just so that it's in `globals()`
import six

from ..fields.enumfield import EnumField
from .testapp.models import TestEnumModel, TestEnum, TestEnumModelWithDefault
from asymm_enum.tests.testapp.models import ConcreteModel1

if django.get_version() >= '1.7':
	from django.db import migrations  # NOQA @UnresolvedImport
	from django.db.migrations.writer import MigrationWriter  # NOQA @UnresolvedImport

class TestEnumField(TestCase):

	def setUp(self):
		#loading.cache.loaded = False
		TestEnumModel.objects.all().delete()
		TestEnumModel.objects.bulk_create((
			TestEnumModel(field1 = TestEnum.VALUE1),
			TestEnumModel(field1 = TestEnum.VALUE1),
			TestEnumModel(field1 = TestEnum.VALUE1),
			TestEnumModel(field1 = TestEnum.VALUE2),
			TestEnumModel(field1 = TestEnum.VALUE2),
		))
		
		ConcreteModel1.objects.all().delete()
		ConcreteModel1.objects.bulk_create([
			ConcreteModel1(field1 = TestEnum.VALUE1, field2 = 'a'),
			ConcreteModel1(field1 = TestEnum.VALUE1, field2 = 'a'),
			ConcreteModel1(field1 = TestEnum.VALUE1, field2 = 'b'),
			ConcreteModel1(field1 = TestEnum.VALUE2, field2 = 'a'),
			ConcreteModel1(field1 = TestEnum.VALUE2, field2 = 'b'),
		])
		
	def test_querying_by_enum_value(self):
		''' Querying by Enum value '''
		self.assertEqual(TestEnumModel.objects.filter(field1 = TestEnum.VALUE1).count(), 3)
		self.assertEqual(TestEnumModel.objects.filter(field1 = TestEnum.VALUE2).count(), 2)
		self.assertEqual(TestEnumModel.objects.filter(field1 = TestEnum.VALUE3).count(), 0)
	
	def test_querying_by_string(self):
		''' - Test querying by string value
		    - Test that model fields gets converted to enum
		'''
		model1 = TestEnumModel.objects.filter(field1 = '1')
		
		self.assertEqual(model1[0].field1, TestEnum.VALUE1)
		self.assertNotEqual(model1[0].field1, '1')
		self.assertNotEqual(model1[0].field1, 1)
		
		
	def test_save_get_default(self):
		model = TestEnumModelWithDefault()
		model.save()
		
		self.assertEqual(model.field1, TestEnum.VALUE1)
		
	
	@unittest.skipIf(django.get_version() < '1.7', "Migrations only in django > 1.7")
	def test_migration(self):
		fields = {
			'field1':EnumField(TestEnum)
		}
		migration = type(str("Migration"), (migrations.Migration,), {
			'operations' : [
				migrations.CreateModel("Model1", tuple(fields.items()), {}, (models.Model,))
			]
		})
		writer = MigrationWriter(migration)
		output = writer.as_string()
		self.assertIsInstance(output, six.string_types)
		r = {}
		try:
			exec(output, globals(), r)
		except Exception as e:
			self.fail("Could not exec {!r}: {}".format(output.strip(), e))
		self.assertIn("Migration", r)
	
	@unittest.skipIf(django.get_version() < '1.7', "Migrations only in django > 1.7")
	def test_migration_with_default_value(self):
		'''
		Need to make sure that default values get serialized.
		'''
		
		MigrationWriter.serialize(EnumField(enum = TestEnum, default = TestEnum.VALUE1))
	
	def test_modelfield_validate(self):
		obj = TestEnumModel()
		field = TestEnumModel._meta.get_field('field1')
		
		field.validate(TestEnum.VALUE1, obj)
		with self.assertRaises(exceptions.ValidationError):
			# int(0) doesn't exist in the enum
			field.validate(0, obj)
		with self.assertRaises(exceptions.ValidationError):
			# Should not be able to validate non EnumValues
			field.validate(1, obj)
	
	def test_querying_with_abstract_field(self):
		'''
		This tests a bug that arose in django 1.8 if there are two models inheriting from an abstract model
		which has a enum field.
		The problem stems from the way django handles abstract models. If two models inherit the field, then the
		related model of the field is set to the concrete model. Unfortunately, due to the way EnumField implemented
		the `__deepcopy__` method, there was only ever one instance of that enum field across all models that inherit
		from the abstract class and its related model was set to whichever the last model defined is. The result of this
		is that when querying on models defined earlier, django will throw an exception because it thinks the query is 
		for a field from another model, so it treats it as a proxy model, which it is not.
		
		End of traceback:
			for int_model in opts.get_base_chain(model):
			TypeError: 'NoneType' object is not iterable

		'''
		objs = [obj for obj in ConcreteModel1.objects.filter(field1 = TestEnum.VALUE1)]
		self.assertEqual(len(objs), 3)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
