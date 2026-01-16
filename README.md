#   DIY 多功能便携黑客工具
```text

________________________________________________________________________________
                                                                              
    _____                      ______                                         
   |  __ \                    |___  /                                         
   | |__) |_      ___ __   ____  / /  ___ _ __ ___                            
   |  ___/\ \ /\ / / '_ \ |_  / / /  / _ \ '__/ _ \                           
   | |     \ V  V /| | | | / / / /__|  __/ | | (_) |                          
   |_|      \_/\_/ |_| |_|/___/_____/\___|_|  \___/                           
                                                                              
   [ PwnZero Ultra: The Linux-Powered Toolkit ]                               
   [ Far more powerful than Flipper Zero — A True Portable Cyberdeck ]        
________________________________________________________________________________

> **Repository Description:**
> PwnZero Ultra: A DIY Flipper Zero Clone on Steroids. 
> A credit-card-sized, quad-core hacking powerhouse that redefines 
> portable hardware auditing. Built for pros who need more than a toy.
 [ Portable Linux-Based Hacking Multi-Tool ]
 [ Powered by RPi Zero 2W | Dual CC1101 | PN532 ]

> **基于 Raspberry Pi Zero 2W 的 Flipper Zero 开源替代方案**

---

## 免责声明

```
本项目仅供以下用途：
- CTF 竞赛 / 黑客马拉松比赛
- 授权的安全研究与渗透测试
- 教育学习目的

严禁用于任何非法目的！
使用者需自行承担法律责任。
```

---

## 快速导航

| 章节 | 内容 |
|------|------|
| [功能介绍](#功能介绍) | 设备能做什么 |
| [硬件清单](#硬件清单) | 需要购买的材料 |
| [硬件组装](#硬件组装) | 焊接与接线指南 |
| [软件安装](#软件安装) | 系统配置与部署 |
| [使用说明](#使用说明) | 各功能操作方法 |
| [3D外壳](#3d外壳) | 外壳打印指南 |
| [故障排除](#故障排除) | 常见问题解决 |

---

Why settle for a toy when you can carry a workstation? PwnZero isn't just a clone; it's a field-ready pentesting toolkit that fits in your credit-card slot. Built on the 64-bit architecture of Raspberry Pi Zero 2W, it redefines what a handheld hacking multi-tool can do.

## 功能介绍

### 硬件功能

| 模块 | 功能 | 应用场景 |
|------|------|----------|
| **Sub-GHz** | 433/315MHz 信号收发 | 无线门禁、遥控器分析 |
| **NFC** | 读取 NFC/RFID 卡片 | 门禁卡 UID 读取 |
| **Infrared** | 红外信号学习与发送 | 电视/空调遥控 |
| **OLED** | 128x64 显示屏 | 菜单界面显示 |
| **电池** | PiSugar 3 供电 | 便携使用 |

### 软件功能

| 功能 | 说明 |
|------|------|
| 信号录制 | 捕获 Sub-GHz 无线信号 |
| 信号重放 | 重放录制的信号 |
| RollJam 演示 | 滚动码攻击演示 (仅限授权测试) |
| NFC 读卡 | 读取卡片 UID/ATQA/SAK |
| IR 学习 | 学习红外遥控信号 |
| IR 发送 | 发送学习的红外信号 |
| 电量显示 | 实时显示电池电量 |

---

## 硬件清单

### 核心模块

| 组件 | 型号 | 数量 | 参考价格 |
|------|------|------|----------|
| 主控 | Raspberry Pi Zero 2 W | 1 | ~$15 |
| 电源 | PiSugar 3 (1200mAh) | 1 | ~$30 |
| 屏幕 | SH1106 1.3" OLED (I2C) | 1 | ~$5 |
| 无线电 | AS07-M1101D-TH (CC1101) | 2 | ~$6 |
| NFC | PN532 红色小方板 | 1 | ~$8 |
| IR接收 | VS1838B | 1 | ~$1 |
| IR发射 | 940nm LED | 1 | ~$0.5 |
| 按键 | 五向摇杆模块 (带PCB底座) | 1 | ~$2 |
| 状态灯 | 5mm LED (红/黄/绿) | 3 | ~$0.5 |
| 散热片 | 铝制 14x14mm | 1 | ~$1 |
| 摇杆帽 | 五向摇杆帽 | 1 | ~$1 |

### 电阻电容

| 组件 | 规格 | 数量 | 用途 |
|------|------|------|------|
| 电阻 | 330Ω 1/4W | 4 | IR LED + 3个状态灯限流 |
| 电阻 | 10KΩ 1/4W | 5 | 按键上拉 (备用) |
| 电容 | 10uF 16V | 2 | CC1101 电源滤波 |
| 电容 | 100nF (0.1uF) | 2 | CC1101 高频滤波 |

### 辅材

| 组件 | 规格 | 数量 | 用途 |
|------|------|------|------|
| 洞洞板 | 7x5cm 双面镀锡 | 2 | 主板 |
| 漆包线 | 0.5mm | 1卷 | 走线连接 |
| 电烙铁套装 | 含焊锡丝 | 1 | 焊接 |

### 总成本

约 **$70 / ¥350-400**

---

## 硬件组装

### 电压警告

```
⚠️ 重要！接错电压会烧毁模块！

