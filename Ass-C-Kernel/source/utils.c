#include <mini_uart.h>
#include <stdarg.h>
#include <utils.h>

#define CORE0_TIMER_IRQ_CTRL 0x40000040

int strcmp(char *s1, char *s2) { // adding basic string comparison
  while (*s1 && (*s1 == *s2)) {
    s1++;
    s2++;
  }
  return *(unsigned char *)s1 - *(unsigned char *)s2;
}

void itoa(long n, char *s) {
  long i, sign;
  if ((sign = n) < 0)
    n = -n;
  i = 0;
  do {
    s[i++] = n % 10 + '0';
  } while ((n /= 10) > 0);
  if (sign < 0)
    s[i++] = '-';
  s[i] = '\0';

  for (int j = 0, k = i - 1; j < k; j++, k--) {
    char temp = s[j];
    s[j] = s[k];
    s[k] = temp;
  }
}

void timer_tick() { system_uptime_seconds++; }
unsigned long get_uptime() { return system_uptime_seconds; }

void print(char *fmt, ...) {
  va_list args;
  va_start(args, fmt);

  for (char *p = fmt; *p != '\0'; p++) {
    if (*p != '%') {
      uart_send(*p);
      continue;
    }
    p++;
    switch (*p) {
    case 's': {
      char *s = va_arg(args, char *);
      uart_send_str(s);
      break;
    }
    case 'd': {
      int d = va_arg(args, int);
      char buf[32];
      itoa(d, buf);
      uart_send_str(buf);
      break;
    }
    case 'c': {
      char c = (char)va_arg(args, int);
      uart_send(c);
      break;
    }
    }
  }
  va_end(args);
}

void timer_init() { *(unsigned int *)CORE0_TIMER_IRQ_CTRL = (1 << 1); }
