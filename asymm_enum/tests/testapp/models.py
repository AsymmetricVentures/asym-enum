from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import models

from asymm_enum.enum import Enum
from asymm_enum.fields.enumfield import EnumField

__author__ = "Richard Eames <reames@asymmetricventures.com>"
__date__ = "May 20, 2014"
__updated__ = "May 20, 2014"
__rev__ = "$Id$"

class TestEnum(Enum):
	VALUE1 = 1
	VALUE2 = 2

class TestEnumModel(models.Model):
	field1 = EnumField(TestEnum)

class TestEnumModel1(models.Model):
	field1 = EnumField(TestEnum)
	field2 = EnumField(TestEnum)
	field3 = EnumField(TestEnum)

class TestEnumModelWithDefault(models.Model):
	field1 = EnumField(TestEnum, default = TestEnum.VALUE1)
