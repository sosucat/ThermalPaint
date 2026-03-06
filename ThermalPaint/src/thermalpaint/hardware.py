import asyncio
import threading
import time
from bleak import BleakScanner, BleakClient
import dicot  # Assuming this library is installed
from typing import Tuple, Optional

# Bluetooth device name and characteristic UUID
DEVICE_NAME = "XIAO_Flex"
CHARACTERISTIC_UUID = "000019b2-0000-1000-8000-00805f9b34fb"

class BrushSensor:
    """Handles input from the Bluetooth brush sensor."""
    def __init__(self, device_name: str = DEVICE_NAME):
        self.device_name = device_name
        self.client = None
        self._angle = None  # Single angle value: -90 (left) to +90 (right)
        self._loop = None
        self._thread = None
        
        # Start a background thread with a persistent event loop
        self._start_background_loop()

    def _start_background_loop(self):
        """Start a background thread with an event loop for BLE operations."""
        self._loop = asyncio.new_event_loop()
        self._stop_event = asyncio.Event()
        
        def run_loop():
            asyncio.set_event_loop(self._loop)
            self._loop.run_forever()
        
        self._thread = threading.Thread(target=run_loop, daemon=True)
        self._thread.start()
        
        # Schedule the connection in the background loop
        future = asyncio.run_coroutine_threadsafe(self._connect(), self._loop)
        # Wait for connection to complete (with timeout)
        try:
            future.result(timeout=10)
        except Exception as e:
            print(f"Error connecting to Bluetooth sensor: {e}")

    async def _connect(self):
        """Connect to the Bluetooth sensor device."""
        print(f"Scanning for {self.device_name}...")
        device = await BleakScanner.find_device_by_name(self.device_name)
        
        if device is None:
            print(f"Could not find {self.device_name}. Is the board powered on?")
            return

        print(f"Found {self.device_name} at {device.address}! Connecting...")
        
        self.client = BleakClient(device)
        await self.client.connect()
        print("Bluetooth sensor connected!")
        
        # Subscribe to notifications
        await self.client.start_notify(CHARACTERISTIC_UUID, self._notification_handler)

    def _notification_handler(self, sender, data):
        """Callback that runs when new sensor data arrives."""
        try:
            # Data arrives as raw bytes, decode to text string
            # New format: single angle value from -90 to +90 (can be float)
            data_str = data.decode('utf-8').strip()
            self._angle = int(float(data_str))  # Parse as float first, then convert to int
        except Exception as e:
            print(f"Error parsing sensor data: {e}")

    def read(self) -> Optional[int]:
        """Returns the bend angle (-90 to +90) or None."""
        # Since we get data asynchronously via notifications,
        # we just return the latest value stored by the callback
        return self._angle

    def calibrate_baseline(self, samples=300) -> int:
        """Averages readings to find zero-point (neutral position)."""
        print("Calibrating sensor baseline...")
        total, count = 0, 0
        for _ in range(samples):
            val = self.read()
            if val is not None:
                total += val
                count += 1
            time.sleep(0.01)  # Small delay between samples
        if count == 0: return 0
        return int(total / count)

    def close(self):
        """Disconnect and cleanup."""
        if self.client and self.client.is_connected:
            try:
                asyncio.run_coroutine_threadsafe(
                    self.client.disconnect(), self._loop
                ).result(timeout=5)
            except Exception as e:
                print(f"Error disconnecting: {e}")
        
        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)

class BlindMotor:
    """Handles output to the ThermoBlind motors."""
    def __init__(self, port: str):
        try:
            self.cnx = dicot.open(port)
            self.motor = self.cnx.motor(1)
            self.motor.torque_enabled = True
            print(f"Motor connected on {port}")
        except Exception as e:
            print(f"Error connecting to Motor on {port}: {e}")
            self.cnx = None

    def set_angle(self, angle: float):
        if self.cnx:
            self.motor.angle = angle

    def close(self):
        if self.cnx:
            self.cnx.close()