CC1101: 只能接 3.3V (接5V会烧毁)
PN532:  接 5V (模块自带稳压，接3.3V电流不足)
OLED:   接 3.3V
IR:     接 3.3V
```

### GPIO 引脚分配表

| 模块 | 引脚 | GPIO | 物理Pin |
|------|------|------|---------|
| **SH1106 OLED** | | | |
| └ VCC | 3.3V | - | Pin 1 |
| └ GND | GND | - | Pin 9 |
| └ SDA | I2C数据 | GPIO 2 | Pin 3 |
| └ SCL | I2C时钟 | GPIO 3 | Pin 5 |
| **CC1101 TX** | | | |
| └ VCC | 3.3V | - | Pin 17 |
| └ GND | GND | - | Pin 20 |
| └ MOSI | SPI数据出 | GPIO 10 | Pin 19 |
| └ MISO | SPI数据入 | GPIO 9 | Pin 21 |
| └ SCK | SPI时钟 | GPIO 11 | Pin 23 |
| └ CSN | 片选 | GPIO 8 | Pin 24 |
| └ GDO0 | 数据IO | GPIO 13 | Pin 33 |
| **CC1101 RX** | | | |
| └ VCC | 3.3V | - | Pin 17 |
| └ GND | GND | - | Pin 25 |
| └ MOSI | SPI数据出 | GPIO 10 | Pin 19 |
| └ MISO | SPI数据入 | GPIO 9 | Pin 21 |
| └ SCK | SPI时钟 | GPIO 11 | Pin 23 |
| └ CSN | 片选 | GPIO 7 | Pin 26 |
| └ GDO0 | 数据IO | GPIO 19 | Pin 35 |
| └ GDO2 | 状态IO | GPIO 26 | Pin 37 |
| **PN532 NFC** | | | |
| └ VCC | 5V | - | Pin 2 |
| └ GND | GND | - | Pin 6 |
| └ SDA | I2C数据 | GPIO 2 | Pin 3 |
| └ SCL | I2C时钟 | GPIO 3 | Pin 5 |
| **IR 红外** | | | |
| └ TX (LED+330Ω) | 发射 | GPIO 5 | Pin 29 |
| └ RX (VS1838B) | 接收 | GPIO 6 | Pin 31 |
| **五向按键** | | | |
| └ UP | 上 | GPIO 17 | Pin 11 |
| └ DOWN | 下 | GPIO 27 | Pin 13 |
| └ LEFT | 左 | GPIO 22 | Pin 15 |
| └ RIGHT | 右 | GPIO 23 | Pin 16 |
| └ CENTER | 确认 | GPIO 24 | Pin 18 |
| └ COM | 公共端 | GND | Pin 14 |
| **状态 LED** | | | |
| └ LED1 (红+330Ω) | 状态灯1 | GPIO 12 | Pin 32 |
| └ LED2 (黄+330Ω) | 状态灯2 | GPIO 16 | Pin 36 |
| └ LED3 (绿+330Ω) | 状态灯3 | GPIO 20 | Pin 38 |

### 电容接线

```
CC1101 电源滤波 (每个模块都要接):

       ┌─[10uF]──┐
3.3V ──┼─[100nF]─┼── GND
       └─────────┘
```

### IR LED 接线

```
GPIO 5 ──[330Ω]──(+)IR LED(-)── GND
```

### 焊接顺序

1. 给 Pi Zero 焊排针（如果没有）
2. 测试 5V/3.3V 供电正常
3. 焊接 OLED，测试显示
4. 焊接五向按键，测试输入
5. 焊接 CC1101 x2，测试 SPI
6. 焊接 PN532，测试 I2C
7. 焊接 IR 收发，测试红外

### PN532 拨码开关设置

```
设置为 I2C 模式：
SEL0 = 1 (ON)
SEL1 = 0 (OFF)
```

---

## 软件安装

### 1. 系统准备

```bash
# 烧录 Raspberry Pi OS Lite 到 SD 卡
# 启用 SSH、WiFi（用 Raspberry Pi Imager）

