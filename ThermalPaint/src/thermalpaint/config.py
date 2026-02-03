import csv
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Tuple

# --- Configuration Constants ---
COM_PORT_BRUSH = 'COM4'   # Arduino Sensor
COM_PORT_MOTOR = 'COM11'  # Dicot Motor
BAUD_RATE = 115200

# Buffer thresholds for detecting brush contact
BUFFER_RIGHT = 6
BUFFER_LEFT = 4

PARAMETERS_FILE = Path("data/parameters.csv")

@dataclass
class CalibrationParameters:
    """Stores calibration data and handles coordinate projection logic."""
    right_init_val: int = 549
    left_init_val: int = 529
    right_init_x: int = 410
    left_init_x: int = 255
    right_init_y: int = 210
    left_init_y: int = 210
    right_x_coeff: float = 4.6
    right_y_coeff: float = 0.0
    left_x_coeff: float = 6.0
    left_y_coeff: float = 0.0

    @classmethod
    def load_from_csv(cls, filename: Path) -> 'CalibrationParameters':
        try:
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
                if len(rows) < 2:
                    print(f"Warning: {filename} is empty or malformed. Using defaults.")
                    return cls()
                # Use the last row of data
                data = rows[-1] 
                return cls(
                    int(data[0]), int(data[1]), 
                    int(data[2]), int(data[3]), int(data[4]), int(data[5]),
                    float(data[6]), float(data[7]), float(data[8]), float(data[9])
                )
        except FileNotFoundError:
            print(f"Warning: {filename} not found. Using defaults.")
            return cls()

    def save_to_csv(self, filename: Path) -> None:
        data = asdict(self)
        # Round floats for cleaner CSV output
        for k, v in data.items():
            if isinstance(v, float):
                data[k] = round(v, 2)
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(list(data.keys()))
            writer.writerow(list(data.values()))
        print(f"Parameters saved to {filename}")

    def project_coordinates(self, sensor_val: int, is_right: bool, max_w: int, max_h: int) -> Tuple[int, int]:
        """Calculates screen coordinates based on sensor value and calibration."""
        if is_right:
            delta = sensor_val - self.right_init_val
            x = self.right_init_x + (delta * self.right_x_coeff)
            y = self.right_init_y + (delta * self.right_y_coeff)
        else:
            delta = sensor_val - self.left_init_val
            x = self.left_init_x - (delta * self.left_x_coeff)
            y = self.left_init_y - (delta * self.left_y_coeff)
        
        # Clamp to screen bounds
        return int(max(0, min(x, max_w - 1))), int(max(0, min(y, max_h - 1)))