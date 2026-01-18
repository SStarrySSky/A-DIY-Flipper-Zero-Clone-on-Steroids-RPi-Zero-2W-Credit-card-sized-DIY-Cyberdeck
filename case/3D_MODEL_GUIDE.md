# PwnZero 3D 模型资源指南

## 📦 外壳3D模型（已创建）

本项目已包含以下可直接3D打印的外壳模型：

| 文件名 | 说明 | 用途 |
|--------|------|------|
| `pwnzero_case_complete.scad` | 完整外壳模型（OpenSCAD） | 可编辑的参数化模型 |
| `pwnzero_case.scad` | 简化版外壳 | 快速预览 |

### 外壳包含的部件：

1. **底壳** - 容纳Raspberry Pi和PCB
2. **顶盖** - 带OLED、摇杆、LED开孔
3. **曲面透明面板** - 参考模型（实际用滴胶/亚克力制作）
4. **摇杆按键帽** - 可3D打印
5. **曲面面板模具** - 用于滴胶浇注

---

## 🔧 如何导出STL文件

### 使用OpenSCAD：

1. **安装OpenSCAD**
   - 下载：https://openscad.org/downloads.html
   - 免费开源软件

2. **打开模型文件**
   ```
   文件 → 打开 → 选择 pwnzero_case_complete.scad
   ```

3. **选择要导出的部件**
   - 编辑文件底部的渲染控制部分
   - 取消注释想要导出的部件
   - 例如导出底壳：
   ```openscad
   bottom_case();  // 取消注释这行
   ```

4. **渲染并导出**
   ```
   设计 → 渲染 (F6)
   文件 → 导出 → 导出为STL
   ```

5. **重复步骤3-4**，分别导出：
   - `bottom_case.stl` - 底壳
   - `top_case.stl` - 顶盖
   - `joystick_cap.stl` - 摇杆帽
   - `panel_mold.stl` - 面板模具（可选）

---

## 📥 电子元件3D模型下载

电子元件的3D模型需要从以下网站下载：


### 1. GrabCAD（推荐）

**网址：** https://grabcad.com/

**搜索关键词：**
- `Raspberry Pi Zero 2W` - 树莓派主板
- `CC1101 module` - Sub-GHz无线模块
- `PN532 NFC module` - NFC模块
- `SH1106 OLED 1.3 inch` - OLED显示屏
- `5-way tactile switch` - 五向摇杆
- `VS1838B IR receiver` - 红外接收器
- `5mm LED` - LED灯

**优点：**
- 模型质量高
- 免费下载
- 格式多样（STEP, STL, IGES）

---

### 2. Thingiverse

**网址：** https://www.thingiverse.com/

**搜索关键词：**
- `Raspberry Pi Zero`
- `CC1101`
- `PN532`
- `OLED display`

**优点：**
- 开源社区
- 直接提供STL文件
- 适合3D打印

---

### 3. Traceparts（工业级）

**网址：** https://www.traceparts.com/

**搜索关键词：**
- 按照元件型号搜索
- 提供原厂CAD模型

**优点：**
- 精度最高
- 原厂认证
- 多种CAD格式


### 4. 淘宝商家（国内）

很多淘宝卖家会提供元件的3D模型：

- 搜索元件型号 + "3D模型"
- 联系卖家索取STEP/STL文件
- 部分商家免费提供

---

## 📋 所需元件3D模型清单

| 元件 | 型号 | 数量 | 推荐下载源 |
|------|------|------|------------|
| 主控板 | Raspberry Pi Zero 2W | 1 | GrabCAD |
| 无线模块 | CC1101 | 2 | GrabCAD |
| NFC模块 | PN532 | 1 | GrabCAD |
| 显示屏 | SH1106 OLED 1.3" | 1 | GrabCAD |
| 摇杆 | 5-Way Tactile Switch | 1 | Thingiverse |
| IR接收 | VS1838B | 1 | Traceparts |
| LED | 5mm LED | 4 | 通用模型 |
| 电池 | PiSugar 3 | 1 | 官方网站 |


---

## 🖨️ 3D打印参数建议

### 底壳 (bottom_case.stl)

