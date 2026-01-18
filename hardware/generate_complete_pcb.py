#!/usr/bin/env python3
"""
PwnZero - 自动生成完整PCB
使用KiCad Python API自动创建包含元器件、封装、布线的完整PCB

使用方法：
1. 安装KiCad 7.0+
2. 运行: python generate_complete_pcb.py
3. 生成的文件: pwnzero_auto.kicad_pcb

依赖：
- KiCad 7.0+ (包含pcbnew Python模块)
"""

import sys
import os

try:
    import pcbnew
except ImportError:
    print("错误: 无法导入pcbnew模块")
    print("请确保已安装KiCad 7.0+")
    print("Windows: 将KiCad的bin目录添加到PATH")
    print("Linux: sudo apt install kicad python3-pcbnew")
    sys.exit(1)

# ============================================
# PCB基本参数
# ============================================

PCB_WIDTH = 85.6  # mm
PCB_HEIGHT = 53.98  # mm
PCB_THICKNESS = 1.6  # mm

# 板框坐标
BOARD_OUTLINE = [
    (0, 0),
    (PCB_WIDTH, 0),
    (PCB_WIDTH, PCB_HEIGHT),
    (0, PCB_HEIGHT),
    (0, 0)
]

# 安装孔位置 (M2.5)
MOUNTING_HOLES = [
    (5, 5),
    (80.6, 5),
    (5, 48.98),
    (80.6, 48.98)
]

print("=" * 60)
print("PwnZero PCB 自动生成脚本")
print("=" * 60)
print(f"PCB尺寸: {PCB_WIDTH}mm x {PCB_HEIGHT}mm")
print(f"层数: 2层")
print(f"板厚: {PCB_THICKNESS}mm")
print("=" * 60)

# ============================================
# 元器件定义
# ============================================

# 顶层元器件
TOP_COMPONENTS = {
    "U5": {
        "footprint": "Display:OLED_128x64_I2C",
        "x": 31, "y": 16, "rotation": 0,
        "value": "SH1106_OLED"
    },
    "SW1": {
        "footprint": "Button_Switch_THT:SW_PUSH_6mm",
        "x": 60, "y": 27, "rotation": 0,
        "value": "Joystick_5Way"
    },
    "D2": {
        "footprint": "LED_THT:LED_D5.0mm",
        "x": 78, "y": 5, "rotation": 0,
        "value": "LED_Red"
    },
    "D3": {
        "footprint": "LED_THT:LED_D5.0mm",
        "x": 78, "y": 13, "rotation": 0,
        "value": "LED_Yellow"
    },
    "D4": {
        "footprint": "LED_THT:LED_D5.0mm",
        "x": 78, "y": 21, "rotation": 0,
        "value": "LED_Green"
    },
}

# 底层元器件
BOTTOM_COMPONENTS = {
    "U1": {
        "footprint": "Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical",
        "x": 42.8, "y": 27, "rotation": 0,
        "value": "RPi_Zero_2W"
    },
    "U2": {
        "footprint": "RF_Module:CC1101_Module",
        "x": 11, "y": 14, "rotation": 0,
        "value": "CC1101_TX"
    },
    "U3": {
        "footprint": "RF_Module:CC1101_Module",
        "x": 11, "y": 41, "rotation": 0,
        "value": "CC1101_RX"
    },
    "U4": {
        "footprint": "RF_Module:PN532_Module",
        "x": 45, "y": 27, "rotation": 0,
        "value": "PN532"
    },
    "U6": {
        "footprint": "OptoDevice:Vishay_MOLD-3Pin",
        "x": 78, "y": 10, "rotation": 180,
        "value": "VS1838B"
    },
    "D1": {
        "footprint": "LED_THT:LED_D5.0mm",
        "x": 78, "y": 35, "rotation": 180,
        "value": "IR_LED_940nm"
    },
    "R1": {
        "footprint": "Resistor_SMD:R_0805_2012Metric",
        "x": 75, "y": 35, "rotation": 90,
        "value": "330"
    },
    "R2": {
        "footprint": "Resistor_SMD:R_0805_2012Metric",
        "x": 75, "y": 5, "rotation": 90,
        "value": "330"
    },
    "R3": {
        "footprint": "Resistor_SMD:R_0805_2012Metric",
        "x": 75, "y": 13, "rotation": 90,
        "value": "330"
    },
    "R4": {
        "footprint": "Resistor_SMD:R_0805_2012Metric",
        "x": 75, "y": 21, "rotation": 90,
        "value": "330"
    },
    "C1": {
        "footprint": "Capacitor_SMD:C_0805_2012Metric",
        "x": 8, "y": 11, "rotation": 0,
        "value": "10uF"
    },
    "C2": {
        "footprint": "Capacitor_SMD:C_0805_2012Metric",
        "x": 8, "y": 8, "rotation": 0,
        "value": "100nF"
    },
    "C3": {
        "footprint": "Capacitor_SMD:C_0805_2012Metric",
        "x": 8, "y": 38, "rotation": 0,
        "value": "10uF"
    },
    "C4": {
        "footprint": "Capacitor_SMD:C_0805_2012Metric",
        "x": 8, "y": 35, "rotation": 0,
        "value": "100nF"
    },
}

