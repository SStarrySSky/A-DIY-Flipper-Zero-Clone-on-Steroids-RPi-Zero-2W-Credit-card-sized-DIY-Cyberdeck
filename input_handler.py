"""
Input Handler for PiHacker device.
Handles button debouncing and event detection for 5-way navigation switch.
"""

import time
import threading
from config import Buttons, Timing, SIMULATION_MODE


class InputHandler:
    """Handles button input with debouncing and event callbacks."""

    def __init__(self):
        self.gpio = None
        self.last_press_time = {btn: 0 for btn in Buttons.ALL}
        self.button_states = {btn: False for btn in Buttons.ALL}
        self.callbacks = {btn: None for btn in Buttons.ALL}
        self._running = False
        self._poll_thread = None
        self._init_gpio()

    def _init_gpio(self):
        """Initialize GPIO for button input."""
        if SIMULATION_MODE:
            print("Simulation: Input handler initialized")
            print("  Use keyboard: w=UP, s=DOWN, a=LEFT, d=RIGHT, ENTER=SELECT")
            return

        try:
            import RPi.GPIO as GPIO
            self.gpio = GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)

            for pin in Buttons.ALL:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            print("Input: GPIO initialized successfully")
        except Exception as e:
            print(f"Input init failed: {e}, using simulation mode")
            self.gpio = None

    def read_button(self, button):
        """Read current state of a button (True if pressed)."""
        if SIMULATION_MODE or self.gpio is None:
            return False
        return self.gpio.input(button) == 0  # Active low

    def is_pressed(self, button):
        """Check if button is currently pressed with debouncing."""
        current_time = time.time()
        if current_time - self.last_press_time[button] < Timing.BUTTON_DEBOUNCE:
            return False

        if self.read_button(button):
            self.last_press_time[button] = current_time
            return True
        return False

    def wait_for_press(self, timeout=None):
        """Wait for any button press and return which button."""
        start_time = time.time()
        while True:
            for button in Buttons.ALL:
                if self.is_pressed(button):
                    return button
            if timeout and (time.time() - start_time) > timeout:
                return None
            time.sleep(0.01)

    def get_input(self):
        """Non-blocking check for button input. Returns button or None."""
        for button in Buttons.ALL:
            if self.is_pressed(button):
                return button
        return None

    def register_callback(self, button, callback):
        """Register a callback function for a button press."""
        self.callbacks[button] = callback

    def start_polling(self):
        """Start background polling thread."""
        if self._running:
            return
        self._running = True
        self._poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._poll_thread.start()

    def stop_polling(self):
        """Stop background polling thread."""
        self._running = False
        if self._poll_thread:
            self._poll_thread.join(timeout=1)

    def _poll_loop(self):
        """Background polling loop for button events."""
        while self._running:
            for button in Buttons.ALL:
                if self.is_pressed(button):
                    if self.callbacks[button]:
                        self.callbacks[button](button)
            time.sleep(0.01)

    def cleanup(self):
        """Clean up GPIO resources."""
        self.stop_polling()
        if self.gpio and not SIMULATION_MODE:
            try:
                self.gpio.cleanup()
            except:
                pass


class SimulatedInput:
    """Keyboard-based input for simulation/testing."""

    KEY_MAP = {
        'w': Buttons.UP,
        's': Buttons.DOWN,
        'a': Buttons.LEFT,
        'd': Buttons.RIGHT,
        '\r': Buttons.CENTER,
        '\n': Buttons.CENTER,
    }

    @classmethod
    def get_key(cls):
        """Get keyboard input (non-blocking where possible)."""
        try:
            import msvcrt
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8', errors='ignore').lower()
                return cls.KEY_MAP.get(key)
        except ImportError:
            pass
        return None
