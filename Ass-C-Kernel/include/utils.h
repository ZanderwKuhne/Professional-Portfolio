#pragma once

#include "common.h"

void delay(u64 ticks);
void put32(u64 address, u32 value);
u32 get32(u64 address);
int strcmp(char *s1, char *s2);
int get_el();
void gen_timer_init(void);
void gen_timer_reset(unsigned long interval);
void enable_irq(void);

void disable_irq(void);

void set_vbar(unsigned long addr);
unsigned long get_timer_freq();
void timer_init();
void timer_tick();
unsigned long get_uptime();

void itoa(long n, char *s);
void print(char *fmt, ...);

extern void exception_vectors(void);
static volatile unsigned long system_uptime_seconds = 0;