# ============================================
# 网络连接定义
# ============================================

NETS = {
    "GND": {"tracks": [], "width": 0.6},
    "+3V3": {"tracks": [], "width": 0.5},
    "+5V": {"tracks": [], "width": 0.6},
    "I2C_SDA": {"tracks": [], "width": 0.3},
    "I2C_SCL": {"tracks": [], "width": 0.3},
    "SPI_MOSI": {"tracks": [], "width": 0.3},
    "SPI_MISO": {"tracks": [], "width": 0.3},
    "SPI_SCLK": {"tracks": [], "width": 0.3},
    "CC1101_TX_CS": {"tracks": [], "width": 0.25},
    "CC1101_RX_CS": {"tracks": [], "width": 0.25},
    "GPIO5_IR_TX": {"tracks": [], "width": 0.25},
    "GPIO6_IR_RX": {"tracks": [], "width": 0.25},
    "GPIO12_LED_RED": {"tracks": [], "width": 0.25},
    "GPIO16_LED_YELLOW": {"tracks": [], "width": 0.25},
    "GPIO20_LED_GREEN": {"tracks": [], "width": 0.25},
}

# ============================================
# 辅助函数
# ============================================

def mm_to_nm(mm):
    """毫米转纳米（KiCad内部单位）"""
    return int(mm * 1000000)

def create_board():
    """创建PCB板对象"""
    print("\n[1/7] 创建PCB板对象...")
    board = pcbnew.BOARD()

    # 设置板子属性
    board.SetDesignSettings(pcbnew.BOARD_DESIGN_SETTINGS())
    design_settings = board.GetDesignSettings()
    design_settings.SetCopperLayerCount(2)

    print("  ✓ PCB板对象创建成功")
    return board

def draw_board_outline(board):
    """绘制板框"""
    print("\n[2/7] 绘制板框...")

    edge_layer = pcbnew.Edge_Cuts

    for i in range(len(BOARD_OUTLINE) - 1):
        x1, y1 = BOARD_OUTLINE[i]
        x2, y2 = BOARD_OUTLINE[i + 1]

        segment = pcbnew.PCB_SHAPE(board)
        segment.SetShape(pcbnew.SHAPE_T_SEGMENT)
        segment.SetLayer(edge_layer)
        segment.SetStart(pcbnew.VECTOR2I(mm_to_nm(x1), mm_to_nm(y1)))
        segment.SetEnd(pcbnew.VECTOR2I(mm_to_nm(x2), mm_to_nm(y2)))
        segment.SetWidth(mm_to_nm(0.1))
        board.Add(segment)

    print(f"  ✓ 板框绘制完成: {PCB_WIDTH}mm x {PCB_HEIGHT}mm")

def add_mounting_holes(board):
    """添加安装孔"""
    print("\n[3/7] 添加安装孔...")

    for i, (x, y) in enumerate(MOUNTING_HOLES):
        pad = pcbnew.PAD(board)
        pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
        pad.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
        pad.SetLayerSet(pad.UnplatedHoleMask())
        pad.SetDrillSize(pcbnew.VECTOR2I(mm_to_nm(2.7), mm_to_nm(2.7)))
        pad.SetSize(pcbnew.VECTOR2I(mm_to_nm(2.7), mm_to_nm(2.7)))
        pad.SetPosition(pcbnew.VECTOR2I(mm_to_nm(x), mm_to_nm(y)))
        board.Add(pad)

    print(f"  ✓ 添加了 {len(MOUNTING_HOLES)} 个安装孔 (M2.5)")

