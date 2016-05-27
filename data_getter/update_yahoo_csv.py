import csv
import sqlite3 as sql
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../db')
import db_connect as db

import urllib
import urllib.request
import time

""" Downloads CSVs of stock data from the yahoo finance api
the single letter variables are intentional because those are the variable names
in the request url.
Requires the database to already be populated with stock symbols.

This will do partial updates of files.
It will start adding rows to the CSVs at the last date present in the database.
This is good for updating the CSVs, but will work if the database exists but is empty
except for stock symbols.
"""

url = "https://ichart.yahoo.com/table.csv"

# ?s=CUDA&a=0&b=1&c=2012&d=0&e=30&f=2013&g=d&ignore=.csv"

def build_param_string(s, a, b, c, d, e, f, g):
	return "?s="+urllib.parse.quote_plus(s)+"&a="+str(a)+"&b="+str(b)+"&c="+str(c)+"&d="+str(d)+"&e="+str(e)+"&f="+str(f)+"&g="+g

# symbol
s = ""

# from day, month, year
a = 0
b = 1
c = 1970

# to day, month, year
d = 0
e = 1
f = 1971

# interval (d = day, w = week, m = month)
g = "d"

dbc = db.db_connect()
dbc.execute('SELECT * from stock')
stocks = dbc.fetchall()
dbc.execute('CREATE TABLE IF NOT EXISTS stock_hv')

for stock in stocks:
	dbc.execute('SELECT max(date) FROM stock_hv WHERE symbol = \"'+stock['symbol']+'\"')
	last_stock_date = dbc.fetchone()['max(date)']
	print('Fetching '+urllib.parse.quote_plus(stock['symbol'])+'...')

	if(last_stock_date != None and last_stock_date < time.strftime("%Y-%m-%d")):
		c = last_stock_date[0][:4]
		b = last_stock_date[0][5:7]
		a = last_stock_date[0][8:10]

		f = time.strftime("%Y")
		e = time.strftime("%m")
		d = time.strftime("%d")

		try:
			response = urllib.request.urlopen(url + build_param_string(stock['symbol'], a, b, c, d, e, f, g) + "&ignore=.csv")
			content = response.read()

			f = open('../data/yahoo/stocks/'+stock['symbol']+'.csv', 'a')
			f.write(content.decode('ascii'))
		except urllib.error.HTTPError as err:
			print(err.code)
			print('Unable to retrive '+urllib.parse.quote_plus(stock['symbol'])+' for year ' + str(year))

			break
	elif(last_stock_date == None):
		