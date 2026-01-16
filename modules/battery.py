"""
Battery Manager for PiSugar 3.
Communicates with PiSugar daemon via TCP socket.
"""

import socket
import subprocess
from config import SIMULATION_MODE


class BatteryManager:
    """Manages PiSugar 3 battery monitoring."""

    PISUGAR_HOST = '127.0.0.1'
    PISUGAR_PORT = 8423

    def __init__(self):
        self.available = False
        self.last_level = -1
        self.is_charging = False
        self._check_availability()

    def _check_availability(self):
        """Check if PiSugar daemon is running."""
        if SIMULATION_MODE:
            self.available = True
            return

        try:
            result = self._send_command('get battery')
            if result and 'battery' in result.lower():
                self.available = True
                print("Battery: PiSugar 3 detected")
            else:
                self.available = False
                print("Battery: PiSugar not detected")
        except Exception as e:
            self.available = False
            print(f"Battery: PiSugar check failed - {e}")

    def _send_command(self, cmd):
        """Send command to PiSugar daemon via TCP socket."""
        if SIMULATION_MODE:
            return self._simulate_response(cmd)

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0)
            sock.connect((self.PISUGAR_HOST, self.PISUGAR_PORT))
            sock.sendall((cmd + '\n').encode())
            response = sock.recv(256).decode().strip()
            sock.close()
            return response
        except Exception as e:
            return None

    def _simulate_response(self, cmd):
        """Simulate PiSugar responses for testing."""
        import random
        if 'get battery' in cmd:
            return f'battery: {random.randint(60, 95)}.{random.randint(0, 9)}'
        elif 'get battery_charging' in cmd:
            return 'battery_charging: false'
        elif 'get battery_power_plugged' in cmd:
            return 'battery_power_plugged: false'
        return ''

    def get_level(self):
        """Get battery level percentage (0-100)."""
        response = self._send_command('get battery')
        if response:
            try:
                # Response format: "battery: 85.5"
                parts = response.split(':')
                if len(parts) >= 2:
                    level = float(parts[1].strip())
                    self.last_level = int(level)
                    return self.last_level
            except (ValueError, IndexError):
                pass
        return self.last_level if self.last_level >= 0 else -1

    def is_charging(self):
        """Check if battery is currently charging."""
        response = self._send_command('get battery_charging')
        if response:
            self.is_charging = 'true' in response.lower()
        return self.is_charging

    def is_plugged(self):
        """Check if power is plugged in."""
        response = self._send_command('get battery_power_plugged')
        if response:
            return 'true' in response.lower()
        return False

    def get_voltage(self):
        """Get battery voltage in mV."""
        response = self._send_command('get battery_v')
        if response:
            try:
                parts = response.split(':')
                if len(parts) >= 2:
                    return float(parts[1].strip())
            except (ValueError, IndexError):
                pass
        return 0.0

    def get_status_string(self):
        """Get formatted battery status for display."""
        level = self.get_level()

        if level < 0:
            return "--"

        charging = self.is_charging()
        if charging:
            return f"{level}%+"
        else:
            return f"{level}%"

    def get_icon(self):
        """Get battery icon character based on level."""
        level = self.get_level()
        charging = self.is_charging()

        if level < 0:
            return "?"
        elif charging:
            return "C"  # Charging
        elif level > 75:
            return "F"  # Full
        elif level > 50:
            return "H"  # High
        elif level > 25:
            return "M"  # Medium
        elif level > 10:
            return "L"  # Low
        else:
            return "!"  # Critical
