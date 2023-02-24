from __future__ import print_function
from bcc import BPF
from time import sleep
from sys import argv

def usage():
    print("USAGE: %s [interval [count]]" % argv[0])
    exit()

interval = 5
count = -1

if len(argv) > 1:
	try:
		interval = int(argv[1])
		if interval == 0:
			raise
		if len(argv) > 2:
			count = int(argv[2])
	except:	# also catches -h, --help
		usage()
		
b = BPF(src_file='11-vfsreadlat.c')
b.attach_kprobe(event='vfs_read', fn_name='do_entry')
b.attach_kretprobe(event='vfs_read', fn_name='do_return')

print('Tracing... Hit Ctrl-C to end.')

# output
loop = 0
do_exit = 0
while (1):
	if count > 0:
		loop += 1
		if loop > count:
			exit()
	try:
		sleep(interval)
	except KeyboardInterrupt:
		pass; do_exit = 1

	print()
	b["dist"].print_log2_hist("usecs")
	b["dist"].clear()
	if do_exit:
		exit()