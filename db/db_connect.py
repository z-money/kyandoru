import sqlite3 as sql
import os


class db_connect:
	""" A wrapper class for database connections
	"""

	def __init__(self, db_name='kyandoru.db'):
		self.db_name = db_name
		self.con = sql.connect(os.path.abspath(os.path.dirname(__file__)) + '/' + self.db_name)
		self.con.row_factory = self.dict_factory
		self.cur = self.con.cursor()
		self.cur.execute("PRAGMA busy_timeout = 10000")

	def dict_factory(self, cursor, row):
	    """ allows for the return of associative arrays
	    """
	    d = {}
	    for idx, col in enumerate(cursor.description):
	        d[col[0]] = row[idx]
	    return d

	def quote_identifier(self, s, errors="backslashreplace"):
		""" encodes strings to avoid db errors around quotes
		"""
	    encodable = s.encode("utf-8", errors).decode("utf-8")

	    nul_index = encodable.find("\x00")

	    if nul_index >= 0:
	        error = UnicodeEncodeError("utf-8", encodable, nul_index, nul_index + 1, "NUL not allowed")
	        error_handler = codecs.lookup_error(errors)
	        replacement, _ = error_handler(error)
	        encodable = encodable.replace("\x00", replacement)

	    return "\"" + encodable.replace("\"", "\"\"") + "\""

	def execute(self, sql_string, params = None):
		if(params == None):
			self.cur.execute(sql_string)
		else:
			self.cur.execute(sql_string, params)

	def execute_q(self, sql_string, params):
		self.cur.execute(sql_string + self.quote_identifier(params))

	def upsert(self, table, columns, values, keys = None, key_values = None):
		""" an upsert command for sqlite
		"""
		insert = 'INSERT OR IGNORE INTO '+table+' ('
		if(keys != None):
			insert_columns = keys + columns
			insert_values = key_values + values
		else:
			insert_columns = columns
			insert_values = values
		for column in insert_columns:
			insert += column + ', '
		insert = insert[:-2]
		insert += ') values('
		for i in range(0, len(insert_values)):
			insert += '?, '
		insert = insert[:-2]
		insert += ')'

		update = 'UPDATE '+table+' SET '
		index = 0
		for column in columns:
			if(isinstance(values[index], str)):
				value = self.quote_identifier(values[index])
			else:
				value = values[index]
			update += column +' = '+str(value)+', '
			index += 1
		update = update[:-2]
		if(keys != None):
			index = 0
			update += ' WHERE '
			for key in keys:
				if(isinstance(key_values[index], str)):
					value = self.quote_identifier(key_values[index])
				else:
					value = key_values[index]
				update += key + ' = '+ str(value) +' AND '
				index += 1
			update = update[:-5]

		self.cur.execute(insert, insert_values)
		self.cur.execute(update)

	def fetchall(self):
		return self.cur.fetchall()

	def fetchone(self):
		return self.cur.fetchone()

	def open(self):
		self.con = sql.connect(os.path.abspath(os.path.dirname(__file__)) + '/' + self.db_name)
		self.con.row_factory = self.dict_factory
		self.cur = self.con.cursor()
		self.cur.execute("PRAGMA busy_timeout = 10000")

	def close(self):
		try:
			self.con.close()
		except:
			return -1

	def commit(self):
		self.con.commit()