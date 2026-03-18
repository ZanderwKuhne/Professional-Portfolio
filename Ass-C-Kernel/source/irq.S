.section ".text"

.extern irq_handler

.align 11
.globl exception_vectors
exception_vectors:
    // --- Set 1: Current EL with SP0 (Exceptions from EL1 using SP_EL0) ---
    .align 7
    b .             // 0x000: Synchronous
    .align 7
    b .             // 0x080: IRQ
    .align 7
    b .             // 0x100: FIQ
    .align 7
    b .             // 0x180: SError

    // --- Set 2: Current EL with SPx (Exceptions from EL1 using SP_EL1) ---
    // THIS IS WHERE YOUR TIMER LANDS (Address 0x280 from start of table)
    .align 7
    b .             // 0x200: Synchronous
    
    .align 7        // 0x280: IRQ
    sub sp, sp, #256
    stp x0, x1, [sp, #0]
    stp x2, x3, [sp, #16]
    stp x4, x5, [sp, #32]
    stp x6, x7, [sp, #48]
    stp x8, x9, [sp, #64]
    stp x10, x11, [sp, #80]
    stp x12, x13, [sp, #96]
    stp x14, x15, [sp, #112]
    stp x16, x17, [sp, #128]
    stp x18, x19, [sp, #144]
    stp x29, x30, [sp, #160]

    bl irq_handler

    ldp x29, x30, [sp, #160]
    ldp x18, x19, [sp, #144]
    ldp x16, x17, [sp, #128]
    ldp x14, x15, [sp, #112]
    ldp x12, x13, [sp, #96]
    ldp x10, x11, [sp, #80]
    ldp x8, x9, [sp, #64]
    ldp x6, x7, [sp, #48]
    ldp x4, x5, [sp, #32]
    ldp x2, x3, [sp, #16]
    ldp x0, x1, [sp, #0]
    add sp, sp, #256
    eret

    .align 7
    b .             // 0x300: FIQ
    .align 7
    b .             // 0x380: SError

    // --- Set 3: Lower EL using AArch64 (Exceptions from EL0) ---
    .align 7
    b .             // 0x400
    .align 7
    b .             // 0x480
    .align 7
    b .             // 0x500
    .align 7
    b .             // 0x580

    // --- Set 4: Lower EL using AArch32 (Not used) ---
    .align 7
    b .             // 0x600
    .align 7
    b .             // 0x680
    .align 7
    b .             // 0x700
    .align 7
    b .             // 0x780
