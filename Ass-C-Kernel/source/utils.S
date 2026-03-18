.globl delay
.globl get_el
delay:
  subs x0, x0, #1
  bne delay
  ret

.globl put32
put32:
  str w1, [x0]
  ret

.global get32
get32:
  ldr w0, [x0]
  ret

get_el:
  mrs x0, CurrentEL
  lsr x0, x0, #2
  ret

.globl gen_timer_init
gen_timer_init:
  mov x0, #1
  msr cntp_ctl_el0, x0
  ret

.globl gen_timer_reset
gen_timer_reset:
  msr cntp_tval_el0, x0
  ret

.globl enable_irq
enable_irq:
  msr daifclr, #2
  ret

.globl set_vbar
set_vbar:
  msr vbar_el1, x0
  ret

.globl get_timer_freq
get_timer_freq:
  mrs x0, cntfrq_el0
  ret
