import sys
import os

cur_file = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_file + '/../analyzers')
sys.path.append(cur_file + '/../analyzers/constraints')

import ohlc_difference_factor_constraint
import binary_analyzer
import slope_constraint

import json

# NOTE: this may be too simple to be a class

class json_loader:
	""" class for loading analyzer and constraints from a json file
	accepts date, symbols and constraints
	json filename must be provided
	"""

	# available types of constraints
	constraint_types = {
		"ohlc_difference_factor_constraint":ohlc_difference_factor_constraint.ohlc_difference_factor_constraint,
		"slope_constraint":slope_constraint.slope_constraint
	}

	def load(self, file):
		""" load constraints and analyzer info
		returns the analyzer with attached constraints
		"""
		with open(file) as data_file:
			data = json.load(data_file)

		analyzer = binary_analyzer.binary_analyzer()

		analyzer.set_symbols(data["symbols"])

		if(data["dates"] != None):
			analyzer.set_date(data["dates"][0])

		for constraint_info in data["constraints"]:
			constraint = self.constraint_types[constraint_info['type']](constraint_info['offset'], constraint_info['days'])

			if(constraint_info['type'] == 'ohlc_difference_factor_constraint'):
				if(constraint_info['left_abs'] != None):
					constraint.set_left_abs(constraint_info['left_abs'])
				if(constraint_info['right_abs'] != None):
					constraint.set_right_abs(constraint_info['right_abs'])

				# if the json file is using null to mean no factor
				# we set the factor to 1
				if(constraint_info['factor1'] == None):
					constraint_info['factor1'] = 1
				if(constraint_info['factor2'] == None):
					constraint_info['factor2'] = 1
				if(constraint_info['factor3'] == None):
					constraint_info['factor3'] = 1
				if(constraint_info['factor4'] == None):
					constraint_info['factor4'] = 1

				constraint.set_left_side(first = constraint_info['first'],
					factor1 = constraint_info['factor1'],
					operation = constraint_info['operation1'],
					second = constraint_info['second'],
					factor2 = constraint_info['factor2']
					)

				constraint.set_comparison(constraint_info['comparison'])

				constraint.set_right_side(third = constraint_info['third'],
					factor3 = constraint_info['factor3'],
					operation = constraint_info['operation2'],
					fourth = constraint_info['fourth'],
					factor4 = constraint_info['factor4']
					)
			elif(constraint_info['type'] == 'slope_constraint'):
				constraint.set_slope_type = constraint_info['slope_type']
				constraint.set_slope_min_max(constraint_info['min_slope'], constraint_info['max_slope'])
			analyzer.add_constraint(constraint)
		return analyzer
