import constraint
import sys
import os
cur_file = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_file + '/../')
sys.path.append(cur_file + '/../../data_provider')

import data_provider
import time

class ohlc_change_constraint:
	offset = None
	days = None
	dp = None

	def __init__(self, offset, days):
		self.offset = offset
		self.days = days
		self.dp = data_provider.data_provider()

	min_o = None
	max_o = None
	
	min_h = None
	max_h = None
	
	min_l = None
	max_l = None
	
	min_c = None
	max_c = None

	def set_o(self, min_o, max_o):
		self.min_o = min_o
		self.max_o = max_o

	def set_h(self, min_h, max_h):
		self.min_h = min_h
		self.max_h = max_h
	
	def set_o(self, min_l, max_l):
		self.min_l = min_l
		self.max_l = max_l
	
	def set_o(self, min_c, max_c):
		self.min_c = min_c
		self.max_c = max_c

	def check(self, date, symbol):
		data = self.dp.get_days(date, symbol, self.days*2 + self.offset*2)
		
		if(len(data) < self.days + self.offset):
			return False
		for i in range(self.days):
			if(self.min_o != None and self.max_o != None):
				delta_o = data[i]['open'] - data[i+self.offset]['open']
				if(delta_o < self.min_o or delta_o > self.max_o):
					return False
			if(self.min_h != None and self.max_h != None):
				delta_h = data[i]['high'] - data[i+self.offset]['high']
				if(delta_h < self.min_h or delta_h > self.max_h):
					return False
			if(self.min_l != None and self.max_l != None):
				delta_l = data[i]['low'] - data[i+self.offset]['low']
				if(delta_l < self.min_l or delta_l > self.max_l):
					return False
			if(self.min_c != None and self.max_c != None):
				delta_c = data[i]['close'] - data[i+self.offset]['close']
				if(delta_c < self.min_c or delta_c > self.max_c):
					return False
		return True


