#!/usr/bin/env python
# This script calibrates the parameters used for ThermalPaint Brush.
# Usage: python calibration.py
__author__ = "Sosuke Ichihashi"
__copyright__ = "Copyright 2023, The ThermalPaint Project"
__credits__ = ["Sosuke Ichihashi"]
__maintainer__ = "Sosuke Ichihashi"
__email__ = "sichihashi3@gatech.edu"


import serial
import cv2
import time
import keyboard
import csv


ser = serial.Serial('COM16', 115200)# Change the COM port to the one of the Arduino you are using.
x = 0
y = 0

filename = "parameters.csv"
#default values (do not edit these lines).
right_init_val = 549# initial sensor value for the right bend sensor.
left_init_val = 529# initial sensor value for the left bend sensor.
right_init_x = 410# initial color-picking position on the right.
left_init_x = 255# initial color-picking position on the left.
right_init_y = 210# initial color-picking position on the right.
left_init_y = 210# initial color-picking position on the left.
right_x_coeff = 4.6# coefficient to adjust color-picking position on the right when force is applied.
right_y_coeff = 0.0# coefficient to adjust color-picking position on the right when force is applied.
left_x_coeff = 6.0# coefficient to adjust color-picking position on the left when force is applied.
left_y_coeff = 0.0# coefficient to adjust color-picking position on the left when force is applied.

# Default Sensor Values Calibration
print("Please hold the brush in the air.")
# Wait for 5 sec
for i in range(5, 0, -1):
    print("Sensor initialization starts in " + str(i), end='\r')
    time.sleep(1)
print("Sensor initialization starts in 0\nSensor initialization started.")
print("Initializing", end='')
# Calculate the initial sensor values for the right and left bend sensors
right_init_val = 0
left_init_val = 0
# Take the average of 1000 values
for i in range(1000):
    if i % 250 == 0:
        print(".", end='')
    # Clear the input buffer before attempting to read the latest values from the Arduino
    while ser.in_waiting > 10:
        ser.readline()
    # Read a line from the serial input
    line = ser.readline().decode('utf-8').rstrip()
    # Convert it to an array of values
    if len(line) > 0:
        values = [int(val) for val in line.split(",")]
    right_init_val += values[0]
    left_init_val += values[1]
right_init_val = int(right_init_val / 1000)
left_init_val = int(left_init_val / 1000)
print("done")
print("Color-picking position initialization starts soon...")

# Default Color-Picking Positions Calibration
# Open a video stream (change the id so that the program shows the video stream from the webcam)
cap = cv2.VideoCapture(0)
cap_width = cap.get(3)
cap_height = cap.get(4)
# Right
print("Please use the arrow keys to move the circle to the right of the brush.")
print("When you finish the adjustment, please press Enter.")
while True:
    if keyboard.is_pressed('enter'):
        break
    if keyboard.is_pressed('right'):
        right_init_x += 3
    if keyboard.is_pressed('left'):
        right_init_x -= 3
    if keyboard.is_pressed('up'):
        right_init_y -= 3
    if keyboard.is_pressed('down'):
        right_init_y += 3
    right_init_x = int(max(min(right_init_x, cap_width-1), 0))
    right_init_y = int(max(min(right_init_y, cap_height-1), 0))
    # Read a frame from the video stream
    ret, frame = cap.read()
    blue, green, red = frame[right_init_y, right_init_x]
    # Show the frame with a circle around the specified pixel
    cv2.circle(frame, (right_init_x, right_init_y), 24, (0, 255, 0), -1)
    cv2.circle(frame, (right_init_x, right_init_y), 20, (int(blue), int(green), int(red)), -1)
    cv2.imshow("Video", frame)
    # Wait for a key press and exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

time.sleep(0.8)

