import csv

import sqlite3 as sql

""" Saves stock symbols and some info to the database.
Requires a CSV of stock symbols.
"""


con = None
con = sql.connect('db/kyandoru.db')
cur = con.cursor()

cur.execute('DROP TABLE IF EXISTS stock')
cur.execute('CREATE TABLE stock(symbol char(10) PRIMARY KEY, name char(200), last_sale real, market_cap real, adr_tso real, ipo_year int, sector char(100), industry char(100), exchange char(20));')

with open('data/companylistNASDAQ.csv') as csvfile:
	stock_reader = csv.reader(csvfile, delimiter = ',')
	next(csvfile)
	for row in stock_reader:
		cur.execute('INSERT INTO stock VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], 'NASDAQ'))

with open('data/companylistNYSE.csv') as csvfile:
	stock_reader = csv.reader(csvfile, delimiter = ',')
	next(csvfile)
	for row in stock_reader:
		try:
			cur.execute('INSERT INTO stock VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], 'NYSE'))
		except sql.IntegrityError:
			continue

con.commit()