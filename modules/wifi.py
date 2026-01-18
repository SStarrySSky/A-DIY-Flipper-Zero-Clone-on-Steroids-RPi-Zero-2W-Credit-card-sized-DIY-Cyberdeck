"""
WiFi Penetration Testing Module
WiFi 渗透测试模块 - 基于 aircrack-ng 套件
"""

import subprocess
import re
from config import SIMULATION_MODE


class WiFiModule:
    """WiFi 渗透测试功能"""

    def __init__(self):
        self.interface = "wlan0"
        self.monitor_mode = False
        self.available = self._check_tools()

    def _check_tools(self):
        """检查 aircrack-ng 工具是否安装"""
        if SIMULATION_MODE:
            print("WiFi: Simulation mode")
            return True

        try:
            subprocess.run(['airmon-ng', '--version'],
                         capture_output=True, timeout=5)
            print("WiFi: aircrack-ng found")
            return True
        except:
            print("WiFi: aircrack-ng not installed")
            return False
