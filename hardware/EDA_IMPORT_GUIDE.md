# PwnZero EDA 文件导入指南

## 📁 已生成的文件

本目录包含以下可导入EDA软件的文件：

| 文件名 | 格式 | 用途 |
|--------|------|------|
| `pwnzero.net` | Netlist | 网表文件，包含所有元件和连接关系 |
| `pwnzero_bom.csv` | CSV | 物料清单，可直接用于采购 |
| `pwnzero_pcb_layout.txt` | Text | PCB布局坐标参考 |
| `pwnzero.kicad_pro` | KiCad | KiCad项目文件 |

---

## 🔧 方法一：使用立创EDA（推荐国内用户）

### 步骤：

1. **打开立创EDA**
   - 访问：https://lceda.cn/
   - 或下载桌面版

2. **创建新项目**
   - 点击"新建项目" → 命名为 "PwnZero"

3. **导入网表文件**
   - 打开PCB编辑器
   - 文件 → 导入 → 网表文件
   - 选择 `pwnzero.net`

4. **导入BOM清单**
   - 工具 → BOM → 导入CSV
   - 选择 `pwnzero_bom.csv`
   - 系统会自动匹配嘉立创商城的元件

5. **手动布局**
   - 参考 `pwnzero_pcb_layout.txt` 中的坐标
   - 设置PCB尺寸：85.6mm x 53.98mm
   - 按照坐标放置元件

6. **布线**
   - 使用自动布线或手动布线
   - 注意电源线宽度：
     - 3.3V: 0.5mm
     - 5V: 0.6mm
     - GND: 铺铜

7. **生成Gerber文件**
   - 文件 → 导出 → Gerber
   - 直接下单到嘉立创PCB

---

## 🔧 方法二：使用KiCad（开源免费）

### 步骤：

1. **安装KiCad**
   - 下载：https://www.kicad.org/
   - 版本要求：6.0 或更高

2. **打开项目**
   - 文件 → 打开项目
   - 选择 `pwnzero.kicad_pro`

3. **导入网表**
   - 打开PCB编辑器（Pcbnew）
   - 工具 → 加载网表
   - 选择 `pwnzero.net`

4. **设置PCB参数**
   ```
   尺寸：85.6mm x 53.98mm
   层数：2层
   板厚：1.6mm
   最小线宽：0.2mm
   最小间距：0.2mm
   ```

5. **元件布局**
   - 参考 `pwnzero_pcb_layout.txt`
   - 顶层：OLED、摇杆、LED
   - 底层：CC1101、PN532、IR、SMD元件

6. **布线规则**
   - 编辑 → 板设置 → 设计规则
   - 设置不同网络的线宽

7. **生成制造文件**
   - 文件 → 绘图
   - 选择Gerber格式
   - 生成钻孔文件

---

## 🔧 方法三：使用Altium Designer

### 步骤：

1. **创建新项目**
   - File → New → Project
   - 命名为 "PwnZero"

2. **导入网表**
   - Design → Import → Netlist
   - 选择格式：Protel
   - 选择 `pwnzero.net`

3. **导入BOM**
   - Tools → Bill of Materials
   - Import → 选择 `pwnzero_bom.csv`

4. **PCB设计**
   - 创建新PCB文件
   - 设置板框：85.6mm x 53.98mm
   - 更新PCB（Design → Update PCB）

5. **布局布线**
   - 参考坐标文件手动放置元件
   - 设置布线规则
   - 自动或手动布线

6. **输出Gerber**
   - File → Fabrication Outputs → Gerber Files

---

## 📦 直接下单到PCB厂商

### 嘉立创（JLCPCB）

1. 访问：https://www.jlc.com/
2. 上传Gerber文件
3. 导入BOM：`pwnzero_bom.csv`
4. 选择SMT贴片服务（可选）
5. 参数设置：
   - 尺寸：85.6 x 53.98 mm
   - 层数：2层
   - 板厚：1.6mm
   - 阻焊：黑色
   - 字符：白色
   - 表面处理：HASL无铅

### 华秋PCB

1. 访问：https://www.hqpcb.com/
2. 类似流程
3. 可选择SMT贴片

---

## 📋 BOM采购说明

`pwnzero_bom.csv` 包含所有元件的详细信息：

- **LCSC Part Number**：立创商城料号，可直接搜索购买
- **Manufacturer Part**：原厂料号
- **Quantity**：数量

### 采购渠道：

1. **立创商城**（推荐）
   - https://www.szlcsc.com/
   - 使用LCSC料号直接搜索

2. **淘宝**
   - 搜索原厂料号
   - 注意核对规格

3. **亚马逊/eBay**
   - 国际采购
   - 适合批量购买

---

## ⚠️ 重要注意事项

### 电压警告
```
CC1101: 只能接 3.3V（接5V会烧毁）
PN532:  接 5V（模块自带稳压）
OLED:   接 3.3V
IR:     接 3.3V
```

### 电容放置
- C1, C2 必须紧靠 CC1101 TX 的 VCC/GND 引脚
- C3, C4 必须紧靠 CC1101 RX 的 VCC/GND 引脚
- 距离越近越好（< 5mm）

### PN532 拨码开关
```
I2C 模式设置：
SEL0 = 1 (ON)
SEL1 = 0 (OFF)
```

---

## 🛠️ 下一步

1. ✅ 选择一个EDA软件导入文件
2. ✅ 完成PCB布局和布线
3. ✅ 生成Gerber文件
4. ✅ 下单PCB制造
5. ✅ 采购元件（使用BOM清单）
6. ✅ 焊接组装
7. ✅ 测试调试

---

## 📞 技术支持

如有问题，请参考：
- 原理图：`SCHEMATIC.md`
- PCB布局：`PCB_LAYOUT_DETAIL.md`
- 主README：`../README.md`

---

**祝你制作顺利！🎉**
