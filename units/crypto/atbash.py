from unit import BaseUnit
from collections import Counter
import sys
from io import StringIO
import argparse
from pwn import *
import os
import units.crypto
import string
import collections
import io
import units

# class Unit(units.PrintableDataUnit):
class Unit(units.NotEnglishAndPrintableUnit):

	PROTECTED_RECURSE = True
	PRIORITY = 60	
	def __init__(self, katana, parent, target, keywords=[]):
		super(Unit, self).__init__(katana, parent, target)

		try:
			self.raw_target = self.target.stream.read().decode('utf-8')
		except UnicodeDecodeError:
			raise units.NotApplicable("unicode error, unlikely usable cryptogram")

	def __init__(self, *args, **kwargs):
		super(Unit, self).__init__(*args, **kwargs)	

	def evaluate(self, katana, case):
		new_string = []
		reverse_upper = string.ascii_uppercase[::-1]
		reverse_lower = string.ascii_lowercase[::-1]

		with io.TextIOWrapper(self.target.stream, encoding='utf-8') as stream:
			try: 
				for character in iter(lambda: stream.read(1), ''):
					if character in string.ascii_uppercase:
						new_string.append(reverse_upper[string.ascii_uppercase.index(character)])
					elif character in string.ascii_lowercase:
						new_string.append(reverse_lower[string.ascii_lowercase.index(character)])
					else:
						new_string.append(character)
			except UnicodeDecodeError:
				# We can't decode this.... must usable...
				pass

		result = ''.join(new_string)

		katana.recurse(self, result)
		katana.locate_flags(self, result)
		katana.add_results(self, result)