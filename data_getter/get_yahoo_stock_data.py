import csv
import sqlite3 as sql
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../db')
import db_connect as db

import urllib
import urllib.request

import binascii

""" Downloads CSVs of stock data from the yahoo finance api
the single letter variables are intentional because those are the variable names
in the request url.
Requires the database to already be populated with stock symbols.
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

files = os.listdir('../data/yahoo/stocks/')

dbc = db.db_connect()
dbc.execute('SELECT symbol from stock')
symbols = dbc.fetchall()

for symbol in symbols:
	symbol = symbol['symbol']
	
	if(len(files) > 0 and str(symbol + '.csv') == str(files[-1])):
		print('deleting '+symbol+'.csv')
		os.remove('../data/yahoo/stocks/'+symbol+'.csv')
	elif(symbol + '.csv' in files):
		print('skipping '+symbol+'.csv')
		continue

	print('Fetching '+urllib.parse.quote_plus(symbol)+'...')
	for year in range(2016, 1970, -1):
		c = year
		f = year + 1
		try:
			response = urllib.request.urlopen(url + build_param_string(symbol, a, b, c, d, e, f, g) + "&ignore=.csv")
			content = response.read()

			f = open('../data/yahoo/stocks/'+symbol+'.csv', 'a')
			f.write(content.decode('ascii'))
		except urllib.error.HTTPError as err:
			print(err.code)
			print('Unable to retrive '+urllib.parse.quote_plus(symbol)+' for year ' + str(year))

			break


