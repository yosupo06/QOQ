#!/usr/bin/env python3

import psycopg2, psycopg2.extras

from os import path
import sys
import uuid
import time

argv = sys.argv

if len(argv) != 4:
	print('usage: python3 Appender.py path_to_in_file source_ext path_to_source_file')
	sys.exit(1)

import Config
con = psycopg2.connect(**Config.cfg['dbinfo'])
cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

case_num = int(open(path.join(argv[1], 'info.txt'), 'r').read().strip())

print('# of case:', case_num)

src = open(argv[3], 'rb').read()

query_hs = uuid.uuid4().hex
qlist = []
for i in range(1, case_num+1):
	qlist.append(
		(query_hs, i, argv[2], src, open(path.join(argv[1], str(i)+'.txt'), 'rb').read()))

cur.executemany(
	'INSERT INTO queue(hash, idx, src_ext, src, in_file) VALUES(%s, %s, %s, %s, %s)',
	qlist)
con.commit()

out = [bytes() for i in range(case_num)]

exec_c = 0
while exec_c < case_num:
	cur.execute('SELECT * FROM result WHERE hash = %s LIMIT 1 FOR UPDATE', [query_hs]);
	row = cur.fetchone()
	if not row:
		con.commit();
		print('waiting...')
		time.sleep(3);
		continue
	hs = row['hash']
	idx = row['idx']
	cur.execute('DELETE FROM result WHERE hash = %s AND idx = %s', [hs, idx]);
	con.commit()
	if hs != query_hs or idx < 1 or case_num < idx:
		print('わけわからんでしょ')
		sys.exit(1)
	print('Case #{} end. Time={}ms Judge status={}'.format(idx, row['exec_time'], row['result']))
	out[idx-1] = row['out_file']
	exec_c += 1

open('answer.txt', 'wb').write(b''.join(out))
cur.close()
con.close()

