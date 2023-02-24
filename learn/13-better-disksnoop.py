# nir not looking good

from __future__ import print_function
from bcc import BPF
from bcc.utils import printb

REQ_WRITE = 1

src = '''
TRACEPOINT_PROBE(block_rq_issue, block_rq_complete) {
    bpf_trace_printk("%s\\n", args->rwbs);
    return 0;
}
'''

b = BPF(text=src)

while 1:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    except ValueError:
        continue
    except KeyboardInterrupt:
        exit()
    printb(b"%s" % (msg))