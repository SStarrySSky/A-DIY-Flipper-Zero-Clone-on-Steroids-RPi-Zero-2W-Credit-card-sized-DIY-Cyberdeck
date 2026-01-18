// ============================================
// PwnZero Complete 3D Assembly Model
// ============================================
// 包含所有电子元器件的完整装配模型
// 可用于可视化、检查干涉、3D打印参考

// ============================================
// 全局参数
// ============================================

// 外壳尺寸 (信用卡尺寸)
case_length = 85.6;
case_width = 53.98;
case_height = 25;
wall_thickness = 2;
corner_radius = 3;

// PCB 参数
pcb_length = 85.6;
pcb_width = 53.98;
pcb_thickness = 1.6;
pcb_z_position = 5;  // PCB在外壳中的高度

// 显示控制
show_case_bottom = true;
show_case_top = false;
show_pcb = true;
show_components = true;
show_raspberry_pi = true;
exploded_view = false;
explode_distance = 20;

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
                        sphere(r = radius, $fn = 20);
    }
}

// ============================================
// PCB 模块
// ============================================
module pcb_board() {
    color("darkgreen", 0.9)
    difference() {
        // PCB主体
        rounded_cube([pcb_length, pcb_width, pcb_thickness], 1);

        // 安装孔 (4个角)
        for (x = [3, pcb_length - 3])
            for (y = [3, pcb_width - 3])
                translate([x, y, -0.5])
                    cylinder(h = pcb_thickness + 1, d = 2.5, $fn = 20);
    }
}
