#include "common.h"
#include "mini_uart.h"
#include "shell.h"
#include "utils.h"

void kernel_main() {
  uart_init();
  uart_send_str("Raspberry Pi Bare Metal Basics OS Initializing...\n");

#if RPI_VERSION == 3
  uart_send_str("\tBoard: Raspberry PI 3\n");
#endif

  extern void exception_vectors();
  set_vbar((unsigned long)&exception_vectors);

  timer_init();
  gen_timer_init();
  gen_timer_reset(get_timer_freq());
  enable_irq();

#if RPI_VERSION == 4
  uart_send_str("\tBoard: Raspberry PI 4\n");
#endif

  uart_send_str("\n\nDone\n");

  shell_run();
}
