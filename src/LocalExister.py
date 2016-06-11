#!/usr/bin/env python3

import psycopg2, psycopg2.extras


from os import path
import sys
import uuid
import subprocess
import time

argv = sys.argv

if len(argv) != 3:
	print('usage: python3 LocalExister.py path_to_in_file exec_command')
	sys.exit(1)

case_num = int(open(path.join(argv[1], 'info.txt'), 'r').read().strip())

print('# of case:', case_num, file=sys.stderr)


exec_tle = 600 # 10分

for i in range(1, case_num+1):
	import time
	s_time = time.time()
	run_res = subprocess.call(
		['bash', '-c', argv[2]],
		stdin=open(path.join(argv[1], str(i)+'.txt'), 'rb'),
		timeout=exec_tle)
	print('Case #', i, ' time:', (int)((time.time()-s_time)*1000), 'ms', file=sys.stderr)

