# PwnZero 原理图设计文档

## 核心连接

### 1. Pi Zero 2W GPIO 分配

```
Pi Zero 2W (40-pin Header)
============================

3.3V Power Rail:
├─ Pin 1, 17  → CC1101 TX VCC
├─ Pin 1, 17  → CC1101 RX VCC
├─ Pin 1      → OLED VCC
├─ Pin 1      → VS1838B VCC
└─ 滤波电容: 10uF + 100nF (每个 CC1101)

5V Power Rail:
├─ Pin 2, 4   → PN532 VCC
└─ 来自 PiSugar 3

GND:
└─ Pin 6, 9, 14, 20, 25, 30, 34, 39 → 所有模块 GND
```

### 2. I2C 总线 (共用)

```
I2C Bus (GPIO 2, 3)
===================
Pi Zero Pin 3 (SDA) ──┬── OLED SDA
                      └── PN532 SDA

Pi Zero Pin 5 (SCL) ──┬── OLED SCL
                      └── PN532 SCL

地址分配:
- OLED:  0x3C
- PN532: 0x24
```

### 3. SPI 总线 (CC1101 双模块)

```
SPI Bus (GPIO 9, 10, 11)
========================
Pi Zero Pin 19 (MOSI) ──┬── CC1101 TX MOSI
                        └── CC1101 RX MOSI

Pi Zero Pin 21 (MISO) ──┬── CC1101 TX MISO
                        └── CC1101 RX MISO

Pi Zero Pin 23 (SCLK) ──┬── CC1101 TX SCK
                        └── CC1101 RX SCK

片选 (独立):
- Pin 24 (GPIO 8)  → CC1101 TX CS
- Pin 26 (GPIO 7)  → CC1101 RX CS

数据引脚:
- Pin 33 (GPIO 13) → CC1101 TX GDO0
- Pin 35 (GPIO 19) → CC1101 RX GDO0
- Pin 37 (GPIO 26) → CC1101 RX GDO2
```

### 4. 红外模块

```
IR Module
=========
Pin 29 (GPIO 5) ──[330Ω]── IR LED 940nm (+) ── GND (-)
Pin 31 (GPIO 6) ────────── VS1838B OUT
                           VS1838B VCC ── 3.3V
                           VS1838B GND ── GND
```

### 5. 五向按键

```
5-Way Joystick
==============
Pin 11 (GPIO 17) ── UP    ──┐
Pin 13 (GPIO 27) ── DOWN  ──┤
Pin 15 (GPIO 22) ── LEFT  ──┼── COM ── GND
Pin 16 (GPIO 23) ── RIGHT ──┤
Pin 18 (GPIO 24) ── CENTER──┘

注：内部上拉已启用，无需外接电阻
```

### 6. 状态 LED

```
Status LEDs
===========
Pin 32 (GPIO 12) ──[330Ω]── LED 红 (+) ── GND (-)
Pin 36 (GPIO 16) ──[330Ω]── LED 黄 (+) ── GND (-)
Pin 38 (GPIO 20) ──[330Ω]── LED 绿 (+) ── GND (-)
```

## 电源滤波电路

### CC1101 电源滤波（每个模块）

```
3.3V ──┬──[10uF]──┬── GND
       └──[100nF]─┘

位置：紧靠 CC1101 VCC/GND 引脚
```

## 物料清单 (BOM)

| 编号 | 名称 | 数量 | 封装 | 备注 |
|------|------|------|------|------|
| U1 | Pi Zero 2W | 1 | 40pin | 主控 |
| U2 | CC1101 TX | 1 | 8pin | Sub-GHz |
| U3 | CC1101 RX | 1 | 8pin | Sub-GHz |
| U4 | PN532 | 1 | 8pin | NFC |
| U5 | SH1106 OLED | 1 | 4pin | 显示 |
| U6 | VS1838B | 1 | TO-92 | IR接收 |
| SW1 | 五向摇杆 | 1 | - | 按键 |
| D1 | IR LED 940nm | 1 | Φ5mm | IR发射 |
| D2 | LED 红 | 1 | Φ5mm | 状态灯 |
| D3 | LED 黄 | 1 | Φ5mm | 状态灯 |
| D4 | LED 绿 | 1 | Φ5mm | 状态灯 |
| R1-R4 | 330Ω | 4 | 0805 | LED限流 |
| C1-C2 | 10uF | 2 | 0805 | 滤波 |
| C3-C4 | 100nF | 2 | 0805 | 滤波 |






