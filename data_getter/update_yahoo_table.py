import csv
import sqlite3 as sql
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../db')
import db_connect as db

""" Saves stock data from the yahoo CSVs to the database
Just adds any missing data from the CSVs.
"""

files = os.listdir('../data/yahoo/stocks/')

dbc = db.db_connect()

dbc.execute('CREATE TABLE IF NOT EXISTS yahoo(symbol char(10), date char(100), open real, high real, low real, close real, volume real);')

for filename in files:
	with open('../data/yahoo/stocks/'+filename) as csvfile:
		symbol = filename[:-4]

		dbc.execute('SELECT max(date) FROM yahoo WHERE symbol = \"'+symbol+'\"')
		last_stock_date = dbc.fetchone()['max(date)']

		eod_reader = csv.reader(csvfile, delimiter = ',')

		for row in eod_reader:
			if(row[0] == 'Date' or (last_stock_date != None and last_stock_date >= row[0])):
				continue
			dbc.execute('INSERT OR IGNORE INTO stock_hv VALUES(?, ?, ?, ?, ?, ?, ?)', (symbol, row[0], row[1], row[2], row[3], row[4], row[5]))

dbc.commit()