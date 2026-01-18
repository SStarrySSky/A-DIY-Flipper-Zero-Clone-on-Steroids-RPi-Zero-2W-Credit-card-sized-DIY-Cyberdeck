// ============================================
// PwnZero 外壳 3D 模型 - 完整版
// ============================================
// 信用卡尺寸便携黑客工具外壳
// 尺寸: 85.6mm x 53.98mm x 25mm

// ============================================
// 全局参数
// ============================================

// 外壳尺寸
case_length = 85.6;
case_width = 53.98;
case_height = 25;
wall_thickness = 2;
corner_radius = 3;

// 分层高度
bottom_height = 15;  // 底壳高度
top_height = 10;     // 顶盖高度

// OLED 开孔 (顶层)
oled_x = 15;
oled_y = 8;
oled_width = 32;
oled_height = 16;

// 五向摇杆开孔 (顶层)
joystick_x = 60;
joystick_y = case_width / 2;
joystick_diameter = 12;

// LED 开孔 (顶层右侧)
led_x = 78;
led_y_positions = [5, 13, 21];  // 红、黄、绿
led_diameter = 5.5;

// USB 开孔 (侧面)
usb_x = 54;
usb_width = 8;
usb_height = 3;

// 天线孔 (侧面)
antenna_x = 10;
antenna_diameter = 2;

// 安装柱位置 (4个角)
mount_positions = [
    [5, 5],
    [case_length - 5, 5],
    [5, case_width - 5],
    [case_length - 5, case_width - 5]
];
mount_diameter = 4;
mount_screw_diameter = 2.5;

// ============================================
// 基础模块
// ============================================

// 圆角立方体
module rounded_cube(size, radius) {
    hull() {
        for (x = [radius, size[0] - radius])
            for (y = [radius, size[1] - radius])
                for (z = [radius, size[2] - radius])
                    translate([x, y, z])
                        sphere(r = radius, $fn = 30);
    }
}

// ============================================
// 底壳模块
// ============================================
module bottom_case() {
    difference() {
        // 外壳主体
        rounded_cube([case_length, case_width, bottom_height], corner_radius);
        
        // 内部挖空
        translate([wall_thickness, wall_thickness, wall_thickness])
            cube([
                case_length - wall_thickness * 2,
                case_width - wall_thickness * 2,
                bottom_height
            ]);
        
        // USB 开孔 (短边侧面)
        translate([usb_x, -1, 5])
            cube([usb_width, wall_thickness + 2, usb_height]);
        
        // 天线孔 x2 (长边侧面)
        for (y_pos = [15, 35])
            translate([-1, y_pos, 8])
                rotate([0, 90, 0])
                    cylinder(h = wall_thickness + 2, d = antenna_diameter, $fn = 20);
    }
    
    // 安装柱
    for (pos = mount_positions) {
        translate([pos[0], pos[1], wall_thickness])
            difference() {
                cylinder(h = 8, d = mount_diameter, $fn = 30);
                translate([0, 0, 4])
                    cylinder(h = 5, d = mount_screw_diameter, $fn = 20);
            }
    }
}


// ============================================
// 顶盖模块
// ============================================
module top_case() {
    difference() {
        // 顶盖主体
        rounded_cube([case_length, case_width, top_height], corner_radius);
        
        // 内部挖空
        translate([wall_thickness, wall_thickness, -1])
            cube([
                case_length - wall_thickness * 2,
                case_width - wall_thickness * 2,
                top_height - wall_thickness + 1
            ]);
        
        // OLED 显示屏开孔
        translate([oled_x, oled_y, -1])
            cube([oled_width, oled_height, wall_thickness + 2]);
        
        // 五向摇杆开孔
        translate([joystick_x, joystick_y, -1])
            cylinder(h = wall_thickness + 2, d = joystick_diameter, $fn = 30);
        
        // LED 开孔 x3 (红、黄、绿)
        for (y_pos = led_y_positions)
            translate([led_x, y_pos, -1])
                cylinder(h = wall_thickness + 2, d = led_diameter, $fn = 30);
    }
}


// ============================================
// 曲面透明面板模块
// ============================================
module curved_panel() {
    panel_thickness = 2;
    curve_radius = 150;
    
    difference() {
        // 曲面主体
        translate([0, 0, 0])
            intersection() {
                // 基础平板
                cube([case_length, case_width, panel_thickness]);
                
                // 曲面切割
                translate([case_length/2, case_width/2, -curve_radius + panel_thickness])
                    sphere(r = curve_radius, $fn = 100);
            }
        
        // OLED 开孔
        translate([oled_x, oled_y, -1])
            cube([oled_width, oled_height, panel_thickness + 2]);
        
        // 摇杆开孔
        translate([joystick_x, joystick_y, -1])
            cylinder(h = panel_thickness + 2, d = joystick_diameter, $fn = 30);
        
        // LED 开孔
        for (y_pos = led_y_positions)
            translate([led_x, y_pos, -1])
                cylinder(h = panel_thickness + 2, d = led_diameter, $fn = 30);
    }
}


// ============================================
// 摇杆按键帽模块
// ============================================
module joystick_cap() {
    difference() {
        // 按键帽主体 (锥形)
        cylinder(h = 8, d1 = 10, d2 = 8, $fn = 30);
        
        // 内部凹槽 (配合摇杆)
        translate([0, 0, -1])
            cylinder(h = 4, d = 6, $fn = 30);
    }
    
    // 防滑纹理
    for (angle = [0:45:315])
        rotate([0, 0, angle])
            translate([3.5, 0, 4])
                cube([0.5, 0.5, 3], center = true);
}


// ============================================
// 曲面面板模具 (用于滴胶/亚克力热弯)
// ============================================
module panel_mold() {
    mold_depth = 5;
    
    difference() {
        // 模具外框
        cube([case_length + 10, case_width + 10, mold_depth + 2]);
        
        // 曲面凹槽
        translate([5, 5, 2])
            intersection() {
                cube([case_length, case_width, mold_depth]);
                translate([case_length/2, case_width/2, -145])
                    sphere(r = 150, $fn = 100);
            }
    }
}


// ============================================
// 渲染控制
// ============================================

// 选择要渲染的部件 (取消注释对应行)

// 1. 底壳 (用于3D打印)
bottom_case();

// 2. 顶盖 (用于3D打印)
// translate([0, 60, 0]) top_case();

// 3. 曲面面板 (用于参考，实际用滴胶/亚克力制作)
// translate([0, 120, 0]) curved_panel();

// 4. 摇杆按键帽 (用于3D打印)
// translate([100, 0, 0]) joystick_cap();

// 5. 曲面面板模具 (用于滴胶浇注)
// translate([0, 180, 0]) panel_mold();

// ============================================
// 完整装配视图 (预览用)
// ============================================
/*
// 底壳
bottom_case();

// 顶盖 (分离显示)
translate([0, 0, 20])
    top_case();

// 曲面面板
translate([0, 0, 30])
    color("lightblue", 0.3)
    curved_panel();

// 摇杆帽
translate([joystick_x, joystick_y, 32])
    color("red")
    joystick_cap();
*/