# Left
print("Please use the arrow keys to move the circle to the left of the brush.")
print("When you finish the adjustment, please press Enter.")
while True:
    if keyboard.is_pressed('enter'):
        break
    if keyboard.is_pressed('right'):
        left_init_x += 3
    if keyboard.is_pressed('left'):
        left_init_x -= 3
    if keyboard.is_pressed('up'):
        left_init_y -= 3
    if keyboard.is_pressed('down'):
        left_init_y += 3
    left_init_x = int(max(min(left_init_x, cap_width-1), 0))
    left_init_y = int(max(min(left_init_y, cap_height-1), 0))
    # Read a frame from the video stream
    ret, frame = cap.read()
    blue, green, red = frame[left_init_y, left_init_x]
    # Show the frame with a circle around the specified pixel
    cv2.circle(frame, (left_init_x, left_init_y), 24, (0, 255, 0), -1)
    cv2.circle(frame, (left_init_x, left_init_y), 20, (int(blue), int(green), int(red)), -1)
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

time.sleep(0.8)

# Bend Coefficient Calibration
# Right
print("Please move the circle to the right of the brush stroked from left to right.")
print("When you finish the adjustment, please press Enter.")
while True:
    # Clear the input buffer before attempting to read the latest values from the Arduino
    while ser.in_waiting > 10:
        ser.readline()
    # Read a line from the serial input
    line = ser.readline().decode('utf-8').rstrip()
    # Convert it to an array of values
    if len(line) > 0:
        values = [int(val) for val in line.split(",")]

    if keyboard.is_pressed('enter'):
        break
    if keyboard.is_pressed('right'):
        right_x_coeff += 0.1
    if keyboard.is_pressed('left'):
        right_x_coeff -= 0.1
    if keyboard.is_pressed('up'):
        right_y_coeff -= 0.1
    if keyboard.is_pressed('down'):
        right_y_coeff += 0.1
    x = right_init_x + (values[0] - right_init_val) * right_x_coeff
    y = right_init_y + (values[0] - right_init_val) * right_y_coeff
    x = int(max(min(x, cap_width-1), 0))
    y = int(max(min(y, cap_height-1), 0))

    # Read a frame from the video stream
    ret, frame = cap.read()
    blue, green, red = frame[y, x]
    # Show the frame with a circle around the specified pixel
    cv2.circle(frame, (x, y), 24, (0, 255, 0), -1)
    cv2.circle(frame, (x, y), 20, (int(blue), int(green), int(red)), -1)
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

time.sleep(0.8)

# Left
print("Please move the circle to the left of the brush stroked from Right to Left.")
print("When you finish the adjustment, please press Enter.")
while True:
    # Clear the input buffer before attempting to read the latest values from the Arduino
    while ser.in_waiting > 10:
        ser.readline()
    # Read a line from the serial input
    line = ser.readline().decode('utf-8').rstrip()
    # Convert it to an array of values
    if len(line) > 0:
        values = [int(val) for val in line.split(",")]

    if keyboard.is_pressed('enter'):
        break
    if keyboard.is_pressed('right'):
        left_x_coeff -= 0.1
    if keyboard.is_pressed('left'):
        left_x_coeff += 0.1
    if keyboard.is_pressed('up'):
        left_y_coeff -= 0.1
    if keyboard.is_pressed('down'):
        left_y_coeff += 0.1
    x = left_init_x - (values[1] - left_init_val) * left_x_coeff
    y = left_init_y - (values[1] - left_init_val) * left_y_coeff
    x = int(max(min(x, cap_width-1), 0))
    y = int(max(min(y, cap_height-1), 0))
    
    # Read a frame from the video stream
    ret, frame = cap.read()
    blue, green, red = frame[y, x]
    # Show the frame with a circle around the specified pixel
    cv2.circle(frame, (x, y), 24, (0, 255, 0), -1)
    cv2.circle(frame, (x, y), 20, (int(blue), int(green), int(red)), -1)
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save the calibrated parameters
with open(filename, 'w', newline='') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerows([["right_init_val", "left_init_val", "right_init_x", "left_init_x", "right_init_y", "left_init_y", "right_x_coeff", "right_y_coeff", "left_x_coeff", "left_y_coeff"], 
                        [right_init_val, left_init_val, right_init_x, left_init_x, right_init_y, left_init_y, round(right_x_coeff, 2), round(right_y_coeff, 2), round(left_x_coeff, 2), round(left_y_coeff, 2)]])

print("Parameter values were saved to " + filename)
# Release the video stream and close all windows
cap.release()
cv2.destroyAllWindows()
print("Calibration is completed!")