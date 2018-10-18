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

try:
	from django.utils import unittest
except ImportError:
	import unittest

from asymm_enum.enum import Enum

try:
	class EnumP(Enum):
		A = 1
		B = 2
except Exception as e:
	raise Exception("Could not create an enum")

class EnumTest(unittest.TestCase):
	def test_basic_enum(self):
		class Enum1(Enum):
			A = 1
			B = 2
		
		self.assertEqual(int(Enum1.A), 1)
		self.assertEqual(str(Enum1.A), 'A')
		self.assertEqual(int(Enum1.B), 2)
		self.assertEqual(str(Enum1.B), 'B')
		
		self.assertNotEqual(Enum1.A, Enum1.B)
		
		self.assertIs(Enum1.A, Enum1.A)
		
		self.assertEqual(Enum1.A._enum_type_, Enum1)
		
		self.assertEqual(Enum1(1), Enum1.A)
		self.assertIs(Enum1(1), Enum1.A)
		
		with self.assertRaises(ValueError):
			_ = Enum1(3) 
		
		with self.assertRaises(TypeError):
			# Enum ordinals must be integers
			class Enum5(Enum):
				A = 'a'
				B = 'b'
		
	def test_two_enums(self):
		class Enum1(Enum):
			A = 1
			B = 2
		
		class Enum2(Enum):
			A = 1
			B = 2
		
		self.assertNotEqual(Enum1.A, Enum2.A)
		self.assertEqual(Enum1.A, Enum1.A)
		self.assertNotEqual(Enum1.B, Enum2.B)
	
	def test_methods(self):
		class E(Enum):
			A = 1
			B = 2
		
			def mylabel(self):
				return self.label
			
			@classmethod
			def getBLabel(cls):
				return cls.B.label
		
		self.assertEqual(E.A.mylabel(), 'A')
		self.assertEqual(E.getBLabel(), 'B')
		
		self.assertRaises(AttributeError, lambda: E.A.getBLabel())
		self.assertRaises(AttributeError, lambda: E.mylabel())
	
	def test_comparitor(self):
		class Enum1(Enum):
			A = 1
			B = 2
		
		class Enum2(Enum):
			A = 1
			B = 2
		
		self.assertGreater(Enum1.B, Enum1.A)
		
		self.assertRaises(TypeError, lambda: Enum1.A > Enum2.A)
	
	def test_repr_labels(self):
		class MyEnum4(Enum):
			A = 1
			B = 3, 'Hello'
			UPPER_CASE_WORD = 4
		
		self.assertEqual(repr(MyEnum4.A), 'MyEnum4.A')
		
		self.assertEqual(str(MyEnum4.A), 'A')
		self.assertEqual(str(MyEnum4.B), 'Hello')
		self.assertEqual(str(MyEnum4.UPPER_CASE_WORD), 'Upper Case Word')
		
		self.assertEqual(MyEnum4(3).label, 'Hello')
	
	def test_membership(self):
		class MyEnum4(Enum):
			A = 1
			B = 3, 'Hello'
			UPPER_CASE_WORD = 4
		
		self.assertListEqual(list(MyEnum4), [MyEnum4.A, MyEnum4.B, MyEnum4.UPPER_CASE_WORD])
		self.assertIn(MyEnum4.A, MyEnum4)
		self.assertNotIn(1, MyEnum4)
	
	def test_display_order(self):
		class MyEnum6(Enum):
			class Meta(object):
				properties = ('value', 'display_order')
			A = 1, 2
			B = 2, 3
			C = 3, 1
		
		self.assertEqual(MyEnum6.A.display_order, 2)
		self.assertListEqual(list(MyEnum6), [MyEnum6.C, MyEnum6.A, MyEnum6.B])
	
	def test_hashable(self):
		class EnumH(Enum):
			A = 1
			B = 2
		
		_ = hash(EnumH.A)
		d = { EnumH.A : 'a'}
		self.assertEqual(d[EnumH.A], 'a')
	
	def test_pickle(self):
		import pickle
		
		d = pickle.dumps(EnumP.A, pickle.HIGHEST_PROTOCOL)
		r = pickle.loads(d)
		
		self.assertEqual(r, EnumP.A)
