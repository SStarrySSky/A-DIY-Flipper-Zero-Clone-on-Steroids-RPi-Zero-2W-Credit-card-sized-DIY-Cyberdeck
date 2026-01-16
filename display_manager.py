"""
Display Manager for PiHacker device.
Handles all OLED screen operations using SH1106 driver.
"""

import time
from datetime import datetime
from config import Display, UI, SIMULATION_MODE


class DisplayManager:
    """Manages the SH1106 OLED display with menu rendering capabilities."""

    def __init__(self, battery_manager=None):
        self.width = Display.WIDTH
        self.height = Display.HEIGHT
        self.device = None
        self.draw = None
        self.font = None
        self.font_small = None
        self.battery = battery_manager
        self._init_display()

    def _init_display(self):
        """Initialize the OLED display hardware or simulation."""
        if SIMULATION_MODE:
            print("Simulation: Display initialized (128x64 OLED)")
            self._init_simulation()
        else:
            self._init_hardware()

    def _init_hardware(self):
        """Initialize real hardware display."""
        try:
            from luma.core.interface.serial import i2c
            from luma.oled.device import sh1106
            from PIL import ImageFont, Image, ImageDraw

            serial = i2c(port=1, address=Display.I2C_ADDRESS)
            self.device = sh1106(serial, width=self.width, height=self.height)
            self._load_fonts()
            print("Display: SH1106 initialized successfully")
        except Exception as e:
            print(f"Display init failed: {e}, falling back to simulation")
            self._init_simulation()

    def _init_simulation(self):
        """Initialize simulation mode display."""
        try:
            from PIL import Image, ImageDraw, ImageFont
            self.sim_image = Image.new('1', (self.width, self.height), 0)
            self.draw = ImageDraw.Draw(self.sim_image)
            self._load_fonts()
        except ImportError:
            print("Simulation: PIL not available, text-only mode")
            self.draw = None

    def _load_fonts(self):
        """Load fonts for display rendering."""
        try:
            from PIL import ImageFont
            self.font = ImageFont.load_default()
            self.font_small = self.font
        except:
            self.font = None
            self.font_small = None

    def clear(self):
        """Clear the display."""
        if SIMULATION_MODE:
            if self.draw:
                self.draw.rectangle((0, 0, self.width, self.height), fill=0)
        elif self.device:
            self.device.clear()

    def show(self):
        """Push buffer to display."""
        if SIMULATION_MODE:
            print("Simulation: Display updated")
        elif self.device:
            pass  # luma handles this automatically

    def _get_canvas(self):
        """Get drawing canvas."""
        if SIMULATION_MODE:
            from PIL import Image, ImageDraw
            self.sim_image = Image.new('1', (self.width, self.height), 0)
            return ImageDraw.Draw(self.sim_image)
        else:
            from luma.core.render import canvas
            return canvas(self.device)

    def draw_status_bar(self, draw):
        """Draw the top status bar with system info."""
        bar_height = UI.STATUS_BAR_HEIGHT
        draw.rectangle((0, 0, self.width, bar_height), fill=255)

        # Time
        current_time = datetime.now().strftime("%H:%M")
        draw.text((2, 1), current_time, fill=0, font=self.font_small)

        # CPU Temp
        temp = self._get_cpu_temp()
        draw.text((45, 1), f"{temp}C", fill=0, font=self.font_small)

        # Battery status
        bat_str = self._get_battery_string()
        draw.text((85, 1), bat_str, fill=0, font=self.font_small)

        # Separator line
        draw.line((0, bar_height, self.width, bar_height), fill=255)

    def _get_cpu_temp(self):
        """Get CPU temperature."""
        if SIMULATION_MODE:
            return "42"
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = int(f.read()) / 1000
                return f"{temp:.0f}"
        except:
            return "--"

    def _get_battery_string(self):
        """Get battery status string for display."""
        if self.battery:
            return self.battery.get_status_string()
        return "--"

    def draw_menu(self, title, items, selected_index, scroll_offset=0):
        """Draw a scrollable menu list."""
        if SIMULATION_MODE:
            self._draw_menu_simulation(title, items, selected_index, scroll_offset)
        else:
            self._draw_menu_hardware(title, items, selected_index, scroll_offset)

    def _draw_menu_simulation(self, title, items, selected_index, scroll_offset):
        """Draw menu in simulation mode."""
        from PIL import Image, ImageDraw
        img = Image.new('1', (self.width, self.height), 0)
        draw = ImageDraw.Draw(img)

        self.draw_status_bar(draw)
        self._render_menu_content(draw, title, items, selected_index, scroll_offset)

        self._print_menu_text(title, items, selected_index)

    def _draw_menu_hardware(self, title, items, selected_index, scroll_offset):
        """Draw menu on real hardware."""
        from luma.core.render import canvas
        with canvas(self.device) as draw:
            self.draw_status_bar(draw)
            self._render_menu_content(draw, title, items, selected_index, scroll_offset)

    def _render_menu_content(self, draw, title, items, selected_index, scroll_offset):
        """Render menu items to the draw context."""
        start_y = UI.STATUS_BAR_HEIGHT + 2
        item_height = 12
        visible_items = UI.MENU_ITEMS_VISIBLE

        for i in range(visible_items):
            item_idx = scroll_offset + i
            if item_idx >= len(items):
                break

            y = start_y + (i * item_height)
            item_text = items[item_idx]

            if item_idx == selected_index:
                draw.rectangle((0, y, self.width, y + item_height - 1), fill=255)
                draw.text((4, y + 1), f"> {item_text}", fill=0, font=self.font)
            else:
                draw.text((4, y + 1), f"  {item_text}", fill=255, font=self.font)

    def _print_menu_text(self, title, items, selected_index):
        """Print menu to console in simulation mode."""
        print(f"\n{'='*30}")
        print(f"  {title}")
        print(f"{'='*30}")
        for i, item in enumerate(items):
            marker = ">" if i == selected_index else " "
            print(f"  {marker} {item}")
        print(f"{'='*30}\n")

    def draw_message(self, title, message, icon=None):
        """Draw a message screen with optional icon."""
        if SIMULATION_MODE:
            print(f"Simulation: [{title}] {message}")
            self._draw_message_sim(title, message)
        else:
            self._draw_message_hw(title, message)

    def _draw_message_sim(self, title, message):
        """Draw message in simulation mode."""
        from PIL import Image, ImageDraw
        img = Image.new('1', (self.width, self.height), 0)
        draw = ImageDraw.Draw(img)
        self.draw_status_bar(draw)
        draw.text((4, 20), title, fill=255, font=self.font)
        draw.text((4, 35), message, fill=255, font=self.font)

    def _draw_message_hw(self, title, message):
        """Draw message on hardware."""
        from luma.core.render import canvas
        with canvas(self.device) as draw:
            self.draw_status_bar(draw)
            draw.text((4, 20), title, fill=255, font=self.font)
            draw.text((4, 35), message, fill=255, font=self.font)

    def draw_signal_graph(self, title, data_points, max_val=100):
        """Draw a signal strength graph (for RSSI display)."""
        if SIMULATION_MODE:
            print(f"Simulation: Signal graph - {title}")
            print(f"  Data points: {len(data_points)}")
            self._draw_graph_sim(title, data_points, max_val)
        else:
            self._draw_graph_hw(title, data_points, max_val)

    def _draw_graph_sim(self, title, data_points, max_val):
        """Draw graph in simulation mode."""
        from PIL import Image, ImageDraw
        img = Image.new('1', (self.width, self.height), 0)
        draw = ImageDraw.Draw(img)
        self.draw_status_bar(draw)
        self._render_graph(draw, title, data_points, max_val)

    def _draw_graph_hw(self, title, data_points, max_val):
        """Draw graph on hardware."""
        from luma.core.render import canvas
        with canvas(self.device) as draw:
            self.draw_status_bar(draw)
            self._render_graph(draw, title, data_points, max_val)

    def _render_graph(self, draw, title, data_points, max_val):
        """Render signal graph to draw context."""
        graph_top = UI.STATUS_BAR_HEIGHT + 2
        graph_bottom = self.height - 2
        graph_height = graph_bottom - graph_top

        draw.text((2, graph_top), title, fill=255, font=self.font_small)

        if not data_points:
            return

        graph_top += 12
        graph_height -= 12
        points_to_show = min(len(data_points), self.width - 4)
        step = max(1, len(data_points) // points_to_show)

        for i in range(points_to_show):
            idx = i * step
            if idx >= len(data_points):
                break
            val = data_points[idx]
            bar_height = int((val / max_val) * graph_height)
            x = 2 + i
            draw.line((x, graph_bottom, x, graph_bottom - bar_height), fill=255)

    def draw_progress(self, title, progress, message=""):
        """Draw a progress bar screen."""
        if SIMULATION_MODE:
            bar = "#" * int(progress / 5) + "-" * (20 - int(progress / 5))
            print(f"Simulation: {title} [{bar}] {progress}% {message}")
        else:
            from luma.core.render import canvas
            with canvas(self.device) as draw:
                self.draw_status_bar(draw)
                draw.text((4, 20), title, fill=255, font=self.font)
                bar_width = int((self.width - 8) * progress / 100)
                draw.rectangle((4, 35, self.width - 4, 45), outline=255)
                draw.rectangle((4, 35, 4 + bar_width, 45), fill=255)
                draw.text((4, 50), message, fill=255, font=self.font_small)
