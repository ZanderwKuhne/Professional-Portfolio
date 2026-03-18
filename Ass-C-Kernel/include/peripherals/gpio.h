#pragma once

#include "common.h"

#include "peripherals/base.h"

struct GpioPinData {
  reg32 reserved;
  reg32 data[2];
};

struct GpioRegs {
  reg32 func_select[6];
  struct GpioPinData output_set;
  struct GpioPinData output_clear;
  struct GpioPinData lvl;
  struct GpioPinData event_dt_stat;
  struct GpioPinData rising_edge_dt_en;
  struct GpioPinData falling_edge_dt_en;
  struct GpioPinData high_dt_en;
  struct GpioPinData low_dt_en;
  struct GpioPinData async_red;
  struct GpioPinData async_fed;
  reg32 reserved;
  reg32 pu_pd_en;
  reg32 pu_pd_clock[2];
};

#define REGS_GPIO ((struct GpioRegs *)(PBASE + 0x00200000))
