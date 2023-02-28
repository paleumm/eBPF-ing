from __future__ import print_function
from bcc import BPF



b = BPF(src_file='drop.c')

b.attach_kprobe(event=b.get_syscall_fnname("clone"), fn_name='drop')
