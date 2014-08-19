# -*- coding: utf-8 -*-
#    Asymmetric Base Framework - A collection of utilities for django frameworks
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
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory

from asymm_enum.fields.enumfield import EnumField

from .models import TestEnum, TestEnumModel, TestEnumModel1, TestEnumModelWithDefault

__author__ = "Richard Eames <reames@asymmetricventures.com>"
__date__ = "May 20, 2014"
__updated__ = "May 20, 2014"
__rev__ = "$Id$"

class TestForm(forms.Form):
	field1 = EnumField(TestEnum).formfield(required = False)
	field2 = EnumField(TestEnum, default = TestEnum.VALUE2).formfield()

class TestModelForm(forms.ModelForm):
	class Meta(object):
		model = TestEnumModel
		fields = ('field1',)

class TestModelWithDefaultForm(forms.ModelForm):
	class Meta(object):
		model = TestEnumModelWithDefault
		fields = ('field1',)

TestModelFormSet = modelformset_factory(TestEnumModel1, fields=('field1', 'field2', 'field2'))
TestFormSet = formset_factory(TestForm)
