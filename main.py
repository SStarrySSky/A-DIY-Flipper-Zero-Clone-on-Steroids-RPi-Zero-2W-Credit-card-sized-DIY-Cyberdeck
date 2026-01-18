"""
PiHacker - Main Application Entry Point.
Flipper Zero-like device for Raspberry Pi Zero 2 W.
"""

import sys
import time
import signal
from config import Buttons, SIMULATION_MODE


class MenuState:
    """Tracks current menu state."""
    MAIN = 'main'
    SUBGHZ = 'subghz'
    NFC = 'nfc'
    IR = 'infrared'
    WIFI = 'wifi'
    SYSTEM = 'system'


class PiHacker:
    """Main application class."""

    def __init__(self):
        self.running = False
        self.current_menu = MenuState.MAIN
        self.selected_index = 0
        self.scroll_offset = 0
        self.display = None
        self.input_handler = None
        self.battery = None
        self.subghz = None
        self.nfc = None
        self.ir = None
        self.led = None
        self._init_hardware()

    def _init_hardware(self):
        """Initialize all hardware components."""
        print("PiHacker initializing...")

        from input_handler import InputHandler
        from modules import SubGHzModule, NFCModule, IRModule, BatteryManager, LEDController
        from display_manager import DisplayManager

        # Initialize battery first (needed by display)
        self.battery = BatteryManager()

        # Initialize display with battery manager
        self.display = DisplayManager(battery_manager=self.battery)
        self.input_handler = InputHandler()

        # Initialize other modules
        self.subghz = SubGHzModule()
        self.nfc = NFCModule()
        self.ir = IRModule()
        self.led = LEDController()

        print("PiHacker ready!")

    def get_menu_items(self):
        """Get menu items for current state."""
        menus = {
            MenuState.MAIN: [
                "Sub-GHz",
                "NFC",
                "Infrared",
                "WiFi Tools",
                "System"
            ],
            MenuState.SUBGHZ: [
                "Read Signal",
                "Replay",
                "RollJam Demo",
                "Set Frequency",
                "Back"
            ],
            MenuState.NFC: [
                "Read Card",
                "Emulate Card",
                "Back"
            ],
            MenuState.IR: [
                "Universal Remote",
                "Send Power Off",
                "Back"
            ],
            MenuState.WIFI: [
                "Scan Networks",
                "Deauth (Demo)",
                "Back"
            ],
            MenuState.SYSTEM: [
                "Device Info",
                "Battery Info",
                "Reboot",
                "Shutdown",
                "Back"
            ]
        }
        return menus.get(self.current_menu, [])

    def get_menu_title(self):
        """Get title for current menu."""
        titles = {
            MenuState.MAIN: "PiHacker",
            MenuState.SUBGHZ: "Sub-GHz",
            MenuState.NFC: "NFC",
            MenuState.IR: "Infrared",
            MenuState.WIFI: "WiFi Tools",
            MenuState.SYSTEM: "System"
        }
        return titles.get(self.current_menu, "Menu")

    def handle_input(self, button):
        """Handle button input."""
        items = self.get_menu_items()

        if button == Buttons.UP:
            if self.selected_index > 0:
                self.selected_index -= 1
                if self.selected_index < self.scroll_offset:
                    self.scroll_offset = self.selected_index

        elif button == Buttons.DOWN:
            if self.selected_index < len(items) - 1:
                self.selected_index += 1
                if self.selected_index >= self.scroll_offset + 4:
                    self.scroll_offset = self.selected_index - 3

        elif button == Buttons.LEFT:
            self.go_back()

        elif button == Buttons.CENTER:
            self.select_item(items[self.selected_index])

    def go_back(self):
        """Navigate back to previous menu."""
        self.selected_index = 0
        self.scroll_offset = 0
        if self.current_menu != MenuState.MAIN:
            self.current_menu = MenuState.MAIN

    def select_item(self, item):
        """Handle menu item selection."""
        self.selected_index = 0
        self.scroll_offset = 0

        if item == "Back":
            self.go_back()
            return

        # Main menu navigation
        if self.current_menu == MenuState.MAIN:
            if item == "Sub-GHz":
                self.current_menu = MenuState.SUBGHZ
            elif item == "NFC":
                self.current_menu = MenuState.NFC
            elif item == "Infrared":
                self.current_menu = MenuState.IR
            elif item == "WiFi Tools":
                self.current_menu = MenuState.WIFI
            elif item == "System":
                self.current_menu = MenuState.SYSTEM

        # Sub-GHz actions
        elif self.current_menu == MenuState.SUBGHZ:
            self._handle_subghz(item)

        # NFC actions
        elif self.current_menu == MenuState.NFC:
            self._handle_nfc(item)

        # IR actions
        elif self.current_menu == MenuState.IR:
            self._handle_ir(item)

        # System actions
        elif self.current_menu == MenuState.SYSTEM:
            self._handle_system(item)

    def _handle_subghz(self, item):
        """Handle Sub-GHz menu actions."""
        if item == "Read Signal":
            self.led.start_chase(speed=0.1)
            self.display.draw_message("Sub-GHz", "Recording...")
            data = self.subghz.record_signal(duration=3.0)
            self.led.stop_chase()
            self.led.success()
            self.display.draw_signal_graph("RSSI", data)
            time.sleep(2)

        elif item == "Replay":
            self.led.start_chase(speed=0.08)
            self.display.draw_message("Sub-GHz", "Replaying...")
            self.subghz.replay_signal()
            self.led.stop_chase()
            self.led.success()
            self.display.draw_message("Sub-GHz", "Done!")
            time.sleep(1)

        elif item == "RollJam Demo":
            self.led.start_chase(speed=0.05)
            self.display.draw_message("RollJam", "Running...")
            self.subghz.rolljam_attack()
            self.led.stop_chase()
            self.led.blink_all(times=3)
            self.display.draw_message("RollJam", "Captured!")
            time.sleep(1)

    def _handle_nfc(self, item):
        """Handle NFC menu actions."""
        if item == "Read Card":
            self.led.start_chase(speed=0.1)
            self.display.draw_message("NFC", "Place card...")
            result = self.nfc.read_card()
            self.led.stop_chase()
            if result.get('uid'):
                self.led.success()
                self.display.draw_message("NFC", f"UID:{result['uid']}")
            elif result.get('error'):
                self.led.error()
                self.display.draw_message("NFC", result['error'])
            else:
                self.led.error()
                self.display.draw_message("NFC", "No card")
            time.sleep(2)

        elif item == "Emulate Card":
            self.led.start_chase(speed=0.1)
            self.display.draw_message("NFC", "Emulating...")
            result = self.nfc.emulate_card()
            self.led.stop_chase()
            if result.get('success'):
                self.led.success()
                self.display.draw_message("NFC", f"Emulated:{result['uid'][:8]}")
            else:
                self.led.error()
                self.display.draw_message("NFC", "Failed")
            time.sleep(2)

    def _handle_ir(self, item):
        """Handle IR menu actions."""
        if item == "Universal Remote":
            self.led.start_chase(speed=0.1)
            self.display.draw_message("IR", "Learning...")
            self.ir.record_signal(duration=5.0)
            self.led.stop_chase()
            self.led.success()
            self.display.draw_message("IR", "Learned!")
            time.sleep(1)

        elif item == "Send Power Off":
            self.led.start_chase(speed=0.08)
            self.display.draw_message("IR", "Sending...")
            self.ir.send_power_off()
            self.led.stop_chase()
            self.led.success()
            self.display.draw_message("IR", "Sent!")
            time.sleep(1)

    def _handle_system(self, item):
        """Handle System menu actions."""
        if item == "Device Info":
            info = f"Mode: {'SIM' if SIMULATION_MODE else 'HW'}"
            self.display.draw_message("System", info)
            time.sleep(2)

        elif item == "Battery Info":
            if self.battery and self.battery.available:
                level = self.battery.get_level()
                charging = "Yes" if self.battery.is_charging() else "No"
                voltage = self.battery.get_voltage()
                self.display.draw_message("Battery", f"{level}% V:{voltage:.2f}")
            else:
                self.display.draw_message("Battery", "Not detected")
            time.sleep(2)

        elif item == "Reboot":
            self.display.draw_message("System", "Rebooting...")
            if not SIMULATION_MODE:
                import os
                os.system("sudo reboot")

        elif item == "Shutdown":
            self.display.draw_message("System", "Shutting down...")
            if not SIMULATION_MODE:
                import os
                os.system("sudo shutdown -h now")

    def render(self):
        """Render current menu to display."""
        items = self.get_menu_items()
        title = self.get_menu_title()
        self.display.draw_menu(title, items, self.selected_index, self.scroll_offset)

    def run(self):
        """Main application loop."""
        self.running = True
        print("Starting main loop...")

        while self.running:
            self.render()
            button = self.input_handler.get_input()
            if button is not None:
                self.handle_input(button)
            time.sleep(0.05)

    def cleanup(self):
        """Clean up resources."""
        print("Cleaning up...")
        if self.led:
            self.led.cleanup()
        if self.input_handler:
            self.input_handler.cleanup()
        if self.subghz:
            self.subghz.close()
        if self.nfc:
            self.nfc.close()
        if self.ir:
            self.ir.close()


def signal_handler(sig, frame):
    """Handle interrupt signal."""
    print("\nInterrupt received, exiting...")
    sys.exit(0)


def main():
    """Application entry point."""
    signal.signal(signal.SIGINT, signal_handler)

    app = PiHacker()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        app.cleanup()


if __name__ == "__main__":
    main()
