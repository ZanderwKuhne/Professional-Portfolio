#include "utils.h"

void irq_handler() {
  gen_timer_reset(get_timer_freq());
  timer_tick();
}

void sync_error_handler() { print("PANIC: SYNC ERROR!"); }
