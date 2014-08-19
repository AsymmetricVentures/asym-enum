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

import django
from django.conf import settings
from django.core.management import call_command
from django.db import models
from django.db.models import loading
from django.utils import unittest

import asymm_enum #@UnusedImport #This is just so that it's in `globals()`
import six

from ..fields.enumfield import EnumField
from .testapp.models import TestEnumModel, TestEnum, TestEnumModelWithDefault

if django.get_version() >= '1.7':
	from django.db import migrations  # NOQA @UnresolvedImport
	from django.db.migrations.writer import MigrationWriter  # NOQA @UnresolvedImport

class TestEnumField(unittest.TestCase):

	def setUp(self):
		loading.cache.loaded = False
		migrate = 'south' not in settings.INSTALLED_APPS
		call_command('syncdb', verbosity = 0, migrate = migrate)
		
		TestEnumModel.objects.all().delete()
		TestEnumModel.objects.bulk_create((
			TestEnumModel(field1 = TestEnum.VALUE1),
			TestEnumModel(field1 = TestEnum.VALUE1),
			TestEnumModel(field1 = TestEnum.VALUE1),
			TestEnumModel(field1 = TestEnum.VALUE2),
			TestEnumModel(field1 = TestEnum.VALUE2),
		))
		
	def test_querying1(self):
		''' Querying by Enum value '''
		self.assertEqual(TestEnumModel.objects.filter(field1 = TestEnum.VALUE1).count(), 3)
		self.assertEqual(TestEnumModel.objects.filter(field1 = TestEnum.VALUE2).count(), 2)
	
	def test_querying2(self):
		''' - Test querying by string value
		    - Test that model fields gets converted to enum
		'''
		model1 = TestEnumModel.objects.filter(field1 = '1')
		
		self.assertEqual(model1[0].field1, TestEnum.VALUE1)
		self.assertNotEqual(model1[0].field1, 1)
		
		
	def test_get_default(self):
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
				migrations.CreateModel("Model1", tuple(fields.items()), {}, (models.Model))
			]
		})
		writer = MigrationWriter(migration)
		output = writer.as_string()
		self.assertIsInstance(output, six.binary_type)
		r = {}
		try:
			exec(output, globals(), r)
		except Exception as e:
			self.fail("Could not exec {!r}: {}".format(output.strip(), e))
		self.assertIn("Migration", r)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
