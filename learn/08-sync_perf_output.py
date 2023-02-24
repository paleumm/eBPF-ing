# nir

from bcc import BPF

prog = '''
#include <uapi/linux/ptrace.h>

struct data_t {
    u64 ts;
};
BPF_PERF_OUTPUT(events);

int do_trace(struct pt_regs *ctx) {
    struct data_t data = {};
    data.ts = bpf_ktime_get_ns();
    events.perf_submit(ctx, &data, sizeof(data));
    return 0;
}
'''

# load programs
b = BPF(text=prog)

b.attach_kprobe(event=b.get_syscall_fnname("sync"), fn_name="do_trace")
print("Tracing for quick sync's... Ctrl-C to end")

start = 0
def print_event(cpu, data, size):
    global start
    event = b["events"].event(data)
    if start == 0:
        start = event.ts

    time_s = (float(event.ts - start)) / 1000000000
    print("At time %.2f s: multiple syncs detected" % (time_s))

# loop with callback to print_event
b["events"].open_perf_buffer(print_event)
while 1:
    b.perf_buffer_poll()   