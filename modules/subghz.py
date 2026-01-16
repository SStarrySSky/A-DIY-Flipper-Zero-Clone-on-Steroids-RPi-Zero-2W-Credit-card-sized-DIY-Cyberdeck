"""
Sub-GHz Module for PiHacker device.
Complete CC1101 driver with signal recording, replay, and jamming.
Based on pycc1101 and RPi-CC1101 implementations.
"""

import time
import random
import threading
from config import SPI, SubGHz, SIMULATION_MODE


# CC1101 Command Strobes
SRES = 0x30    # Reset chip
SFSTXON = 0x31 # Enable and calibrate frequency synthesizer
SXOFF = 0x32   # Turn off crystal oscillator
SCAL = 0x33    # Calibrate frequency synthesizer
SRX = 0x34     # Enable RX
STX = 0x35     # Enable TX
SIDLE = 0x36   # Exit RX/TX, turn off frequency synthesizer
SWOR = 0x38    # Start automatic RX polling sequence
SPWD = 0x39    # Enter power down mode
SFRX = 0x3A    # Flush the RX FIFO buffer
SFTX = 0x3B    # Flush the TX FIFO buffer
SWORRST = 0x3C # Reset real time clock
SNOP = 0x3D    # No operation

# CC1101 Register Addresses
IOCFG2 = 0x00   # GDO2 output pin configuration
IOCFG1 = 0x01   # GDO1 output pin configuration
IOCFG0 = 0x02   # GDO0 output pin configuration
FIFOTHR = 0x03  # RX FIFO and TX FIFO thresholds
SYNC1 = 0x04    # Sync word, high byte
SYNC0 = 0x05    # Sync word, low byte
PKTLEN = 0x06   # Packet length
PKTCTRL1 = 0x07 # Packet automation control
PKTCTRL0 = 0x08 # Packet automation control
ADDR = 0x09     # Device address
CHANNR = 0x0A   # Channel number
FSCTRL1 = 0x0B  # Frequency synthesizer control
FSCTRL0 = 0x0C  # Frequency synthesizer control
FREQ2 = 0x0D    # Frequency control word, high byte
FREQ1 = 0x0E    # Frequency control word, middle byte
FREQ0 = 0x0F    # Frequency control word, low byte
MDMCFG4 = 0x10  # Modem configuration
MDMCFG3 = 0x11  # Modem configuration
MDMCFG2 = 0x12  # Modem configuration
MDMCFG1 = 0x13  # Modem configuration
MDMCFG0 = 0x14  # Modem configuration
DEVIATN = 0x15  # Modem deviation setting
MCSM2 = 0x16    # Main Radio Control State Machine configuration
MCSM1 = 0x17    # Main Radio Control State Machine configuration
MCSM0 = 0x18    # Main Radio Control State Machine configuration
FOCCFG = 0x19   # Frequency Offset Compensation configuration
BSCFG = 0x1A    # Bit Synchronization configuration
AGCCTRL2 = 0x1B # AGC control
AGCCTRL1 = 0x1C # AGC control
AGCCTRL0 = 0x1D # AGC control
WOREVT1 = 0x1E  # High byte Event 0 timeout
WOREVT0 = 0x1F  # Low byte Event 0 timeout
WORCTRL = 0x20  # Wake On Radio control
FREND1 = 0x21   # Front end RX configuration
FREND0 = 0x22   # Front end TX configuration
FSCAL3 = 0x23   # Frequency synthesizer calibration
FSCAL2 = 0x24   # Frequency synthesizer calibration
FSCAL1 = 0x25   # Frequency synthesizer calibration
FSCAL0 = 0x26   # Frequency synthesizer calibration
RCCTRL1 = 0x27  # RC oscillator configuration
RCCTRL0 = 0x28  # RC oscillator configuration
FSTEST = 0x29   # Frequency synthesizer calibration control
PTEST = 0x2A    # Production test
AGCTEST = 0x2B  # AGC test
TEST2 = 0x2C    # Various test settings
TEST1 = 0x2D    # Various test settings
TEST0 = 0x2E    # Various test settings

