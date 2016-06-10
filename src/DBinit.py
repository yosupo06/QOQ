#!/usr/bin/env python3

import psycopg2


import Config
con = psycopg2.connect(**Config.cfg['dbinfo'])

cur = con.cursor()

cur.execute('DROP TABLE IF EXISTS queue')
cur.execute('DROP TABLE IF EXISTS result')

cur.execute('''
	CREATE TABLE queue (
		hash	CHAR(32),
		idx		INT,
		src_ext	VARCHAR(10),
		src		BYTEA,
		in_file BYTEA
	)
	''');

cur.execute('''
	CREATE TABLE result (
		hash		CHAR(32),
		idx			INT,
		result		VARCHAR(100),
		out_file	BYTEA,
		exec_time	INT
	)
	''');

con.commit()

cur.close()
con.close()
