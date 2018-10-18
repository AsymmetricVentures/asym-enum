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

from django.test.client import RequestFactory
from django.test.testcases import TestCase
try:
	from django.utils import unittest
except ImportError:
	import unittest

from .testapp.forms import TestModelForm, TestModelWithDefaultForm, TestFormSet
from .testapp.models import TestEnum, TestEnumModel

class FormTest(TestCase):
	
	def setUp(self):
		self.factory = RequestFactory()
	
	def test_validation1(self):
		''''''
		request = self.factory.post('/', {'field1' : '1'})
		
		form = TestModelForm(request.POST)
		self.assertTrue(form.is_valid())
		
		models = form.save()
		self.assertEqual(models.field1, TestEnum.VALUE1)
	
	def test_validation2(self):
		''' Test validation against invalid value'''
		request = self.factory.post('/', {'field1' : '8'})
		form = TestModelForm(request.POST)
		
		self.assertFalse(form.is_valid())
	
	def test_widget_selected(self):
		model = TestEnumModel()
		model.field1 = TestEnum.VALUE2
		
		form = TestModelForm(instance = model)
		
		substring_html = '<option value="{0}" selected="selected">{1}</option>'.format(
			int(TestEnum.VALUE2), str(TestEnum.VALUE2)
		)
		self.assertInHTML(substring_html, str(form))
	
	def test_widget_with_initial(self):
		form = TestModelWithDefaultForm()
		
		substring_html = '<option value="{0}" selected="selected">{1}</option>'.format(
			int(TestEnum.VALUE1), str(TestEnum.VALUE1)
		)
		
		self.assertInHTML(substring_html, str(form))
	
	def test_with_formset1(self):
		request = self.factory.post('/', {
			'form-TOTAL_FORMS' : '1',
			'form-INITIAL_FORMS' : '0',
			'form-MAX_NUM_FORMS' : '0',
			'form-0-field1' : '',
			'form-0-field2' : '2',
		})
		
		formset = TestFormSet(request.POST)
		
		self.assertFalse(formset[0].has_changed())
		self.assertFalse(formset.has_changed())
		self.assertTrue(formset.is_valid())
		

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