# Status Registers (burst read)
PARTNUM = 0x30  # Part number
VERSION = 0x31  # Current version number
FREQEST = 0x32  # Frequency offset estimate
LQI = 0x33      # Demodulator estimate for Link Quality
RSSI = 0x34     # Received signal strength indication
MARCSTATE = 0x35 # Control state machine state
WORTIME1 = 0x36 # High byte of WOR timer
WORTIME0 = 0x37 # Low byte of WOR timer
PKTSTATUS = 0x38 # Current GDOx status and packet status
VCO_VC_DAC = 0x39 # Current setting from PLL calibration module
TXBYTES = 0x3A  # Underflow and number of bytes in TX FIFO
RXBYTES = 0x3B  # Overflow and number of bytes in RX FIFO

# FIFO Addresses
TX_FIFO = 0x3F
RX_FIFO = 0x3F
PA_TABLE = 0x3E

# 433.92MHz OOK配置表 (用于车库门、遥控器等)
CONFIG_433MHZ_OOK = [
    (IOCFG2, 0x0D),    # GDO2 输出串行数据
    (IOCFG0, 0x0D),    # GDO0 输出串行数据
    (FIFOTHR, 0x47),   # RX FIFO阈值
    (PKTCTRL0, 0x32),  # 异步串行模式，无CRC
    (FSCTRL1, 0x06),   # IF频率
    (FREQ2, 0x10),     # 433.92MHz高字节
    (FREQ1, 0xB0),     # 433.92MHz中字节
    (FREQ0, 0x71),     # 433.92MHz低字节
    (MDMCFG4, 0xF5),   # 信道带宽
    (MDMCFG3, 0x83),   # 数据速率
    (MDMCFG2, 0x30),   # OOK调制，无同步字
    (MDMCFG1, 0x00),   # 信道间隔
    (MDMCFG0, 0x00),
    (MCSM0, 0x18),     # 自动校准
    (FOCCFG, 0x16),
    (AGCCTRL2, 0x43),
    (AGCCTRL1, 0x49),
    (AGCCTRL0, 0x91),
    (WORCTRL, 0xFB),
    (FREND1, 0x56),
    (FREND0, 0x11),    # PA功率设置
    (FSCAL3, 0xE9),
    (FSCAL2, 0x2A),
    (FSCAL1, 0x00),
    (FSCAL0, 0x1F),
    (TEST2, 0x81),
    (TEST1, 0x35),
    (TEST0, 0x09),
]

# 315MHz OOK配置表
CONFIG_315MHZ_OOK = [
    (IOCFG2, 0x0D),
    (IOCFG0, 0x0D),
    (FIFOTHR, 0x47),
    (PKTCTRL0, 0x32),
    (FSCTRL1, 0x06),
    (FREQ2, 0x0C),     # 315MHz高字节
    (FREQ1, 0x1D),     # 315MHz中字节
    (FREQ0, 0x89),     # 315MHz低字节
    (MDMCFG4, 0xF5),
    (MDMCFG3, 0x83),
    (MDMCFG2, 0x30),
    (MDMCFG1, 0x00),
    (MDMCFG0, 0x00),
    (MCSM0, 0x18),
    (FOCCFG, 0x16),
    (AGCCTRL2, 0x43),
    (AGCCTRL1, 0x49),
    (AGCCTRL0, 0x91),
    (WORCTRL, 0xFB),
    (FREND1, 0x56),
    (FREND0, 0x11),
    (FSCAL3, 0xE9),
    (FSCAL2, 0x2A),
    (FSCAL1, 0x00),
    (FSCAL0, 0x1F),
    (TEST2, 0x81),
    (TEST1, 0x35),
    (TEST0, 0x09),
]

# PA功率表 (最大功率)
PA_TABLE_OOK = [0x00, 0xC0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]


