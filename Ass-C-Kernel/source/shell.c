#include "shell.h"
#include "common.h"
#include "mini_uart.h"
#include "utils.h"

void shell_run() {
  char buffer[MAX_BUFFER_SIZE];
  int i = 0;

  uart_send_str("\nzk-> ");

  while (1) {
    char c = uart_recv();
    uart_send(c);

    if (c == '\r' || c == '\n') {
      buffer[i] = '\0';
      print("\r\n");

      if (i > 0) {
        if (strcmp(buffer, "-help") == 0) {
          print("Available Commands: -help, -hello, -reboot, -uptime\n");
        } else if (strcmp(buffer, "-hello") == 0) {
          print("Hello Zander!\n");
        } else if (strcmp(buffer, "-reboot") == 0) {
          print("Seeya!\n");
        } else if (strcmp(buffer, "-el") == 0) {
          print("Current Exception Level: EL%d\r\n", get_el());
        } else if (strcmp(buffer, "-uptime") == 0) {
          print("System Uptime: %d seconds \r\n", get_uptime());
        } else {
          print("Command not recognized! : %s\r\n", buffer);
        }
      }
      i = 0;
      print("zk-> ");
    } else if (c == 127 || c == 8) {
      if (i > 0) {
        i--;
        print("\b \b");
      }
    } else if (i < MAX_BUFFER_SIZE - 1) {
      buffer[i++] = c;
    }
  }
}