```
材料: PLA / PETG
层高: 0.2mm
填充: 20%
支撑: 需要
壁厚: 3层
打印时间: 约4-6小时
```

### 顶盖 (top_case.stl)

```
材料: PLA / PETG
层高: 0.2mm
填充: 20%
支撑: 需要
壁厚: 3层
打印时间: 约3-5小时
```

### 摇杆帽 (joystick_cap.stl)

```
材料: PLA / TPU (软胶)
层高: 0.15mm
填充: 100%
支撑: 不需要
打印时间: 约30分钟
```


### 曲面面板模具 (panel_mold.stl)

```
材料: PLA
层高: 0.2mm
填充: 30%
支撑: 需要
用途: 滴胶浇注模具
打印时间: 约2-3小时
```

---

## 🎨 曲面透明面板制作

### 方案一：水晶滴胶AB胶

1. **打印模具**
   - 打印 `panel_mold.stl`
   - 打磨光滑

2. **准备材料**
   - AB胶（1:1比例）
   - 脱模剂
   - 搅拌棒

3. **浇注**
   - 涂抹脱模剂
   - 混合AB胶
   - 倒入模具
   - 静置24小时

4. **脱模**
   - 小心脱模
   - 打磨边缘


### 方案二：亚克力热弯

1. **准备材料**
   - 2mm透明亚克力板
   - 热风枪/烤箱

2. **加热**
   - 加热至160°C
   - 均匀加热

3. **成型**
   - 压入模具
   - 保持形状冷却

---

## 🔧 装配步骤

### 1. 准备工作

- [ ] 打印所有外壳部件
- [ ] 下载电子元件3D模型
- [ ] 制作曲面透明面板

### 2. 装配顺序

1. **底壳安装**
   - 将Raspberry Pi Zero 2W固定在底壳安装柱上
   - 使用M2.5螺丝固定

2. **PCB安装**
   - 将扩展PCB通过40针排针连接到Pi Zero
   - 确保所有模块正确插入

3. **顶盖安装**
   - 将OLED、摇杆、LED从顶盖开孔穿出
   - 盖上顶盖

4. **面板安装**
   - 将曲面透明面板覆盖在顶盖上
   - 可用胶水固定边缘

5. **摇杆帽安装**
   - 将3D打印的摇杆帽套在摇杆上


---

## ⚠️ 注意事项

### 3D打印注意事项

1. **支撑结构**
   - 底壳和顶盖需要支撑
   - 使用树形支撑更易去除

2. **打印方向**
   - 底壳：开口朝上
   - 顶盖：开口朝下
   - 摇杆帽：底部朝下

3. **后处理**
   - 去除支撑后打磨
   - 可用砂纸抛光
   - 可喷漆增加质感

### 装配注意事项

1. **静电防护**
   - 触摸电子元件前先放电
   - 使用防静电手环

2. **螺丝规格**
   - M2.5 x 6mm（固定Pi Zero）
   - 不要拧太紧

3. **开孔对齐**
   - 装配前检查所有开孔位置
   - 确保元件能正确穿出


---

## 📊 文件清单总结

### 已创建的3D模型文件

| 文件名 | 类型 | 说明 |
|--------|------|------|
| `pwnzero_case_complete.scad` | OpenSCAD | 完整参数化外壳模型 |
| `pwnzero_case.scad` | OpenSCAD | 简化版外壳 |

### 需要导出的STL文件

- `bottom_case.stl` - 底壳
- `top_case.stl` - 顶盖
- `joystick_cap.stl` - 摇杆帽
- `panel_mold.stl` - 面板模具（可选）

### 需要下载的电子元件模型

- Raspberry Pi Zero 2W
- CC1101 x2
- PN532
- SH1106 OLED
- 5-Way Joystick
- VS1838B
- LEDs x4

---

## 🎯 下一步

1. ✅ 安装OpenSCAD
2. ✅ 打开 `pwnzero_case_complete.scad`
3. ✅ 导出STL文件
4. ✅ 从GrabCAD下载电子元件模型
5. ✅ 3D打印外壳部件
6. ✅ 制作曲面透明面板
7. ✅ 装配完成

---

**祝你制作顺利！🎉**

