import serial
import dicot  # Assuming this library is installed
from typing import Tuple, Optional

class BrushSensor:
    """Handles input from the Arduino brush sensor."""
    def __init__(self, port: str, baud_rate: int):
        try:
            self.ser = serial.Serial(port, baud_rate, timeout=1)
            print(f"Sensor connected on {port}")
        except serial.SerialException as e:
            print(f"Error connecting to Sensor on {port}: {e}")
            self.ser = None

    def read(self) -> Optional[Tuple[int, int]]:
        """Returns (right_val, left_val) or None."""
        if not self.ser: return None
        
        try:
            # Clear buffer to get latest data
            while self.ser.in_waiting > 10:
                self.ser.readline()
                
            line = self.ser.readline().decode('utf-8').strip()
            if line:
                parts = line.split(",")
                if len(parts) >= 2:
                    return int(parts[0]), int(parts[1])
        except Exception:
            pass
        return None

    def calibrate_baseline(self, samples=300) -> Tuple[int, int]:
        """Averages readings to find zero-point."""
        print("Calibrating sensor baseline...")
        r_tot, l_tot, count = 0, 0, 0
        for _ in range(samples):
            val = self.read()
            if val:
                r_tot += val[0]
                l_tot += val[1]
                count += 1
        if count == 0: return 0, 0
        return int(r_tot/count), int(l_tot/count)

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

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