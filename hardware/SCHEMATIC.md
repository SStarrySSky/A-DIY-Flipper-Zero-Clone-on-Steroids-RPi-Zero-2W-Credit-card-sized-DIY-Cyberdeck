# PwnZero 完整原理图设计文档

## 项目信息
- **版本：** v1.0
- **日期：** 2026-01-18
- **用途：** CTF/黑客马拉松比赛

---

## 核心模块清单

| 编号 | 组件 | 型号 | 数量 | 尺寸 (mm) |
|------|------|------|------|-----------|
| U1 | 主控 | Raspberry Pi Zero 2W | 1 | 65 x 30 |
| U2 | 电源 | PiSugar 3 (1200mAh) | 1 | 65 x 30 |
| U3 | Sub-GHz TX | AS07-M1101D-TH | 1 | 12.2 x 20.8 |
| U4 | Sub-GHz RX | AS07-M1101D-TH | 1 | 12.2 x 20.8 |
| U5 | NFC | PN532 | 1 | 40.4 x 42.7 |
| U6 | OLED | SH1106 1.3" | 1 | 35.4 x 33.5 |
| U7 | IR 接收 | VS1838B | 1 | 7.6 x 6.7 |
| SW1 | 五向按键 | 摇杆模块 | 1 | 30.2 x 26 |

---

## 被动元件清单

| 编号 | 元件 | 规格 | 数量 | 封装 | 用途 |
|------|------|------|------|------|------|
| R1 | 电阻 | 330Ω 1/4W | 1 | 0805 | IR LED 限流 |
| R2 | 电阻 | 330Ω 1/4W | 1 | 0805 | 红色 LED 限流 |
| R3 | 电阻 | 330Ω 1/4W | 1 | 0805 | 黄色 LED 限流 |
| R4 | 电阻 | 330Ω 1/4W | 1 | 0805 | 绿色 LED 限流 |
| C1 | 电容 | 10uF 16V | 1 | 0805 | CC1101 TX 电源滤波 |
| C2 | 电容 | 10uF 16V | 1 | 0805 | CC1101 RX 电源滤波 |
| C3 | 电容 | 100nF | 1 | 0603 | CC1101 TX 高频滤波 |
| C4 | 电容 | 100nF | 1 | 0603 | CC1101 RX 高频滤波 |
| D1 | LED | 5mm 红色 | 1 | LED-5mm | 状态指示 |
| D2 | LED | 5mm 黄色 | 1 | LED-5mm | 状态指示 |
| D3 | LED | 5mm 绿色 | 1 | LED-5mm | 状态指示 |
| D4 | IR LED | 940nm 5mm | 1 | LED-5mm | 红外发射 |

---

## 完整引脚连接表

### Pi Zero 2W GPIO 分配

| 物理Pin | BCM GPIO | 功能 | 连接到 |
|---------|----------|------|--------|
| 1 | 3.3V | 电源 | OLED VCC, CC1101 x2 VCC |
| 2 | 5V | 电源 | PN532 VCC |
| 3 | GPIO 2 | I2C SDA | OLED SDA, PN532 SDA |
| 5 | GPIO 3 | I2C SCL | OLED SCL, PN532 SCL |
| 6 | GND | 地 | 所有模块 GND |
| 11 | GPIO 17 | 按键 UP | 五向按键 UP |
| 13 | GPIO 27 | 按键 DOWN | 五向按键 DOWN |
| 15 | GPIO 22 | 按键 LEFT | 五向按键 LEFT |
| 16 | GPIO 23 | 按键 RIGHT | 五向按键 RIGHT |
| 18 | GPIO 24 | 按键 CENTER | 五向按键 CENTER |
| 19 | GPIO 10 | SPI MOSI | CC1101 TX/RX MOSI |
| 21 | GPIO 9 | SPI MISO | CC1101 TX/RX MISO |
| 23 | GPIO 11 | SPI SCLK | CC1101 TX/RX SCLK |
| 24 | GPIO 8 | SPI CS0 | CC1101 TX CSN |
| 26 | GPIO 7 | SPI CS1 | CC1101 RX CSN |
| 29 | GPIO 5 | IR TX | IR LED (+ R1 330Ω) |
| 31 | GPIO 6 | IR RX | VS1838B OUT |
| 32 | GPIO 12 | LED1 | 红色LED (+ R2 330Ω) |
| 33 | GPIO 13 | GDO0 | CC1101 TX GDO0 |
| 35 | GPIO 19 | GDO0 | CC1101 RX GDO0 |
| 36 | GPIO 16 | LED2 | 黄色LED (+ R3 330Ω) |
| 37 | GPIO 26 | GDO2 | CC1101 RX GDO2 |
| 38 | GPIO 20 | LED3 | 绿色LED (+ R4 330Ω) |

---

## 电路连接细节

### 1. CC1101 电源滤波电路

```
CC1101 TX:
3.3V ──┬──[C1: 10uF]──┬── GND
       └──[C3: 100nF]─┘

CC1101 RX:
3.3V ──┬──[C2: 10uF]──┬── GND
       └──[C4: 100nF]─┘
```

### 2. LED 限流电路

```
GPIO 5  ──[R1: 330Ω]──(+)D4 IR LED(-)── GND
GPIO 12 ──[R2: 330Ω]──(+)D1 红LED(-)── GND
GPIO 16 ──[R3: 330Ω]──(+)D2 黄LED(-)── GND
GPIO 20 ──[R4: 330Ω]──(+)D3 绿LED(-)── GND
```

### 3. I2C 总线共享

```
Pi Zero GPIO 2 (SDA) ──┬── OLED SDA
                       └── PN532 SDA

Pi Zero GPIO 3 (SCL) ──┬── OLED SCL
                       └── PN532 SCL
```

---

## 硬件在环仿真配置

### 仿真工具
- **Proteus** - 电路仿真
- **QEMU** - Pi Zero 系统仿真
- **Python unittest** - 软件单元测试

### 仿真步骤

1. **GPIO 模拟**
```python
# 在 config.py 中已实现
SIMULATION_MODE = not is_raspberry_pi()
```

2. **运行仿真**
```bash
python3 main.py  # 自动检测并进入仿真模式
```

3. **验证功能**
- 菜单导航
- LED 闪烁效果
- 模块初始化
- 信号录制/重放逻辑

---

## 注意事项

⚠️ **电压警告**
- CC1101 只能接 3.3V
- PN532 接 5V (模块自带稳压)
- 所有 LED 必须串联限流电阻

⚠️ **I2C 地址**
- OLED: 0x3C
- PN532: 0x24
- 确保无冲突

⚠️ **SPI 片选**
- CC1101 TX: GPIO 8
- CC1101 RX: GPIO 7
- 必须独立，不可共用

