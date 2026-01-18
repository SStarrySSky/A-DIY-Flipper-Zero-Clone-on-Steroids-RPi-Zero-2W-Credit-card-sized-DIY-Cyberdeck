"""
Configuration file for PiHacker device.
Contains all pin definitions, constants, and hardware settings.
"""

# =============================================================================
# SIMULATION MODE DETECTION
# =============================================================================
import platform
import os

def is_raspberry_pi():
    """Detect if running on Raspberry Pi hardware."""
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            return 'BCM' in cpuinfo or 'Raspberry' in cpuinfo
    except:
        return False

SIMULATION_MODE = not is_raspberry_pi()
PLATFORM = platform.system()

# =============================================================================
# GPIO PIN DEFINITIONS (BCM Numbering)
# =============================================================================

# 5-Way Navigation Switch (Active Low - Pull-up required)
class Buttons:
    UP = 17
    DOWN = 27
    LEFT = 22
    RIGHT = 23
    CENTER = 24  # Enter/Select

    ALL = [UP, DOWN, LEFT, RIGHT, CENTER]
    NAMES = {UP: 'UP', DOWN: 'DOWN', LEFT: 'LEFT', RIGHT: 'RIGHT', CENTER: 'CENTER'}

# I2C Configuration
class I2C:
    SDA = 2
    SCL = 3
    BUS = 1  # /dev/i2c-1

# OLED Display (SH1106)
class Display:
    WIDTH = 128
    HEIGHT = 64
    I2C_ADDRESS = 0x3C
    DRIVER = 'sh1106'

# SPI Configuration (CC1101 Radio Modules)
class SPI:
    MOSI = 10
    MISO = 9
    SCLK = 11
    BUS = 0

    # Chip Select pins
    CS_MODULE_A = 8   # CE0 - Jammer/TX
    CS_MODULE_B = 7   # CE1 - Sniffer/RX

# NFC Module (PN532)
class NFC:
    I2C_ADDRESS = 0x24  # Default PN532 I2C address
    IRQ_PIN = None      # Optional IRQ pin
    RESET_PIN = None    # Optional reset pin

# Infrared
class IR:
    TX_PIN = 5
    RX_PIN = 6
    CARRIER_FREQ = 38000  # 38kHz carrier frequency

# Status LEDs
class LED:
    LED1 = 12  # Red
    LED2 = 16  # Yellow
    LED3 = 20  # Green
    ALL = [LED1, LED2, LED3]

# =============================================================================
# UI CONFIGURATION
# =============================================================================

class UI:
    # Fonts
    FONT_SIZE_SMALL = 8
    FONT_SIZE_MEDIUM = 10
    FONT_SIZE_LARGE = 12

    # Menu settings
    MENU_ITEMS_VISIBLE = 4
    SCROLL_SPEED = 1

    # Status bar
    STATUS_BAR_HEIGHT = 12

    # Colors (for OLED: 0=black, 255=white)
    COLOR_BG = 0
    COLOR_FG = 255
    COLOR_HIGHLIGHT = 255

    # Animation
    FRAME_RATE = 30
    DEBOUNCE_MS = 200

# =============================================================================
# TIMING CONSTANTS
# =============================================================================

class Timing:
    BUTTON_DEBOUNCE = 0.15  # seconds
    MENU_SCROLL_DELAY = 0.1
    SCREEN_REFRESH = 0.033  # ~30 FPS
    SIGNAL_SAMPLE_RATE = 1000000  # 1MHz for Sub-GHz

# =============================================================================
# SUB-GHZ CONFIGURATION
# =============================================================================

class SubGHz:
    # Common frequencies (in Hz)
    FREQ_315MHZ = 315000000
    FREQ_433MHZ = 433920000
    FREQ_868MHZ = 868000000
    FREQ_915MHZ = 915000000

    DEFAULT_FREQ = FREQ_433MHZ

    # CC1101 Register defaults
    MODULATION_ASK = 0x30
    MODULATION_FSK = 0x00
    MODULATION_GFSK = 0x10

    # Data rates
    BAUD_RATE = 4800

# =============================================================================
# IR PROTOCOL DEFINITIONS
# =============================================================================

class IRProtocols:
    NEC = 'NEC'
    RC5 = 'RC5'
    RC6 = 'RC6'
    SONY = 'SONY'
    SAMSUNG = 'SAMSUNG'

    # Common power codes (NEC format)
    POWER_CODES = {
        'samsung_tv': {'protocol': 'NEC', 'address': 0x07, 'command': 0x02},
        'lg_tv': {'protocol': 'NEC', 'address': 0x04, 'command': 0x08},
        'sony_tv': {'protocol': 'SONY', 'address': 0x01, 'command': 0x15},
        'generic': {'protocol': 'NEC', 'address': 0x00, 'command': 0x0C},
    }

# =============================================================================
# SYSTEM PATHS
# =============================================================================

class Paths:
    DATA_DIR = '/home/pi/pihacker/data'
    SIGNALS_DIR = '/home/pi/pihacker/data/signals'
    NFC_DIR = '/home/pi/pihacker/data/nfc'
    IR_DIR = '/home/pi/pihacker/data/ir'
    LOGS_DIR = '/home/pi/pihacker/logs'
