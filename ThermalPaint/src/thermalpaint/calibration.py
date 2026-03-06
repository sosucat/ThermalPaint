import cv2
import time
import keyboard
import sys
from config import CalibrationParameters, PARAMETERS_FILE, COM_PORT_BRUSH, BAUD_RATE
from hardware import BrushSensor

class CalibrationApp:
    def __init__(self):
        self.params = CalibrationParameters()
        self.sensor = BrushSensor()
        self.cap = cv2.VideoCapture(0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def run(self):
        print("Starting Calibration...")
        self._calibrate_baseline()
        
        steps = [
            ("Right Position", self._logic_pos_right, False),
            ("Left Position", self._logic_pos_left, False),
            ("Right Coefficient", self._logic_coeff_right, True),
            ("Left Coefficient", self._logic_coeff_left, True)
        ]

        for name, logic, use_sensor in steps:
            print(f"\n--- Calibrating: {name} ---")
            print("Use ARROWS to adjust. ENTER to confirm.")
            if use_sensor:
                print("Bend the brush to the right/left position.")
            self._visual_loop(logic, use_sensor)
            time.sleep(0.5)

        self.params.save_to_csv(PARAMETERS_FILE)
        self._cleanup()

    def _calibrate_baseline(self):
        # Countdown - hold brush in neutral position
        for i in range(5, 0, -1):
            print(f"Hold brush in neutral position... {i}", end='\r')
            time.sleep(1)
        baseline = self.sensor.calibrate_baseline()
        # Single baseline value (neutral position, typically 0)
        self.params.baseline_val = baseline
        print(f"\nBaseline Set: {baseline} (neutral position)")

    def _visual_loop(self, logic_func, use_sensor):
        while True:
            if keyboard.is_pressed('enter'): break
            keys = {
                'right': keyboard.is_pressed('right'), 'left': keyboard.is_pressed('left'),
                'up': keyboard.is_pressed('up'), 'down': keyboard.is_pressed('down')
            }
            
            sensor_angle = self.sensor.read() if use_sensor else None
            
            x, y = logic_func(keys, sensor_angle)
            
            # Draw
            ret, frame = self.cap.read()
            if not ret: break
            
            # Safe pixel access
            x = max(0, min(x, self.width-1))
            y = max(0, min(y, self.height-1))
            
            b, g, r = frame[y, x]
            cv2.circle(frame, (x, y), 24, (0, 255, 0), -1)
            cv2.circle(frame, (x, y), 20, (int(b), int(g), int(r)), -1)
            cv2.imshow("Calibration", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): sys.exit()

    # Logic Handlers
    def _logic_pos_right(self, k, s):
        if k['right']: self.params.right_init_x += 3
        if k['left']: self.params.right_init_x -= 3
        if k['up']: self.params.right_init_y -= 3
        if k['down']: self.params.right_init_y += 3
        return self.params.right_init_x, self.params.right_init_y

    def _logic_pos_left(self, k, s):
        if k['right']: self.params.left_init_x += 3
        if k['left']: self.params.left_init_x -= 3
        if k['up']: self.params.left_init_y -= 3
        if k['down']: self.params.left_init_y += 3
        return self.params.left_init_x, self.params.left_init_y

    def _logic_coeff_right(self, k, s):
        if k['right']: self.params.right_x_coeff += 0.1
        if k['left']: self.params.right_x_coeff -= 0.1
        if k['up']: self.params.right_y_coeff -= 0.1
        if k['down']: self.params.right_y_coeff += 0.1
        # For right: use positive angle from baseline
        if s is not None:
            return self.params.project_coordinates(s, True, self.width, self.height)
        return self.params.right_init_x, self.params.right_init_y

    def _logic_coeff_left(self, k, s):
        if k['right']: self.params.left_x_coeff += 0.1
        if k['left']: self.params.left_x_coeff -= 0.1
        if k['up']: self.params.left_y_coeff -= 0.1
        if k['down']: self.params.left_y_coeff += 0.1
        # For left: use absolute value of negative angle
        if s is not None:
            return self.params.project_coordinates(abs(s), False, self.width, self.height)
        return self.params.left_init_x, self.params.left_init_y

    def _cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.sensor.close()

if __name__ == "__main__":
    CalibrationApp().run()
