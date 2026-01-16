"""
LED Status Module for PiHacker.
Controls 3 status LEDs with chase/blink effects.
"""

import time
import threading
from config import SIMULATION_MODE


class LEDController:
    """Controls status LEDs with various effects."""

    # LED GPIO pins
    LED1 = 12  # Red
    LED2 = 16  # Yellow
    LED3 = 20  # Green

    def __init__(self):
        self.pins = [self.LED1, self.LED2, self.LED3]
        self.running = False
        self.thread = None
        self._init_gpio()

    def _init_gpio(self):
        """Initialize GPIO for LEDs."""
        if SIMULATION_MODE:
            print("LED: Simulation mode")
            return

        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            for pin in self.pins:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.LOW)
            print("LED: GPIO initialized")
        except Exception as e:
            print(f"LED: Init failed - {e}")

    def _set_led(self, index, state):
        """Set single LED state."""
        if index < 0 or index >= len(self.pins):
            return

        if SIMULATION_MODE:
            symbol = "●" if state else "○"
            colors = ["红", "黄", "绿"]
            print(f"LED{index+1}({colors[index]}): {symbol}")
            return

        try:
            import RPi.GPIO as GPIO
            GPIO.output(self.pins[index], GPIO.HIGH if state else GPIO.LOW)
        except:
            pass

    def all_off(self):
        """Turn off all LEDs."""
        for i in range(len(self.pins)):
            self._set_led(i, False)

    def all_on(self):
        """Turn on all LEDs."""
        for i in range(len(self.pins)):
            self._set_led(i, True)

    def chase(self, speed=0.1):
        """Single chase cycle: LEDs light up one by one."""
        for i in range(len(self.pins)):
            self.all_off()
            self._set_led(i, True)
            time.sleep(speed)

    def _chase_loop(self, speed):
        """Internal chase loop for threading."""
        while self.running:
            self.chase(speed)

    def start_chase(self, speed=0.1):
        """Start continuous chase effect in background."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._chase_loop, args=(speed,))
        self.thread.daemon = True
        self.thread.start()

    def stop_chase(self):
        """Stop chase effect."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        self.all_off()

    def blink_all(self, times=3, speed=0.2):
        """Blink all LEDs together."""
        for _ in range(times):
            self.all_on()
            time.sleep(speed)
            self.all_off()
            time.sleep(speed)

    def success(self):
        """Green LED blink for success."""
        self._set_led(2, True)
        time.sleep(0.5)
        self._set_led(2, False)

    def error(self):
        """Red LED blink for error."""
        self._set_led(0, True)
        time.sleep(0.5)
        self._set_led(0, False)

    def cleanup(self):
        """Cleanup GPIO."""
        self.stop_chase()
        self.all_off()