class CC1101:
    """完整的CC1101驱动"""

    def __init__(self, cs_pin, gdo0_pin=None, name="CC1101"):
        self.cs_pin = cs_pin
        self.gdo0_pin = gdo0_pin
        self.name = name
        self.spi = None
        self.gpio = None
        self.frequency = SubGHz.DEFAULT_FREQ
        self.initialized = False
        self._init_hardware()

    def _init_hardware(self):
        """初始化SPI和GPIO"""
        if SIMULATION_MODE:
            print(f"Simulation: {self.name} initialized (CS=GPIO{self.cs_pin})")
            self.initialized = True
            return

        try:
            import spidev
            import RPi.GPIO as GPIO
            self.gpio = GPIO
            self.spi = spidev.SpiDev()
            device = 0 if self.cs_pin == SPI.CS_MODULE_A else 1
            self.spi.open(SPI.BUS, device)
            self.spi.max_speed_hz = 55000
            self.spi.mode = 0

            if self.gdo0_pin:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.gdo0_pin, GPIO.IN)

            self._reset()
            self._configure_433mhz()
            self.initialized = True
            print(f"{self.name}: Initialized OK")
        except Exception as e:
            print(f"{self.name} init failed: {e}")
            self.initialized = False

    def _reset(self):
        """复位CC1101芯片"""
        if not self.spi:
            return
        self.spi.xfer([SRES])
        time.sleep(0.01)
        while self._read_status(MARCSTATE) != 0x01:
            time.sleep(0.001)

    def _write_reg(self, addr, value):
        """写单个寄存器"""
        if self.spi:
            self.spi.xfer([addr | 0x00, value])

    def _read_reg(self, addr):
        """读单个寄存器"""
        if self.spi:
            result = self.spi.xfer([addr | 0x80, 0x00])
            return result[1]
        return 0

    def _read_status(self, addr):
        """读状态寄存器"""
        if self.spi:
            result = self.spi.xfer([addr | 0xC0, 0x00])
            return result[1]
        return 0

    def _strobe(self, cmd):
        """发送命令"""
        if self.spi:
            self.spi.xfer([cmd])

    def _write_burst(self, addr, data):
        """批量写入"""
        if self.spi:
            self.spi.xfer([addr | 0x40] + list(data))

    def _configure_433mhz(self):
        """配置433.92MHz OOK模式"""
        for reg, val in CONFIG_433MHZ_OOK:
            self._write_reg(reg, val)
        self._write_burst(PA_TABLE, PA_TABLE_OOK)
        self.frequency = 433920000

    def _configure_315mhz(self):
        """配置315MHz OOK模式"""
        for reg, val in CONFIG_315MHZ_OOK:
            self._write_reg(reg, val)
        self._write_burst(PA_TABLE, PA_TABLE_OOK)
        self.frequency = 315000000

    def set_frequency(self, freq_hz):
        """设置频率"""
        if SIMULATION_MODE:
            print(f"Simulation: {self.name} freq={freq_hz/1e6:.2f}MHz")
            self.frequency = freq_hz
            return True
        if freq_hz == 315000000:
            self._configure_315mhz()
        else:
            self._configure_433mhz()
        return True

    def get_rssi(self):
        """读取RSSI值"""
        if SIMULATION_MODE:
            return random.randint(-90, -30)
        rssi = self._read_status(RSSI)
        if rssi >= 128:
            rssi = (rssi - 256) / 2 - 74
        else:
            rssi = rssi / 2 - 74
        return int(rssi)

    def set_rx_mode(self):
        """进入接收模式"""
        if self.spi:
            self._strobe(SIDLE)
            self._strobe(SFRX)
            self._strobe(SRX)

    def set_tx_mode(self):
        """进入发送模式"""
        if self.spi:
            self._strobe(SIDLE)
            self._strobe(SFTX)
            self._strobe(STX)

    def set_idle(self):
        """进入空闲模式"""
        if self.spi:
            self._strobe(SIDLE)

    def close(self):
        """关闭SPI连接"""
        if self.spi:
            self.set_idle()
            self.spi.close()


