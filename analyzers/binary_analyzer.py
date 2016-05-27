import sys
import os
import time
import json
cur_file = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_file + '/../../data_provider')

import data_provider

class binary_analyzer:
	""" analyzer class which can have constraints attached
	will check all attached constraints and return results for them
	dates and symbols can also be specified
	"""

	# list of constraints on this analyzer
	constraints = []

	symbol = None
	date = None
	results = []
	data_provider = None

	def __init__(self):
		self.data_provider = data_provider.data_provider()

	def check_constraints(self):
		""" checks all constraints on this analyzer
		returns a two dimensional array of results
		"""
		if(self.date != None):
			for symbol in self.symbols:
				result = []
				for constraint in self.constraints:
					if(constraint.check(self.date, symbol)):
						result.append(True)
					else:
						result.append(False)
				self.results.append([self.date, symbol, result])
			return self.results
		else:
			for symbol in self.symbols:
				dates = self.data_provider.get_dates(symbol)
				for date in dates:
					#datedatedate
					date = date['date']
					result = []
					for constraint in self.constraints:
						if(constraint.check(date, symbol)):
							result.append(True)
						else:
							result.append(False)
					self.results.append([date, symbol, result])
			return self.results


	def set_symbols(self, symbols):
		""" sets the symbols to be used by this analyzer
		symbols must be an array
		"""
		self.symbols = symbols

	def unset_symbol(self):
		""" sets the symbol to None
		"""
		self.symbols = None

	def set_date(self, date):
		""" sets the date to be used by this analyzer
		"""
		self.date = date

	def unset_date(self):
		""" sets the date to None
		this will cause the analyzer to use all available dates
		"""
		self.date = None

	def add_constraint(self, constraint):
		""" adds a new contraint to the analyzer
		"""
		self.constraints.append(constraint)

	def remove_constraint(self, index):
		""" removes the constraint at index
		"""
		self.constraints.pop(index)

	def get_constraints(self):
		""" returns a copy of the constrain list
		"""
		return self.constraints[:]


