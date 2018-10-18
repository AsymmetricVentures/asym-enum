# -*- coding: utf-8 -*-
#    Asymmetric Base Framework :: Enum
#    Copyright (C) 2013-2014  Asymmetric Ventures Inc.
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
import sys

from django.conf import settings

try:
	import django #@UnusedImport
except ImportError:
	print("Error: django is required to run tests")
	sys.exit(1)

try:
	import six #@UnusedImport
except ImportError:
	print("Error: six is required to run tests")
	sys.exit(-1)

djv = django.get_version()

def main():
	settings.configure(
		INSTALLED_APPS = (
			'django.contrib.auth',
			'django.contrib.contenttypes',
			'django.contrib.admin',
			'django.contrib.sessions',
			'asymm_enum',
			'asymm_enum.tests.testapp',
		),
		DATABASE_ENGINE = 'django.db.backends.sqlite3',
		DATABASES = {
			'default': {
				'ENGINE': 'django.db.backends.sqlite3',
				'NAME': ':memory:',
			}
		},
		DEBUG = True,
		TEMPLATE_DEBUG = True,
		MIDDLEWARE_CLASSES = (
			'django.contrib.sessions.middleware.SessionMiddleware',
			'django.contrib.messages.middleware.MessageMiddleware',
		),
		ROOT_URLCONF = 'asymm_enum.tests.testapp.urls',
		TEST_RUNNER = 'asymm_enum.tests.test_runner.TestRunner'
	)
	apps = ['asymm_enum']
	
	django.setup() #@UndefinedVariable

	apps.append('asymm_enum.tests.testapp')
	apps.append('asymm_enum.tests')
	
	from django.core.management import call_command
	call_command('test', 'asymm_enum.tests', 'asymm_enum.tests.testapp', 'asymm_enum')

if __name__ == '__main__':
	main()
