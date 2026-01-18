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