def add_components(board):
    """添加元器件"""
    print("\n[4/7] 添加元器件...")

    component_count = 0

    # 添加顶层元器件
    for ref, comp_data in TOP_COMPONENTS.items():
        try:
            footprint = pcbnew.FootprintLoad("", comp_data["footprint"])
            if footprint:
                footprint.SetReference(ref)
                footprint.SetValue(comp_data["value"])
                footprint.SetPosition(pcbnew.VECTOR2I(
                    mm_to_nm(comp_data["x"]),
                    mm_to_nm(comp_data["y"])
                ))
                footprint.SetOrientation(pcbnew.EDA_ANGLE(comp_data["rotation"], pcbnew.DEGREES_T))
                footprint.SetLayer(pcbnew.F_Cu)
                board.Add(footprint)
                component_count += 1
        except Exception as e:
            print(f"  ⚠ 警告: 无法加载 {ref} 的封装 {comp_data['footprint']}")

    # 添加底层元器件
    for ref, comp_data in BOTTOM_COMPONENTS.items():
        try:
            footprint = pcbnew.FootprintLoad("", comp_data["footprint"])
            if footprint:
                footprint.SetReference(ref)
                footprint.SetValue(comp_data["value"])
                footprint.SetPosition(pcbnew.VECTOR2I(
                    mm_to_nm(comp_data["x"]),
                    mm_to_nm(comp_data["y"])
                ))
                footprint.SetOrientation(pcbnew.EDA_ANGLE(comp_data["rotation"], pcbnew.DEGREES_T))
                footprint.SetLayer(pcbnew.B_Cu)
                board.Add(footprint)
                component_count += 1
        except Exception as e:
            print(f"  ⚠ 警告: 无法加载 {ref} 的封装 {comp_data['footprint']}")

    print(f"  ✓ 添加了 {component_count} 个元器件")

def create_nets(board):
    """创建网络"""
    print("\n[5/7] 创建网络...")

    net_count = 0
    for net_name in NETS.keys():
        net = pcbnew.NETINFO_ITEM(board, net_name)
        board.Add(net)
        net_count += 1

    print(f"  ✓ 创建了 {net_count} 个网络")

def add_simple_routing(board):
    """添加简单布线（示例）"""
    print("\n[6/7] 添加布线...")
    print("  ⚠ 注意: 自动布线功能有限，建议在KiCad中手动完善")

    # 这里只添加一些示例走线
    # 实际的完整布线需要在KiCad GUI中完成
    track_count = 0

    # 示例：添加一条电源走线
    try:
        track = pcbnew.PCB_TRACK(board)
        track.SetStart(pcbnew.VECTOR2I(mm_to_nm(10), mm_to_nm(10)))
        track.SetEnd(pcbnew.VECTOR2I(mm_to_nm(20), mm_to_nm(10)))
        track.SetWidth(mm_to_nm(0.5))
        track.SetLayer(pcbnew.F_Cu)
        board.Add(track)
        track_count += 1
    except:
        pass

    print(f"  ✓ 添加了 {track_count} 条示例走线")
    print("  → 请在KiCad中打开文件并完成完整布线")

def save_board(board, filename):
    """保存PCB文件"""
    print(f"\n[7/7] 保存PCB文件...")

    try:
        board.Save(filename)
        print(f"  ✓ PCB文件已保存: {filename}")
        return True
    except Exception as e:
        print(f"  ✗ 保存失败: {e}")
        return False

# ============================================
# 主函数
# ============================================

def main():
    """主函数"""
    print("\n开始生成PCB...")

    # 1. 创建PCB板
    board = create_board()

    # 2. 绘制板框
    draw_board_outline(board)

    # 3. 添加安装孔
    add_mounting_holes(board)

    # 4. 添加元器件
    add_components(board)

    # 5. 创建网络
    create_nets(board)

    # 6. 添加布线
    add_simple_routing(board)

    # 7. 保存文件
    output_file = os.path.join(os.path.dirname(__file__), "pwnzero_auto.kicad_pcb")
    success = save_board(board, output_file)

    if success:
        print("\n" + "=" * 60)
        print("✓ PCB生成完成！")
        print("=" * 60)
        print(f"\n生成的文件: {output_file}")
        print("\n下一步:")
        print("1. 用KiCad打开 pwnzero_auto.kicad_pcb")
        print("2. 检查元器件位置")
        print("3. 完成布线（工具 → 布线 → 自动布线）")
        print("4. 铺铜（添加填充区域，网络选择GND）")
        print("5. DRC检查（工具 → 设计规则检查）")
        print("6. 生成Gerber文件（文件 → 制造输出 → Gerber）")
        print("=" * 60)
    else:
        print("\n✗ PCB生成失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
