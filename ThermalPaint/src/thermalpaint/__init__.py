#!/usr/bin/env python
"""
ThermalPaint Runtime
Detects brush strokes, samples color, and controls ThermoBlinds.
"""

import cv2
import sys
from config import CalibrationParameters, PARAMETERS_FILE, COM_PORT_BRUSH, COM_PORT_MOTOR, BAUD_RATE, BUFFER_RIGHT, BUFFER_LEFT
from hardware import BrushSensor, BlindMotor
from utils import rgb_to_blind_angle

def main():
    # 1. Setup Hardware & Config
    params = CalibrationParameters.load_from_csv(PARAMETERS_FILE)
    sensor = BrushSensor(COM_PORT_BRUSH, BAUD_RATE)
    blinds = BlindMotor(COM_PORT_MOTOR)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not found.")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print("ThermalPaint Runtime Started. Press 'q' to exit.")

    try:
        while True:
            # 2. Read Inputs
            sensor_vals = sensor.read()
            ret, frame = cap.read()
            
            if not ret or not sensor_vals:
                continue

            r_val, l_val = sensor_vals
            
            # 3. Determine State & Position
            is_painting = False
            x, y = 0, 0
            
            # Check Right Swipe
            if r_val > params.right_init_val + BUFFER_RIGHT:
                # print("State: Right")
                x, y = params.project_coordinates(r_val, True, width, height)
                is_painting = True
                
            # Check Left Swipe
            elif l_val > params.left_init_val + BUFFER_LEFT:
                # print("State: Left")
                x, y = params.project_coordinates(l_val, False, width, height)
                is_painting = True
            
            # 4. Process Logic
            target_angle = 10.0 # Default closed angle
            debug_color = (0, 0, 0)

            if is_painting:
                # Sample Color
                b, g, r = frame[y, x]
                debug_color = (int(b), int(g), int(r))
                
                # Convert to Angle
                target_angle = rgb_to_blind_angle(r, g, b)

            # 5. Actuate Output
            blinds.set_angle(target_angle)

            # 6. Visualization
            if is_painting:
                # Draw target circle
                cv2.circle(frame, (x, y), 24, (0, 255, 0), -1)
                cv2.circle(frame, (x, y), 20, debug_color, -1)
                
                # Draw text info
                info = f"Angle: {target_angle:.1f}deg"
                cv2.putText(frame, info, (x + 30, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow("ThermalPaint Runtime", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        # Cleanup
        sensor.close()
        blinds.close()
        cap.release()
        cv2.destroyAllWindows()
        print("Goodbye.")

if __name__ == "__main__":
    main()