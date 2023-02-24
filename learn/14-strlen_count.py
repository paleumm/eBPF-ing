from __future__ import print_function
from bcc import BPF
from bcc.utils import printb
from time import sleep

b = BPF(src_file='14-strlen_count.c')
b.attach_uprobe(name='c', sym='strlen', fn_name='count')

print("Tracing strlen()... Hit Ctrl-C to end.")

try:
    sleep(99999999)
except KeyboardInterrupt:
    pass

# print output
print("%10s %s" % ("COUNT", "STRING"))
counts = b.get_table("counts")
for k, v in sorted(counts.items(), key=lambda counts: counts[1].value):
    printb(b"%10d \"%s\"" % (v.value, k.c))