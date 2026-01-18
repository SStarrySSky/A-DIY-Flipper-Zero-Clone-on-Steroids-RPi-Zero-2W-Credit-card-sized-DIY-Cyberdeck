"""
Infrared Module for PiHacker device.
Uses pigpio for precise timing control.
"""

import time
from config import IR, SIMULATION_MODE

# 常见遥控器码库 (NEC 协议)
IR_DATABASE = {
    'samsung_tv_power': [9000, 4500, 560, 560, 560, 1690, 560, 560, 560, 1690, 560, 1690, 560, 1690, 560, 560],
    'lg_tv_power': [9000, 4500, 560, 560, 560, 1690, 560, 1690, 560, 560, 560, 1690, 560, 560, 560, 1690],
    'sony_tv_power': [2400, 600, 1200, 600, 600, 600, 1200, 600, 600, 600, 1200, 600, 600],
    'generic_power': [9000, 4500, 560, 560, 560, 560, 560, 560, 560, 560, 560, 1690, 560, 1690, 560, 1690],
}


class IRModule:
    """红外收发模块"""

    def __init__(self):
        self.pi = None
        self.tx_pin = IR.TX_PIN
        self.rx_pin = IR.RX_PIN
        self.recorded_signal = []
        self.is_recording = False
        self._init_gpio()

    def _init_gpio(self):
        """初始化GPIO"""
        if SIMULATION_MODE:
            print("Simulation: IR module ready")
            return

        try:
            import pigpio
            self.pi = pigpio.pi()
            if not self.pi.connected:
                raise Exception("pigpio not connected")
            self.pi.set_mode(self.tx_pin, pigpio.OUTPUT)
            self.pi.set_mode(self.rx_pin, pigpio.INPUT)
            print("IR: pigpio initialized")
        except Exception as e:
            print(f"IR init error: {e}")
            self.pi = None

    def record_signal(self, duration=5.0, callback=None):
        """录制红外信号"""
        self.recorded_signal = []

        if SIMULATION_MODE:
            print(f"Simulation: IR record {duration}s")
            self.recorded_signal = [9000, 4500, 560, 560] * 8
            return self.recorded_signal

        if not self.pi:
            return []

        try:
            self.is_recording = True
            last_tick = self.pi.get_current_tick()
            last_level = self.pi.read(self.rx_pin)
            end_time = time.time() + duration

            while time.time() < end_time and self.is_recording:
                level = self.pi.read(self.rx_pin)
                if level != last_level:
                    tick = self.pi.get_current_tick()
                    pulse = tick - last_tick
                    self.recorded_signal.append(pulse)
                    last_tick = tick
                    last_level = level

            self.is_recording = False
        except Exception as e:
            print(f"IR record error: {e}")

        return self.recorded_signal

    def send_signal(self, pulses=None):
        """发送红外信号"""
        data = pulses or self.recorded_signal
        if not data:
            return False

        if SIMULATION_MODE:
            print(f"Simulation: IR send {len(data)} pulses")
            return True

        if not self.pi:
            return False

        try:
            wf = []
            for i, pulse in enumerate(data):
                if i % 2 == 0:  # Mark (carrier)
                    cycles = int(pulse * 38 / 1000000)
                    for _ in range(cycles):
                        wf.append(pigpio.pulse(1 << self.tx_pin, 0, 13))
                        wf.append(pigpio.pulse(0, 1 << self.tx_pin, 13))
                else:  # Space
                    wf.append(pigpio.pulse(0, 0, pulse))

            import pigpio
            self.pi.wave_clear()
            self.pi.wave_add_generic(wf)
            wave_id = self.pi.wave_create()
            self.pi.wave_send_once(wave_id)
            while self.pi.wave_tx_busy():
                time.sleep(0.01)
            self.pi.wave_delete(wave_id)
            return True
        except Exception as e:
            print(f"IR send error: {e}")
            return False

    def send_nec(self, address, command):
        """发送NEC协议"""
        pulses = [9000, 4500]
        for byte in [address, ~address & 0xFF, command, ~command & 0xFF]:
            for i in range(8):
                pulses.append(560)
                pulses.append(1690 if byte & (1 << i) else 560)
        pulses.append(560)
        return self.send_signal(pulses)

    def send_power_off(self):
        """发送通用电源关闭信号"""
        return self.send_nec(0x00, 0x0C)

    def send_preset(self, preset_name):
        """发送预设遥控器信号"""
        if preset_name not in IR_DATABASE:
            return False
        return self.send_signal(IR_DATABASE[preset_name])

    def list_presets(self):
        """列出所有预设"""
        return list(IR_DATABASE.keys())

    def close(self):
        """清理资源"""
        if self.pi:
            self.pi.stop()
