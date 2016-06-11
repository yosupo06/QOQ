#!/usr/bin/env python3

import psycopg2, psycopg2.extras

import os
import sys
import uuid
import subprocess
import time

argv = sys.argv

if len(argv) != 2:
	print('usage: python3 Exister.py tmpdir_name(distinct with proccess)')
	sys.exit(1)

compile_tle = 60 # 1分
exec_tle = 600 # 10分

workdir = argv[1]
if not os.access(workdir, os.F_OK):
	os.mkdir(workdir)

import Config
con = psycopg2.connect(**Config.cfg['dbinfo'])
cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

while True:
	cur.execute('SELECT * FROM queue LIMIT 1 FOR UPDATE')
	row = cur.fetchone()
	if not row:
		con.commit();
		print('waiting...')
		time.sleep(3);
		continue
	print(row)
	res = {'hash':row['hash'], 'idx':row['idx'], 'exec_time':-1}
	cur.execute('DELETE FROM queue WHERE hash = %s AND idx = %s', [row['hash'], row['idx']])
	con.commit()
	open(os.path.join(workdir, 'src_tmp.txt'), 'wb').write(row['src'])
	open(os.path.join(workdir, 'in.txt'), 'wb').write(row['in_file'])
	cmp_res = subprocess.call(
		['./shell/compile_{}.sh'.format(row['src_ext']), workdir],
		timeout=compile_tle)
	if cmp_res != 0:
		res['result'] = 'CE:compile error'
		res['out_file'] = 'ここにエラー出力を出したい'
	else:
		import time
		s_time = time.time()
		run_res = subprocess.call(
			['./shell/run_{}.sh'.format(row['src_ext']), workdir],
			timeout=exec_tle)
		res['exec_time'] = (int)((time.time()-s_time)*1000)
		if run_res != 0:
			res['result'] = 'RE:runtime error'
			res['out_file'] = 'ここにエラー出力を出したい'
		else:
			res['result'] = 'OK'
			res['out_file'] = open(os.path.join(workdir, 'out.txt'), 'rb').read()
	cur.execute(
		'INSERT INTO result(hash, idx, result, out_file, exec_time) VALUES(%s, %s, %s, %s, %s)',
		(res['hash'], res['idx'], res['result'], res['out_file'], res['exec_time']));
	con.commit()

cur.close()
con.close()
