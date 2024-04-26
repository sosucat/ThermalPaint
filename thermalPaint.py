#!/usr/bin/env python
# This script detect colors the ThermalPaint brush is painting and control the angle of ThermoBlinds accordingly.
# Usage: python thermalPaint.py
__author__ = "Sosuke Ichihashi"
__copyright__ = "Copyright 2023, The ThermalPaint Project"
__credits__ = ["Sosuke Ichihashi"]
__maintainer__ = "Sosuke Ichihashi"
__email__ = "sichihashi3@gatech.edu"


import serial
import cv2
import dicot
import csv
import math

# Obtain heat intensity (i.e., angle of ThermoBlinds) from the RGB color values.
def color2angle(red, green, blue):
    min = min(red, green, blue)
    max = max(red, green, blue)
    if min == max:
        hue = 0.0
    if max == red:
        hue = (green - blue) / (max - min)
    elif max == green:
        hue = 2.0 + (blue - red) / (max - min)
    else:
        hue = 4.0 + (red - green) / (max - min)
    
    hue = hue * 60
    if hue < -30:
        hue = hue + 360
    
    ang = math.degrees(math.acos(1 - (330 - hue)/360))
    
    if ang > 90:
        ang = 90
    if ang < 10:
        ang = 10
        
    return ang


# Buffer between the initial sensor values and the paint detection values.
right_buffer = 6
left_buffer = 4

# Open COM ports and apply torque to the servo motors on ThermoBlinds.
ser = serial.Serial('COM16', 115200)
cnx = dicot.open('COM3')
motor = cnx.motor(1)
motor.torque_enabled = True

# Read the parameter values.
filename = "parameters.csv"
with open(filename, mode ='r')as file:
  csvFile = csv.reader(file)
  for line in csvFile:
      parameter_values = line# I just want the last line.
  right_init_val = int(parameter_values[0])
  left_init_val = int(parameter_values[1])
  right_init_x = int(parameter_values[2])
  left_init_x = int(parameter_values[3])
  right_init_y =int(parameter_values[4])
  left_init_y = int(parameter_values[5])
  right_x_coeff = float(parameter_values[6])
  right_y_coeff =float(parameter_values[7])
  left_x_coeff = float(parameter_values[8])
  left_y_coeff = float(parameter_values[9])

# Open a video stream (change the id to the one for the webcam on the brush.)
cap = cv2.VideoCapture(0)
cap_width = cap.get(3)
cap_height = cap.get(4)

# Main loop
while True:
    try:
        # Clear the input buffer before attempting to read the latest values from the Arduino
        while ser.in_waiting > 10:
            ser.readline()

        # Read a frame from the video stream
        ret, frame = cap.read()

        # Read a line from the serial input
        line = ser.readline().decode('utf-8').rstrip()
        # Convert it to an array of values
        if len(line) > 0:
            values = [int(val) for val in line.split(",")]
            # print(values)

        # Detect right and left swipes
        if values[0] > right_init_val + right_buffer:
            print("right")
            # Get the RGB value of the specified pixel in the frame
            x = right_init_x + (values[0] - right_init_val) * right_x_coeff
            y = right_init_y + (values[0] - right_init_val) * right_y_coeff
            x = int(max(min(x, cap_width-1), 0))
            y = int(max(min(y, cap_height-1), 0))
            blue, green, red = frame[y, x]
            motor.angle = color2angle(red, green, blue)
        elif values[1] > left_init_val + left_buffer:
            print("left")
            # Get the RGB value of the specified pixel in the frame
            x = left_init_x - (values[1] - left_init_val) * left_x_coeff
            y = left_init_y - (values[1] - left_init_val) * left_y_coeff
            x = int(max(min(x, cap_width-1), 0))
            y = int(max(min(y, cap_height-1), 0))
            blue, green, red = frame[y, x]
            motor.angle = color2angle(red, green, blue)
        else:
            print("none")
            x = 0
            y = 0
            blue, green, red = 0, 0, 0
            motor.angle = 10

        # Show the frame with a circle around the specified pixel
        cv2.circle(frame, (x, y), 24, (0, 255, 0), -1)
        cv2.circle(frame, (x, y), 20, (int(blue), int(green), int(red)), -1)
        cv2.imshow("Video", frame)

        # Wait for a key press and exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except KeyboardInterrupt:
        break

print("bye")
# Release the video stream and close all windows
cnx.close()
cap.release()
cv2.destroyAllWindows()
