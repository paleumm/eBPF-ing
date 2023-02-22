from __future__ import print_function
from bcc import BPF

# programs
prog = '''
#include <uapi/linux/ptrace.h>

BPF_HASH(last);

int do_trace(struct pt_regs *ctx) {
    u64 ts, *tsp, delta, key = 0, count = 0;

    // attempt to read stored timestamp
    tsp = last.lookup(&key);
    if (tsp != NULL) {
        delta = bpf_ktime_get_ns() - *tsp;
        bpf_trace_printk("%d\\n", delta / 1000000);
        last.delete(&key);
    }

    // update stored timestamp
    ts = bpf_ktime_get_ns();
    count += 1;
    last.update(&key, &count);
    return 0;
}
'''

# load programs
b = BPF(text=prog)

b.attach_kprobe(event=b.get_syscall_fnname("sync"), fn_name="do_trace")
print("Tracing for quick sync's... Ctrl-C to end")

start = 0
while 1:
    (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    if start == 0:
        start = ts

    ts = ts - start
    print("At time %.2f s: sync count is %s" % (ts, msg))