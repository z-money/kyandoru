import csv
import sqlite3 as sql
import os
import sys
cur_file = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_file + '/../db')
import db_connect as db

""" Saves stock data from the yahoo CSVs to the database
deletes all existing data from the stock_hv TABLE
and rebuilds it from the CSVs.
"""


files = os.listdir(cur_file + '/../data/yahoo/stocks/')

dbc = db.db_connect()

dbc.execute('DROP TABLE IF EXISTS stock_hv')
dbc.execute('CREATE TABLE IF NOT EXISTS stock_hv(symbol char(10), date char(100), open real, high real, low real, close real, volume real, PRIMARY KEY(symbol, date));')

for filename in files:
	with open(cur_file + '/../data/yahoo/stocks/'+filename) as csvfile:
		symbol = filename[:-4]
		eod_reader = csv.reader(csvfile, delimiter = ',')

		for row in eod_reader:
			if(row[0] == 'Date'):
				continue
			dbc.execute('INSERT OR IGNORE INTO stock_hv VALUES(?, ?, ?, ?, ?, ?, ?)', (symbol, row[0], row[1], row[2], row[3], row[4], row[5]))

dbc.commit()