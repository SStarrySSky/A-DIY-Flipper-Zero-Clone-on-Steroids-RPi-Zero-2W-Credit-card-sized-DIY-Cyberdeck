// PwnZero Case - OpenSCAD Model
// 圆角外壳设计，适配 Pi Zero 2W + 扩展板

// ============================================
// 参数设置
// ============================================

// 外壳尺寸 (信用卡尺寸)
case_length = 85.6;
case_width = 53.98;
case_height = 25;
wall_thickness = 2;
corner_radius = 3;

// 曲面面板参数
panel_thickness = 2;  // 亚克力/滴胶厚度
panel_curve_radius = 150;  // 曲面半径 (越大越平)

// Pi Zero 尺寸
pi_length = 65;
pi_width = 30;

// OLED 开孔
oled_width = 32;
oled_height = 16;
oled_x = 10;
oled_y = 8;

// 五向按键开孔
button_diameter = 12;
button_x = 60;
button_y = case_width / 2;

// LED 开孔
led_diameter = 5.5;
led_spacing = 8;
led_x = 45;
led_y = 5;

// USB 开孔
usb_width = 12;
usb_height = 6;

// 天线孔
antenna_diameter = 6;

// ============================================
// 圆角立方体模块
// ============================================
module rounded_cube(size, radius) {
    hull() {
        for (x = [radius, size[0] - radius])
            for (y = [radius, size[1] - radius])
                for (z = [radius, size[2] - radius])
                    translate([x, y, z])
                        sphere(r = radius, $fn = 20);
    }
}

// ============================================
// 底壳模块
// ============================================
module bottom_case() {
    difference() {
        // 外壳主体
        rounded_cube([case_length, case_width, case_height/2], corner_radius);

        // 内部挖空
        translate([wall_thickness, wall_thickness, wall_thickness])
            cube([case_length - wall_thickness*2,
                  case_width - wall_thickness*2,
                  case_height]);
    }
}

// ============================================
// 顶盖模块
// ============================================
module top_case() {
    difference() {
        // 顶盖主体
        rounded_cube([case_length, case_width, case_height/2], corner_radius);

        // 内部挖空
        translate([wall_thickness, wall_thickness, -1])
            cube([case_length - wall_thickness*2,
                  case_width - wall_thickness*2,
                  case_height/2 - wall_thickness + 1]);

        // OLED 开孔
        translate([oled_x, oled_y, -1])
            cube([oled_width, oled_height, wall_thickness + 2]);

        // 五向按键开孔
        translate([button_x, button_y, -1])
            cylinder(h = wall_thickness + 2, d = button_diameter, $fn = 30);

        // LED 开孔 x3
        for (i = [0:2]) {
            translate([led_x + i * led_spacing, led_y, -1])
                cylinder(h = wall_thickness + 2, d = led_diameter, $fn = 20);
        }
    }
}

// ============================================
// 按键帽模块
// ============================================
module button_cap() {
    difference() {
        cylinder(h = 5, d1 = 10, d2 = 8, $fn = 30);
        translate([0, 0, -1])
            cylinder(h = 3, d = 6, $fn = 30);
    }
}

// ============================================
// 渲染选择
// ============================================
// 取消注释来渲染不同部件

// 底壳
// bottom_case();

// 顶盖
top_case();

// 按键帽
// translate([0, 70, 0]) button_cap();
