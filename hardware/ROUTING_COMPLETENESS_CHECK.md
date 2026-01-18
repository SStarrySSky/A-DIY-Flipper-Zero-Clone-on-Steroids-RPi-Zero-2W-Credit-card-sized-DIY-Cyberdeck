# PwnZero 走线完整性检查

## 需要的所有连接

### Pi Zero 2W GPIO引脚分配

根据PCB_COMPLETE_DESIGN.md，需要以下连接：

**电源:**
- Pin 1, 17: 3.3V → CC1101 TX/RX, OLED, VS1838B, 电容
- Pin 2, 4: 5V → PN532
- Pin 6,9,14,20,25,30,34,39: GND → 所有模块

**I2C (OLED + PN532):**
- Pin 3 (GPIO2/SDA) → OLED SDA, PN532 SDA
- Pin 5 (GPIO3/SCL) → OLED SCL, PN532 SCL

**SPI (CC1101 TX + RX):**
- Pin 19 (GPIO10/MOSI) → CC1101 TX MOSI, CC1101 RX MOSI
- Pin 21 (GPIO9/MISO) → CC1101 TX MISO, CC1101 RX MISO
- Pin 23 (GPIO11/SCLK) → CC1101 TX SCK, CC1101 RX SCK
- Pin 24 (GPIO8) → CC1101 TX CS
- Pin 26 (GPIO7) → CC1101 RX CS

**GPIO (LED控制):**
- Pin 29 (GPIO5) → R1 → IR LED
- Pin 31 (GPIO6) → VS1838B OUT
- Pin 32 (GPIO12) → R2 → LED Red
- Pin 36 (GPIO16) → R3 → LED Yellow
- Pin 38 (GPIO20) → R4 → LED Green

**GPIO (摇杆):**
- Pin 11 (GPIO17) → Joystick UP
- Pin 13 (GPIO27) → Joystick DOWN
- Pin 15 (GPIO22) → Joystick LEFT
- Pin 16 (GPIO23) → Joystick RIGHT
- Pin 18 (GPIO24) → Joystick CENTER

---

## 当前PCB中的连接状态

### ✅ 已连接的网络 (25个)

1. GND (net 1) - 铺铜 ✅
2. +3V3 (net 2) - 部分连接 ⚠️
3. +5V (net 3) - 已连接 ✅
4. I2C_SDA (net 4) - 已连接 ✅
5. I2C_SCL (net 5) - 已连接 ✅
6. SPI_MOSI (net 6) - 已连接 ✅
7. SPI_MISO (net 7) - 需要检查 ⚠️
8. SPI_SCLK (net 8) - 需要检查 ⚠️
9. CC1101_TX_CS (net 9) - 需要检查 ⚠️
10. CC1101_RX_CS (net 10) - 需要检查 ⚠️
11. GPIO5_IR_TX (net 11) - 已连接 ✅
12. GPIO6_IR_RX (net 12) - 已连接 ✅
13. GPIO12_LED_RED (net 13) - 已连接 ✅
14. GPIO16_LED_YELLOW (net 14) - 已连接 ✅
15. GPIO20_LED_GREEN (net 15) - 已连接 ✅
16. GPIO17_JOY_UP (net 16) - 已连接 ✅
17. GPIO27_JOY_DOWN (net 17) - 已连接 ✅
18. GPIO22_JOY_LEFT (net 18) - 已连接 ✅
19. GPIO23_JOY_RIGHT (net 19) - 已连接 ✅
20. GPIO24_JOY_CENTER (net 20) - 已连接 ✅
21. LED_IR_ANODE (net 21) - 已连接 ✅
22. LED_RED_ANODE (net 22) - 已连接 ✅
23. LED_YELLOW_ANODE (net 23) - 已连接 ✅
24. LED_GREEN_ANODE (net 24) - 已连接 ✅

---

## ❌ 发现的问题

### 1. Pi Zero GPIO引脚未定义

**严重问题**: J1 (Pi Zero排母) 只定义了6个引脚！

当前PCB中：
```
pad "1" → +3V3
pad "2" → +5V
pad "3" → I2C_SDA
pad "4" → +5V
pad "5" → I2C_SCL
pad "6" → GND
```

**缺失的引脚**: 34个引脚未定义！

需要添加：
- Pin 11 (GPIO17) - 摇杆UP
- Pin 13 (GPIO27) - 摇杆DOWN
- Pin 15 (GPIO22) - 摇杆LEFT
- Pin 16 (GPIO23) - 摇杆RIGHT
- Pin 18 (GPIO24) - 摇杆CENTER
- Pin 19 (GPIO10) - SPI MOSI
- Pin 21 (GPIO9) - SPI MISO
- Pin 23 (GPIO11) - SPI SCLK
- Pin 24 (GPIO8) - CC1101 TX CS
- Pin 26 (GPIO7) - CC1101 RX CS
- Pin 29 (GPIO5) - IR TX
- Pin 31 (GPIO6) - IR RX
- Pin 32 (GPIO12) - LED Red
- Pin 36 (GPIO16) - LED Yellow
- Pin 38 (GPIO20) - LED Green
- 更多GND和电源引脚

### 2. SPI走线不完整

当前只有MOSI走线，缺少：
- MISO走线到Pi Zero
- SCLK走线到Pi Zero
- CS走线到Pi Zero

### 3. +3V3电源分配不完整

需要连接到：
- CC1101 TX VCC
- CC1101 RX VCC
- OLED VCC
- VS1838B VCC
- 所有滤波电容

---

## 🔧 需要修复的内容

### 优先级1: 添加Pi Zero完整引脚定义
- 添加40个引脚的完整定义
- 正确映射GPIO到网络

### 优先级2: 完善SPI走线
- 添加MISO走线
- 添加SCLK走线
- 添加CS走线

### 优先级3: 完善电源走线
- +3V3到所有模块
- GND到所有模块

### 优先级4: 优化走线样式
- 使用45度角拐弯
- 避免直角拐弯
- 减少走线交叉
