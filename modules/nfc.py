"""
NFC Module for PiHacker device.
Uses libnfc tools (nfc-list, nfc-mfclassic) via subprocess.
"""

import subprocess
import re
import time
from config import SIMULATION_MODE


class NFCModule:
    """NFC操作管理器 - 通过libnfc工具"""

    def __init__(self):
        self.last_uid = None
        self.last_atqa = None
        self.last_sak = None
        self.initialized = False
        self._check_libnfc()

    def _check_libnfc(self):
        """检查libnfc是否安装"""
        if SIMULATION_MODE:
            print("Simulation: NFC module ready")
            self.initialized = True
            return

        try:
            result = subprocess.run(
                ['nfc-list', '-v'],
                capture_output=True,
                timeout=5
            )
            self.initialized = True
            print("NFC: libnfc found")
        except FileNotFoundError:
            print("NFC: libnfc not installed")
            self.initialized = False
        except Exception as e:
            print(f"NFC init error: {e}")
            self.initialized = False

    def read_card(self, callback=None):
        """读取NFC卡片"""
        if callback:
            callback("Scanning...")

        if SIMULATION_MODE:
            time.sleep(1)
            self.last_uid = "04:A3:2B:1C"
            self.last_atqa = "00:04"
            self.last_sak = "08"
            return {'uid': self.last_uid, 'atqa': self.last_atqa, 'sak': self.last_sak}

        if not self.initialized:
            return {'error': 'libnfc not installed'}

        try:
            result = subprocess.run(
                ['nfc-list'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return self._parse_nfc_list(result.stdout)
        except Exception as e:
            return {'error': str(e)}

    def _parse_nfc_list(self, output):
        """解析nfc-list输出"""
        result = {'uid': None, 'atqa': None, 'sak': None}

        uid_match = re.search(r'UID.*?:\s*([0-9a-fA-F\s:]+)', output)
        if uid_match:
            self.last_uid = uid_match.group(1).strip()
            result['uid'] = self.last_uid

        atqa_match = re.search(r'ATQA.*?:\s*([0-9a-fA-F\s:]+)', output)
        if atqa_match:
            self.last_atqa = atqa_match.group(1).strip()
            result['atqa'] = self.last_atqa

        sak_match = re.search(r'SAK.*?:\s*([0-9a-fA-F]+)', output)
        if sak_match:
            self.last_sak = sak_match.group(1).strip()
            result['sak'] = self.last_sak

        return result

    def dump_card(self, filename="card.mfd"):
        """导出卡片数据"""
        if SIMULATION_MODE:
            print(f"Simulation: Dump to {filename}")
            return True

        try:
            subprocess.run(
                ['nfc-mfclassic', 'r', 'a', filename],
                timeout=30
            )
            return True
        except Exception as e:
            print(f"Dump error: {e}")
            return False

    def close(self):
        """清理资源"""
        pass

    def emulate_card(self, uid=None):
        """模拟 NFC 卡片"""
        if not uid:
            uid = self.last_uid if self.last_uid else "04112233"

        if SIMULATION_MODE:
            print(f"Simulation: Emulating UID {uid}")
            return True

        try:
            # 使用 nfc-emulate-uid 模拟卡片
            result = subprocess.run(
                ['nfc-emulate-uid', uid],
                timeout=30,
                capture_output=True
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Emulate error: {e}")
            return False
