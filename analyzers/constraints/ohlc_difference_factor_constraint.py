import sys
import os
cur_file = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_file + '/../')
sys.path.append(cur_file + '/../../data_provider')

import data_provider
import operator

class ohlc_difference_factor_constraint:
	""" A constraint which compares two
	ohlc entries.
	"""
	
	ohlc = ["open", "high", "low", "close"]
	
	ops = {
		"+": operator.add,
		"-": operator.sub,
		"*": operator.mul,
		"/": operator.truediv,
		"%": operator.mod,
		"^": operator.xor,
		"=": operator.eq,
		"<": operator.lt,
		"<=": operator.le,
		">": operator.gt,
		">=": operator.ge,
		"!=": operator.ne
		}

	def __init__(self, offset, days):
		self.offset = offset
		self.days = days
		self.dp = data_provider.data_provider()
		self.left_abs = False
		self.right_abs = False
		self.name = None

	def set_name(name):
		self.name = name
	
	def get_name():
		return self.name

	def set_left_side(self, first, factor1 = 1, operation = None, second = None, factor2 = 1):
		""" sets the left side of the comparison
		"""
		self.first = first
		
		self.factor1 = factor1

		if(operation != None):
			self.operation1 = self.ops[operation]
	
		self.second = second

		self.factor2 = factor2

	def set_left_abs(self, _abs):
		""" sets whether we should take the absolute
		value of the left side of the comparison
		"""
		self.left_abs = _abs

	def set_comparison(self, comparison):
		""" sets the comparison operator
		"""
		self.comparison = self.ops[comparison]

	def set_right_side(self, third, factor3 = 1, operation = None, fourth = None, factor4 = 1):
		""" sets the right side of the comparison
		"""
		self.third = third
		
		self.factor3 = factor3

		if(operation != None):
			self.operation2 = self.ops[operation]
	
		self.fourth = fourth

		self.factor4 = factor4

	def set_right_abs(self, _abs):
		""" sets whether we should take the absolute
		value of the left side of the comparison
		"""
		self.right_abs = _abs

	def check(self, date, symbol):
		""" checks this comparison for
		date and symbol
		"""
		data = self.dp.get_days(date, symbol, self.days*2 + self.offset*2)

		if(len(data) < self.days + self.offset):
			return False

		
		for i in range(self.days):
			if(self.first != None and self.second == None and self.third != None and self.fourth == None):
				left = self.factor1*data[i + self.offset][self.first]
				right = self.factor3*data[i + self.offset][self.third]
			elif(self.first != None and self.second != None and self.third != None and self.fourth == None):
				left = self.operation1(self.factor1*data[i + self.offset][self.first], self.factor2*data[i + self.offset][self.second])
				right = self.factor3*data[i + self.offset][self.third]
			elif(self.first != None and self.second != None and self.third != None and self.fourth != None):
				left = self.operation1(self.factor1*data[i + self.offset][self.first], self.factor2*data[i + self.offset][self.second])
				right = self.operation2(self.factor3*data[i + self.offset][self.third], self.factor4*data[i + self.offset][self.fourth])
			
			if(self.left_abs):
				left = abs(left)
			if(self.right_abs):
				right = abs(right)

			if(self.comparison(left, right) != True):
				return False
		return True