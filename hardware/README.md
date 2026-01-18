# PwnZero PCB 自动生成工具

## 📋 概述

本工具使用Python脚本自动生成完整的KiCad PCB文件，包含：
- ✅ 板框 (85.6mm x 53.98mm)
- ✅ 安装孔 (4个M2.5)
- ✅ 所有元器件及封装
- ✅ 网络定义
- ⚠️ 基础布线（需要在KiCad中完善）

---

## 🚀 快速开始

### 方法一：使用Python脚本自动生成（推荐）

#### 1. 安装依赖

**Windows:**
```bash
# 下载并安装KiCad 7.0+
# https://www.kicad.org/download/

# 将KiCad的bin目录添加到PATH
# 例如: C:\Program Files\KiCad\7.0\bin
```

**Linux:**
```bash
sudo apt update
sudo apt install kicad python3-pcbnew
```

**macOS:**
```bash
brew install kicad
```

#### 2. 运行脚本

```bash
cd hardware
python generate_complete_pcb.py
```

#### 3. 打开生成的PCB

```bash
# 生成的文件: pwnzero_auto.kicad_pcb
# 用KiCad打开即可
```

---

## 📁 文件说明

| 文件 | 说明 | 用途 |
|------|------|------|
| `generate_complete_pcb.py` | Python自动生成脚本 | 生成完整PCB |
| `pwnzero.net` | 网表文件 | 导入立创EDA |
| `pwnzero_bom.csv` | BOM清单 | 元器件采购 |
| `PCB_COMPLETE_DESIGN.md` | 完整设计文档 | 参考资料 |
| `JLCPCB_EDA_IMPORT_GUIDE.md` | 立创EDA导入指南 | 使用立创EDA |

---

## 🔧 方法二：使用立创EDA（在线）

如果不想安装KiCad，可以使用立创EDA在线工具：

### 步骤：

1. **打开立创EDA**
   - 访问 https://lceda.cn/
   - 注册并登录

2. **导入网表**
   - 新建PCB项目
   - 文件 → 导入 → 网表文件
   - 选择 `pwnzero.net`

3. **导入BOM**
   - 工具 → BOM → 导入BOM
   - 选择 `pwnzero_bom.csv`

4. **完成设计**
   - 参考 `JLCPCB_EDA_IMPORT_GUIDE.md` 完成布线
   - 直接下单到嘉立创

详细步骤请查看: `JLCPCB_EDA_IMPORT_GUIDE.md`

---

## 📊 PCB规格

```
尺寸: 85.6mm x 53.98mm (信用卡尺寸)
层数: 2层
板厚: 1.6mm
铜厚: 1oz (35μm)
最小线宽: 0.2mm
最小间距: 0.2mm
阻焊颜色: 黑色（推荐）
字符颜色: 白色
表面处理: HASL无铅
```

---

## 🎯 元器件清单

### 主要模块
- Raspberry Pi Zero 2W x1
- CC1101 Sub-GHz模块 x2 (TX/RX)
- PN532 NFC模块 x1
- SH1106 OLED显示屏 1.3寸 x1
- VS1838B 红外接收器 x1
- 940nm 红外LED x1
- 五向摇杆 x1

### 辅助元件
- 5mm LED (红/黄/绿) x3
- 330Ω 电阻 0805 x4
- 10uF 电容 0805 x2
- 100nF 电容 0805 x2

完整BOM请查看: `pwnzero_bom.csv`

---

## ⚙️ 下一步操作

### 在KiCad中完善PCB

1. **打开文件**
   ```
   用KiCad打开 pwnzero_auto.kicad_pcb
   ```

2. **检查元器件**
   - 确认所有元器件位置正确
   - 调整有冲突的元器件

3. **完成布线**
   - 工具 → 布线 → 自动布线
   - 或手动布线

4. **铺铜**
   - 添加填充区域
   - 网络选择: GND
   - 顶层和底层都铺地

5. **DRC检查**
   - 工具 → 设计规则检查
   - 修复所有错误

6. **生成Gerber**
   - 文件 → 制造输出 → Gerber
   - 压缩成ZIP文件

7. **下单制造**
   - 上传到嘉立创/华秋等PCB厂商
   - 选择参数并下单

---

## 🐛 常见问题

### Q1: 运行脚本报错 "无法导入pcbnew模块"
**A:**
- 确保已安装KiCad 7.0+
- Windows: 将KiCad的bin目录添加到PATH
- Linux: `sudo apt install python3-pcbnew`

### Q2: 元器件封装加载失败
**A:**
- 脚本会跳过无法加载的封装
- 在KiCad中手动添加缺失的元器件
- 或使用立创EDA导入网表

### Q3: 如何修改元器件位置？
**A:**
- 编辑 `generate_complete_pcb.py`
- 修改 `TOP_COMPONENTS` 或 `BOTTOM_COMPONENTS` 中的坐标
- 重新运行脚本

### Q4: 自动布线效果不好？
**A:**
- 脚本只生成基础结构
- 建议在KiCad中手动布线
- 或使用立创EDA的智能布线功能

---

## 📞 技术支持

- **项目文档**: 查看 `PCB_COMPLETE_DESIGN.md`
- **立创EDA指南**: 查看 `JLCPCB_EDA_IMPORT_GUIDE.md`
- **KiCad官方文档**: https://docs.kicad.org/

---

**祝你制作顺利！🎉**
