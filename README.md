#asym-enum
==========

An Enum implementation similar to flufl.enum and Python 3.4 enum, except behaves more like a Java enum

[![Build Status](https://travis-ci.org/AsymmetricVentures/asym-enum.svg?branch=master)](https://travis-ci.org/AsymmetricVentures/asym-enum)

Supports:

* python 2.6, 2.7, 3.3, 3.4

* django 1.4, 1.5, 1.6, 1.7

## Examples

### Basic example
```python

from asymm_enum.enum import Enum

class MyEnum(Enum):
	A = 1
	B = 2

class MyEnum2(Enum):
	A = 1
	B = 2

assert MyEnum.A == MyEnum.A, "Enum members are can only be compared to themselves"
assert MyEnum.A != 1, "Cannot compare enums to ints"
assert MyEnum.A is MyEnum.A, "Enum members are singletons"
assert MyEnum.A != MyEnum2.A, "Enums cannot compare to other enums, even of the same ordinal"
assert MyEnum.A in MyEnum, "Enum members are part of the Enum"

```

### Casting and labels
```python

class MyEnum(Enum):
	A = 1
	B = 3, 'Hello'
	UPPER_CASE_WORD = 4

assert repr(MyEnum.A) == 'MyEnum.A'
assert str(MyEnum.A) == 'A', "Labels are automatically created from the left-hand-side"
assert str(MyEnum.B) == 'Hello', "Usually the second parameter is the label"
assert str(MyEnum.UPPER_CASE_WORD), "Labels are title cased if not explicitly given"

assert int(MyEnum.A) == 1, "Casting to int returns the ordinal value"
assert MyEnum(1) == MyEnum.A, "Members can be retrieved via the constructor given its ordinal"
```

**Note**, left hand side of the members must be in UPPER_CASE.

### Methods and functions
```python
class E(Enum):
	A = 1
	B = 2
	
	def get_label(self):
		''' instance methods are attached to individual members '''
		return self.label
	
	@classmethod
	def get_b_label(cls):
		''' class methods are attached to the enum '''
		return cls.B.label

assert E.A.get_label() == 'A'
try:
	E.A.get_b_label()
	assert False, "Should not get here because `get_b_label` does not exist on member"
except AttributeError:
	pass

assert E.get_b_label() == 'B'
try:
	E.get_label()
	assert False, "Should not get here because the enum does not have the instance function"
except AttributeError:
	pass

```

### Custom properties and Display Order
```python
class E(Enum):
	class Meta:
		'''
			Properties are defined with a "Meta" class, similarly to Django.
			If defining this list, ensure that `value` appears in the list exactly once.
			If `label` appears in the list, it will be used as the stringified label
			of the member.
		'''
		properties = ('value', 'display_order', 'attr1', 'label')
	
	A = 1, 2, "Attr1 for E.A", "This is A"
	B = 2, 3, "Attr1 for E.B", "This is B"
	C = 3, 1, "Attr1 for E.C", "This is C"

# Display order is used when the enum is iterated over, or coerced to a list/tuple.
# If not display order is given, the member's ordinal `value` is used.

assert list(E) == (E.C, E.A, E.B)

# Properties are available on the Enum members as attributes
assert E.A.display_order == 2
assert E.B.attr1 == "Attr1 for E.B"
assert E.A.label == "This is A"
assert E.A.label == str(E.A)
```

### Hashable and Pickle-able
```python
import pickle

class E(Enum):
	A = 1
	B = 2

assert hash(E.A), "Is hashable"
d = { E.A : 'a' }
assert d[E.A] == 'a', "Can be used as dictionary/set keys

d = pickle.dumps(E.A, pickle.HIGHEST_PROTOCOL)
r = pickle.loads(d)

assert r == E.A, "Members can be pickled"
```

### Django Model and Form Fields
```python
from django import forms
from django.db import models

from asymm_enum.enum import Enum
from asymm_enum.fields.enumfield import EnumField

class E(Enum):
	A = 1
	B = 2

class MyModel(models.Model)
	field1 = EnumField(E)
	field2 = EnumField(E, default=E.B)

class MyForm(forms.Form):
	field1 = EnumField(E).formfield(required=False)
	field2 = EnumField(E, default=E.B).formfield()

class MyModelForm(forms.ModelForm):
	class Meta:
		model = MyModel
		fields = ('field1',)

```

## Differences from Python 3.4 Enum

* Custom attributes are automatically created and do not need and `__init__`
* The special attribute `display_order` is used for the listing order
* Members are unique by default
* The ordinal value is required, and is required to be an int
* The special attribute `label` is used for stringification of a member
* The left hand side of the member definition must be UPPER_CASE
* Currently, the member is not an instance of the enum, but of an internal class `EnumItem`
* No functional interface.

## TODO:

* More complete test coverage
* Testing for Django 1.7
* Close the API gap with Python 3.4 Enums