# 首次启动后更新系统
sudo apt update && sudo apt upgrade -y
```

### 2. 启用接口

```bash
sudo raspi-config
# Interface Options -> 启用 SPI
# Interface Options -> 启用 I2C
```

### 3. 安装依赖

```bash
sudo apt install -y python3-pip pigpio libnfc-bin libnfc-dev
sudo pip3 install -r requirements.txt
```

### 4. 启动 pigpio 服务

```bash
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
```

### 5. 部署项目

```bash
# 克隆项目
git clone <项目地址> /home/pi/pihacker
cd /home/pi/pihacker

# 运行
sudo python3 main.py
```

### 6. 开机自启（可选）

```bash
sudo cp pihacker.service /etc/systemd/system/
sudo systemctl enable pihacker
```

---

## 使用说明

### 按键操作

| 按键 | 功能 |
|------|------|
| ↑ | 上移菜单 |
| ↓ | 下移菜单 |
| ← | 返回上级 |
| → | (保留) |
| ● | 确认选择 |

### 菜单结构

```
PiHacker
├── Sub-GHz
│   ├── Read Signal    (录制信号)
│   ├── Replay         (重放信号)
│   ├── RollJam Demo   (滚动码演示)
│   └── Set Frequency  (切换频率)
├── NFC
│   ├── Read Card      (读取卡片)
│   └── Emulate Card   (模拟卡片)
├── Infrared
│   ├── Universal Remote (学习遥控)
│   └── Send Power Off   (发送关机)
├── WiFi Tools
│   ├── Scan Networks  (扫描网络)
│   └── Deauth Demo    (断网演示)
└── System
    ├── Device Info    (设备信息)
    ├── Battery Info   (电池信息)
    ├── Reboot         (重启)
    └── Shutdown       (关机)
```

### Sub-GHz 使用

1. 选择 `Read Signal` 开始录制
2. 按下遥控器按钮
3. 录制完成后选择 `Replay` 重放

### NFC 使用

1. 选择 `Read Card`
2. 将卡片贴近 PN532 模块
3. 屏幕显示 UID 信息

### IR 使用

1. 选择 `Universal Remote` 进入学习模式
2. 对准设备按下遥控器
3. 学习完成后可发送信号

---

## 3D外壳

外壳模型文件：`case/pihacker_case.scad`

### 打印参数

| 参数 | 建议值 |
|------|--------|
| 层高 | 0.2mm |
| 填充 | 20% |
| 材料 | PLA |
| 支撑 | 需要 |

### 外壳尺寸

- 外尺寸：80 x 55 x 25 mm
- 壁厚：2mm
- 圆角：3mm

---

## 故障排除

| 问题 | 可能原因 | 解决方法 |
|------|----------|----------|
| OLED 不亮 | I2C 未启用 | `sudo raspi-config` 启用 I2C |
| OLED 不亮 | 接线错误 | 检查 SDA/SCL 是否接反 |
| CC1101 无响应 | SPI 未启用 | `sudo raspi-config` 启用 SPI |
| CC1101 无响应 | CS 引脚冲突 | 确认 TX/RX 用不同 CS |
| NFC 读不到卡 | 拨码开关错误 | 设置为 I2C 模式 |
| NFC 读不到卡 | 供电不足 | 改接 5V |
| IR 无反应 | pigpio 未启动 | `sudo systemctl start pigpiod` |
| 按键不灵 | 接线松动 | 检查焊点 |
| 系统死机 | 3.3V 过载 | PN532 改接 5V |

---

## 项目结构

```
pihacker/
├── main.py              # 主程序入口
├── config.py            # 引脚配置
├── display_manager.py   # OLED 显示管理
├── input_handler.py     # 按键输入处理
├── requirements.txt     # Python 依赖
├── pihacker.service     # systemd 服务
├── modules/
│   ├── subghz.py        # Sub-GHz 模块
│   ├── nfc.py           # NFC 模块
│   ├── infrared.py      # 红外模块
│   └── battery.py       # 电池管理
├── case/
│   └── pihacker_case.scad  # 3D外壳模型
└── README.md            # 本文档
```

---

## 许可证

本项目仅供教育和授权安全研究使用。

---

## 致谢

- Flipper Zero 项目提供的灵感
- Raspberry Pi 基金会
- 开源社区贡献者

---

**再次提醒：请仅在合法授权的场景下使用本设备！**

