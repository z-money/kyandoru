import constraint
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as smf

cur_file = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_file + '/../../data_provider')

import data_provider

class slope_constraint:
	""" Constraint on the slope over a period of days.
	"""
	min_slope = None
	max_slope = None
	days = None
	slope_type = None
	dp = None

	def __init__(self, offset, days, min_slope = None, max_slope = None, slope_type = 'close'):
		self.days = days
		self.dp = data_provider.data_provider()
		self.slope_type = slope_type
		self.min_slope = min_slope
		self.max_slope = max_slope

	def set_slope_type(self, slope_type):
		self.slope_type = slope_type

	def set_slope_min_max(self, min_slope, max_slope):
		self.max_slope = max_slope
		self.min_slope = min_slope

	def get_slope(self, y):
		""" Calculates the slope over a range of days
		y should be a list of values
		returns the slope
		"""
		x = range(len(y)+1)[1:]
		x = smf.add_constant(x)

		model = smf.OLS(y,x)
		results = model.fit()

		return results.params[1]

	def check(self, date, symbol):
		""" checks whether the slope fits the constraint
		for symbold starting at date for self.days days
		"""
		data = self.dp.get_days(date, symbol, self.days+1)

		if(len(data) < self.days):
			return False

		y = [el[self.slope_type] for el in data]

		slope = self.get_slope(y)

		if(slope < self.min_slope or slope > self.max_slope):
			return False
		else:
			return True