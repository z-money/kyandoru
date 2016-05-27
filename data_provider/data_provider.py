import sys
import os
from datetime import datetime, timedelta
import time

cur_file = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_file + '/../db')

import db_connect as db

class data_provider:
	""" Provides access to the database for common queries
	
	Motivation: this class is partially a convenience wrapper,
	but more importantly it serves as a cache for stock data on a single symbol.
	Querying for all stock_hv data for a given stock is relatively quick.
	However, reconnecting to the db multiple times to get data is slow.
	So, when a user calls get_days to get data on certain days for a stock,
	we gather all days for that stock.  Then, when the user asks for different days
	for that same stock, we simply grab them from memory rather than requerying the db.
	To avoid using too much memory we only hold one stock at a time.

	Using a dedicated caching library would be another good option 
	"""
	symbol = None
	data = None
	def __init__(self):
		self.dbc = db.db_connect()


	def get_days(self, date, symbol, days):
		""" Returns ohlcv data for symbol
		starting at date for "days" days.
		"""
		if(self.symbol != symbol or self.data == None):
			self.symbol = symbol
			self.dbc.execute('SELECT open, high, low, close, volume, date FROM stock_hv WHERE symbol = \''+symbol+'\'')
			self.data = self.dbc.fetchall()
		end_date = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=days)
		end_date = end_date.strftime('%Y-%m-%d')

		#db.execute('SELECT open, high, low, close, volume FROM stock_hv where symbol = \''+symbol+'\' and date <= \'' + date + '\' AND date > \'' + end_date + '\'')
		result = []

		for el in self.data:
			if(el['date'] <= date and el['date'] >= end_date):
				result.append(el)


		return result

	def get_dates(self, symbol = None):
		""" Returns the dates for which data exists
		for symbol
		"""
		if(symbol == None):
			self.dbc.execute('SELECT distinct(date) FROM stock_hv ORDER BY date')
		else:
			self.dbc.execute('SELECT date FROM stock_hv WHERE symbol = \"'+symbol+'\" ORDER BY date DESC')
		return self.dbc.fetchall()