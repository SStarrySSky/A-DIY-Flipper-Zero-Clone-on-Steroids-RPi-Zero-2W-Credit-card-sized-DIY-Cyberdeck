#!/usr/bin/env python3
"""
PwnZero - 立创EDA PCB自动生成脚本
生成完整的立创EDA JSON格式PCB文件，包含元器件、封装、布线
"""

import json
import math

# PCB基本参数
PCB_WIDTH = 85.6  # mm
PCB_HEIGHT = 53.98  # mm
LAYER_COUNT = 2

# 元器件坐标定义（顶层）
TOP_COMPONENTS = {
    "U5": {"name": "OLED_SH1106", "x": 31, "y": 16, "rotation": 0, "layer": "TopLayer"},
    "SW1": {"name": "Joystick_5Way", "x": 60, "y": 27, "rotation": 0, "layer": "TopLayer"},
    "D2": {"name": "LED_Red", "x": 78, "y": 5, "rotation": 0, "layer": "TopLayer"},
    "D3": {"name": "LED_Yellow", "x": 78, "y": 13, "rotation": 0, "layer": "TopLayer"},
    "D4": {"name": "LED_Green", "x": 78, "y": 21, "rotation": 0, "layer": "TopLayer"},
}

# 元器件坐标定义（底层）
BOTTOM_COMPONENTS = {
    "U1": {"name": "RPi_Zero_2W", "x": 42.8, "y": 27, "rotation": 0, "layer": "BottomLayer"},
    "U2": {"name": "CC1101_TX", "x": 11, "y": 14, "rotation": 0, "layer": "BottomLayer"},
    "U3": {"name": "CC1101_RX", "x": 11, "y": 41, "rotation": 0, "layer": "BottomLayer"},
    "U4": {"name": "PN532", "x": 45, "y": 27, "rotation": 0, "layer": "BottomLayer"},
    "U6": {"name": "VS1838B", "x": 78, "y": 10, "rotation": 180, "layer": "BottomLayer"},
    "D1": {"name": "IR_LED", "x": 78, "y": 35, "rotation": 180, "layer": "BottomLayer"},
    "R1": {"name": "R_330", "x": 75, "y": 35, "rotation": 90, "layer": "BottomLayer"},
    "R2": {"name": "R_330", "x": 75, "y": 5, "rotation": 90, "layer": "BottomLayer"},
    "R3": {"name": "R_330", "x": 75, "y": 13, "rotation": 90, "layer": "BottomLayer"},
    "R4": {"name": "R_330", "x": 75, "y": 21, "rotation": 90, "layer": "BottomLayer"},
    "C1": {"name": "C_10uF", "x": 8, "y": 11, "rotation": 0, "layer": "BottomLayer"},
    "C2": {"name": "C_100nF", "x": 8, "y": 8, "rotation": 0, "layer": "BottomLayer"},
    "C3": {"name": "C_10uF", "x": 8, "y": 38, "rotation": 0, "layer": "BottomLayer"},
    "C4": {"name": "C_100nF", "x": 8, "y": 35, "rotation": 0, "layer": "BottomLayer"},
}

# 网络连接定义
NETS = {
    "GND": [],
    "+3V3": [],
    "+5V": [],
    "I2C_SDA": [("U1", "GPIO2"), ("U4", "SDA"), ("U5", "SDA")],
    "I2C_SCL": [("U1", "GPIO3"), ("U4", "SCL"), ("U5", "SCL")],
    "SPI_MOSI": [("U1", "GPIO10"), ("U2", "MOSI"), ("U3", "MOSI")],
    "SPI_MISO": [("U1", "GPIO9"), ("U2", "MISO"), ("U3", "MISO")],
    "SPI_SCLK": [("U1", "GPIO11"), ("U2", "SCK"), ("U3", "SCK")],
    "CC1101_TX_CS": [("U1", "GPIO8"), ("U2", "CS")],
    "CC1101_RX_CS": [("U1", "GPIO7"), ("U3", "CS")],
    "GPIO5_IR_TX": [("U1", "GPIO5"), ("R1", "1")],
    "GPIO6_IR_RX": [("U1", "GPIO6"), ("U6", "OUT")],
    "GPIO12_LED_RED": [("U1", "GPIO12"), ("R2", "1")],
    "GPIO16_LED_YELLOW": [("U1", "GPIO16"), ("R3", "1")],
    "GPIO20_LED_GREEN": [("U1", "GPIO20"), ("R4", "1")],
}

def mm_to_mil(mm):
    """毫米转密尔（立创EDA使用密尔作为单位）"""
    return mm * 39.3701

def generate_board_outline():
    """生成板框"""
    width_mil = mm_to_mil(PCB_WIDTH)
    height_mil = mm_to_mil(PCB_HEIGHT)

    outline = {
        "gge": "TRACK",
        "layerid": "19",  # Board Outline layer
        "net": "",
        "pointArr": [
            {"x": 0, "y": 0},
            {"x": width_mil, "y": 0},
            {"x": width_mil, "y": height_mil},
            {"x": 0, "y": height_mil},
            {"x": 0, "y": 0}
        ],
        "strokeWidth": 1
    }
    return outline

def generate_mounting_holes():
    """生成安装孔"""
    holes = []
    positions = [
        (5, 5),
        (80.6, 5),
        (5, 48.98),
        (80.6, 48.98)
    ]

    for i, (x, y) in enumerate(positions):
        hole = {
            "gge": "PAD",
            "layerid": "11",
            "net": "",
            "x": mm_to_mil(x),
            "y": mm_to_mil(y),
            "width": mm_to_mil(2.7),
            "height": mm_to_mil(2.7),
            "holeR": mm_to_mil(2.7),
            "shape": "ROUND",
            "id": f"H{i+1}"
        }
        holes.append(hole)

    return holes

def generate_component_footprint(ref, comp_data):
    """生成元器件封装"""
    x_mil = mm_to_mil(comp_data["x"])
    y_mil = mm_to_mil(comp_data["y"])

    footprint = {
        "gge": "LIB",
        "layerid": "1" if comp_data["layer"] == "TopLayer" else "2",
        "x": x_mil,
        "y": y_mil,
        "rotation": comp_data["rotation"],
        "id": ref,
        "name": comp_data["name"],
        "pads": []
    }

    return footprint

print("正在生成立创EDA PCB文件...")
print("第1部分：基础结构")