class SubGHzModule:
    """高级Sub-GHz操作管理器"""

    def __init__(self, gdo0_rx=24, gdo0_tx=25):
        self.gdo0_rx = gdo0_rx
        self.gdo0_tx = gdo0_tx
        self.tx_radio = CC1101(SPI.CS_MODULE_A, gdo0_tx, "TX")
        self.rx_radio = CC1101(SPI.CS_MODULE_B, gdo0_rx, "RX")
        self.recorded_signal = []
        self.is_recording = False
        self.is_jamming = False
        self._record_thread = None

    def set_frequency(self, freq_hz):
        """设置两个模块的频率"""
        self.tx_radio.set_frequency(freq_hz)
        self.rx_radio.set_frequency(freq_hz)

    def record_signal(self, duration=5.0, callback=None):
        """录制信号 - 通过GPIO中断捕获脉冲"""
        self.recorded_signal = []

        if SIMULATION_MODE:
            print(f"Simulation: Recording for {duration}s")
            for i in range(int(duration * 10)):
                pulse = random.randint(200, 2000)
                self.recorded_signal.append(pulse)
                if callback:
                    callback(i / (duration * 10) * 100)
                time.sleep(0.1)
            return self.recorded_signal

        # 真实硬件录制
        try:
            import RPi.GPIO as GPIO
            self.rx_radio.set_rx_mode()
            self.is_recording = True
            last_time = time.time()
            last_state = GPIO.input(self.gdo0_rx)
            end_time = time.time() + duration

            while time.time() < end_time and self.is_recording:
                state = GPIO.input(self.gdo0_rx)
                if state != last_state:
                    pulse = int((time.time() - last_time) * 1000000)
                    self.recorded_signal.append(pulse)
                    last_time = time.time()
                    last_state = state
                time.sleep(0.000001)

            self.rx_radio.set_idle()
            self.is_recording = False
        except Exception as e:
            print(f"Record error: {e}")

        return self.recorded_signal

    def replay_signal(self):
        """回放录制的信号"""
        if not self.recorded_signal:
            print("No signal to replay")
            return False

        if SIMULATION_MODE:
            print(f"Simulation: Replay {len(self.recorded_signal)} pulses")
            return True

        # 真实硬件回放
        try:
            import RPi.GPIO as GPIO
            GPIO.setup(self.gdo0_tx, GPIO.OUT)
            self.tx_radio.set_tx_mode()
            state = True

            for pulse_us in self.recorded_signal:
                GPIO.output(self.gdo0_tx, state)
                time.sleep(pulse_us / 1000000.0)
                state = not state

            GPIO.output(self.gdo0_tx, False)
            self.tx_radio.set_idle()
            return True
        except Exception as e:
            print(f"Replay error: {e}")
            return False

    def start_jamming(self):
        """开始干扰"""
        self.is_jamming = True
        if SIMULATION_MODE:
            print("Simulation: Jamming started")
            return True
        self.tx_radio.set_tx_mode()
        return True

    def stop_jamming(self):
        """停止干扰"""
        self.is_jamming = False
        if SIMULATION_MODE:
            print("Simulation: Jamming stopped")
        self.tx_radio.set_idle()
        return True

    def rolljam_attack(self, callback=None):
        """RollJam攻击"""
        if SIMULATION_MODE:
            print("Simulation: RollJam")
            if callback:
                callback("Jamming...")
            time.sleep(1)
            self.recorded_signal = [500, 1000] * 20
            if callback:
                callback("Captured!")
            return True
        self.start_jamming()
        self.record_signal(duration=3.0)
        self.stop_jamming()
        return True

    def get_rssi_stream(self, count=50):
        """获取RSSI数据流"""
        values = []
        for _ in range(count):
            values.append(abs(self.rx_radio.get_rssi()))
        return values

    def close(self):
        """清理资源"""
        self.tx_radio.close()
        self.rx_radio.close()
