# PwnZero PCB 完整设计指南

## 📐 PCB规格
- **尺寸**: 85.6mm x 53.98mm (信用卡尺寸)
- **层数**: 双层板
- **板厚**: 1.6mm
- **最小线宽**: 0.2mm
- **最小间距**: 0.2mm

## 🔧 元器件布局（详细坐标）

### 顶层 (Top Layer)

| 元器件 | 位号 | 坐标 (X, Y) mm | 旋转角度 | 说明 |
|--------|------|----------------|----------|------|
| OLED显示屏 | U5 | (31, 16) | 0° | SH1106 1.3寸 |
| 五向摇杆 | SW1 | (60, 27) | 0° | 带PCB底座 |
| LED红 | D2 | (78, 5) | 0° | 5mm直插 |
| LED黄 | D3 | (78, 13) | 0° | 5mm直插 |
| LED绿 | D4 | (78, 21) | 0° | 5mm直插 |

### 底层 (Bottom Layer)

| 元器件 | 位号 | 坐标 (X, Y) mm | 旋转角度 | 说明 |
|--------|------|----------------|----------|------|
| Pi Zero 2W | U1 | (42.8, 27) | 0° | 通过40针排针连接 |
| CC1101 TX | U2 | (11, 14) | 0° | Sub-GHz发射 |
| CC1101 RX | U3 | (11, 41) | 0° | Sub-GHz接收 |
| PN532 | U4 | (45, 27) | 0° | NFC模块 |
| IR接收 | U6 | (78, 10) | 180° | VS1838B |
| IR LED | D1 | (78, 35) | 180° | 940nm红外LED |
| 电阻 R1 | R1 | (75, 35) | 90° | 330Ω 0805 |
| 电阻 R2 | R2 | (75, 5) | 90° | 330Ω 0805 |
| 电阻 R3 | R3 | (75, 13) | 90° | 330Ω 0805 |
| 电阻 R4 | R4 | (75, 21) | 90° | 330Ω 0805 |
| 电容 C1 | C1 | (8, 11) | 0° | 10uF 0805 |
| 电容 C2 | C2 | (8, 8) | 0° | 100nF 0805 |
| 电容 C3 | C3 | (8, 38) | 0° | 10uF 0805 |
| 电容 C4 | C4 | (8, 35) | 0° | 100nF 0805 |


## 🔌 布线规则

### 电源网络

| 网络名 | 线宽 | 说明 |
|--------|------|------|
| GND | 铺铜 | 顶层和底层都铺地 |
| +3V3 | 0.5mm | 供电给CC1101、OLED、IR |
| +5V | 0.6mm | 供电给PN532 |

### 信号网络

| 网络名 | 线宽 | 说明 |
|--------|------|------|
| I2C_SDA | 0.3mm | OLED和PN532共用 |
| I2C_SCL | 0.3mm | OLED和PN532共用 |
| SPI_MOSI | 0.3mm | CC1101 TX和RX共用 |
| SPI_MISO | 0.3mm | CC1101 TX和RX共用 |
| SPI_SCLK | 0.3mm | CC1101 TX和RX共用 |
| 其他GPIO | 0.25mm | LED、IR、按键等 |


## 📋 详细连接表

### I2C总线连接

```
Pi Zero Pin 3 (GPIO2/SDA) ──┬── OLED SDA
                            └── PN532 SDA

Pi Zero Pin 5 (GPIO3/SCL) ──┬── OLED SCL
                            └── PN532 SCL
```

### SPI总线连接

```
Pi Zero Pin 19 (GPIO10/MOSI) ──┬── CC1101 TX MOSI
                               └── CC1101 RX MOSI

Pi Zero Pin 21 (GPIO9/MISO) ──┬── CC1101 TX MISO
                              └── CC1101 RX MISO

Pi Zero Pin 23 (GPIO11/SCLK) ──┬── CC1101 TX SCK
                               └── CC1101 RX SCK

Pi Zero Pin 24 (GPIO8) ── CC1101 TX CS
Pi Zero Pin 26 (GPIO7) ── CC1101 RX CS
```


### GPIO连接

```
GPIO5 (Pin 29) ──[R1 330Ω]── IR LED (+) ── GND (-)
GPIO6 (Pin 31) ── VS1838B OUT

GPIO12 (Pin 32) ──[R2 330Ω]── LED Red (+) ── GND (-)
GPIO16 (Pin 36) ──[R3 330Ω]── LED Yellow (+) ── GND (-)
GPIO20 (Pin 38) ──[R4 330Ω]── LED Green (+) ── GND (-)

GPIO17 (Pin 11) ── Joystick UP
GPIO27 (Pin 13) ── Joystick DOWN
GPIO22 (Pin 15) ── Joystick LEFT
GPIO23 (Pin 16) ── Joystick RIGHT
GPIO24 (Pin 18) ── Joystick CENTER
```


### 电源连接

```
3.3V Rail:
Pi Zero Pin 1, 17 ──┬── CC1101 TX VCC
                    ├── CC1101 RX VCC
                    ├── OLED VCC
                    ├── VS1838B VCC
                    ├── C1 (+)
                    ├── C2 (+)
                    ├── C3 (+)
                    └── C4 (+)

5V Rail:
Pi Zero Pin 2, 4 ── PN532 VCC

GND:
Pi Zero Pin 6,9,14,20,25,30,34,39 ── 所有模块GND
```


## 🏭 制造参数

### 嘉立创下单参数

```
板子尺寸: 85.6 x 53.98 mm
板子层数: 2层
板子厚度: 1.6mm
铜箔厚度: 1oz (35μm)
阻焊颜色: 黑色
字符颜色: 白色
表面处理: HASL无铅
最小线宽: 0.2mm
最小线距: 0.2mm
最小孔径: 0.3mm
```


## 🎯 立创EDA布线步骤

### 1. 导入网表
- 打开立创EDA
- 新建PCB项目
- 导入 `pwnzero.net` 网表文件

### 2. 设置板框
- 绘制板框：85.6mm x 53.98mm
- 添加4个安装孔（M2.5）

### 3. 放置元器件
- 参考上面的坐标表
- 顶层：OLED、摇杆、LED
- 底层：Pi Zero、CC1101、PN532、SMD元件


### 4. 设置布线规则
- 电源线：0.5-0.6mm
- 信号线：0.25-0.3mm
- 间距：≥0.2mm

### 5. 布线
- 先布电源线（粗线）
- 再布信号线（细线）
- 最后铺地铜

### 6. DRC检查
- 运行设计规则检查
- 修复所有错误

### 7. 生成Gerber
- 导出Gerber文件
- 直接下单到嘉立创

