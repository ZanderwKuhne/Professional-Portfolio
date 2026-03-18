#include "../include/mm.h"

.section ".text.boot"

.globl _start
_start:
  mrs x0, mpidr_el1
  and x0, x0, #0xFF
  cbz x0, master
  b proc_hang

master:
  mrs x0, CurrentEL
  lsr x0, x0, #2
  
  cmp x0, #3
  b.eq setup_el3
  cmp x0, #2
  b.eq setup_el1
  b el1_entry

setup_el3:
  mov x0, #((1 << 10) | (1 << 0))
  msr scr_el3, x0

  adr x0, setup_el1
  msr elr_el3, x0

  mov x0, #0x3c9
  msr spsr_el3, x0

  msr cnthp_ctl_el2, xzr

  eret

setup_el1:
  mov x0, #(1 << 31)
  msr hcr_el2, x0

  adr x0, el1_entry
  msr elr_el2, x0

  mov x0, #0x3c5
  msr spsr_el2, x0
  
  mov x0, #0x300000
  msr cpacr_el1, x0

  mov x0, #3
  msr cnthp_ctl_el2, x0
  msr cntvoff_el2, xzr

  eret

el1_entry:
  ldr x0, =LOW_MEMORY
  mov sp, x0

  adr x0, bss_begin
  adr x1, bss_end
  sub x1, x1, x0
  bl memzero

  bl kernel_main
  b proc_hang

proc_hang:
  wfe
  b proc_hang
