import matplotlib.pyplot as plt
import numpy as np
import sqlite3 as sql
from matplotlib.finance import candlestick_ohlc
import matplotlib
import sys

def chart_dates(symbol, date1 = None, date2 = None, db_name = '../db/kyandoru.db', show = 1):
	""" Creates a candle chart for a given stock and dates
	symbol is the ticker symbol of the stock e.g. "AAON".
	(optional) date1 and date2 must be provided together and
		will restrict the search to after date1 and before date2
		should be in the format YYYY-MM-DD
		or if None is passed for either they will be ignored
	(optional) db_name is the name of the database to get data from
	(optional) show is a boolean that determines whether to display the graph at the end
	returns a matplotlib pyplot object
	"""
	con = None
	con = sql.connect(db_name)
	cur = con.cursor()

	if(date1 == None or date2 == None):
		cur.execute('SELECT * FROM eods WHERE symbol = '+symbol)
	else:
		cur.execute('SELECT * FROM eods WHERE symbol = \"'+symbol+'\" and date > \"'+date1+'\" and date < \"'+date2+'\"')
	
	# fetch the rows selected in our sql statement
	rows = cur.fetchall()

	ohlc = []
	for row in rows:
		date = matplotlib.dates.datestr2num(row[1])
		open = row[2]
		high = row[3]
		low = row[4]
		close = row[5]
		volume = row[6]
		append_me = (date, open, high, low, close, volume) 
		ohlc.append(append_me)
	fig = plt.figure()
	ax1 = plt.subplot2grid((1,1), (0,0))

	candlestick_ohlc(ax1, ohlc)

	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.title('stock')
	plt.legend()
	plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
	
	if(show == 1):
		plt.show()

	return plt