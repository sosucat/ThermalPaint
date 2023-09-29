# ThermalPaint

## Heat is applied from ThermoBlinds according to the color painted with ThermalPaint brush.
thermalPaint.py detects the color painted with ThermoPaint brush (a brush with a pair of bend sensors and a webcam) and controls ThermoBlinds based on the color.
For more details about ThermoBlinds, please refer to the following papers:
- Sosuke Ichihashi, Arata Horie, Masaharu Hirose, Zendai Kashino, Shigeo Yoshida, and Masahiko Inami. 2021. High-Speed Non-Contact Thermal Display Using Infrared Rays and Shutter Mechanism. In Adjunct Proceedings of the 2021 ACM International Joint Conference on Pervasive and Ubiquitous Computing and Proceedings of the 2021 ACM International Symposium on Wearable Computers (UbiComp '21). Association for Computing Machinery, New York, NY, USA, 565–569. https://doi.org/10.1145/3460418.3480160
- Sosuke Ichihashi, Arata Horie, Masaharu Hirose, Zendai Kashino, Shigeo Yoshida, Sohei Wakisaka, and Masahiko Inami. 2022. ThermoBlinds: Non-Contact, Highly Responsive Thermal Feedback for Thermal Interaction. In ACM SIGGRAPH 2022 Emerging Technologies (SIGGRAPH '22). Association for Computing Machinery, New York, NY, USA, Article 10, 1–2. https://doi.org/10.1145/3532721.3535569

## How to use
1. Get a Windows PC.
2. Install python (all the programs are tested on 3.8.10): [download page](https://www.python.org/downloads/release/python-3810/).
3. Install the following libraries after updating the pip.
   pip install --upgrade pip
  1. [serial](https://pyserial.readthedocs.io/en/latest/pyserial.html): Handles serial communications between the microcontrollers on ThermoBlinds and ThermalPaint brush and the host PC.
      ```
      pip install pyserial
      ```
  2. [cv2](https://pypi.org/project/opencv-python/): Streams a video from the webcam mounted on the brush.
      ```
      pip install opencv-python
      ```
  3. [dicot](https://pypi.org/project/dicot/): Controls Futaba Command-Type Servo motors on TheroBlinds. It is developed and tested with RS204MD. Please skip this if you are using other servo motors.
      ```
      pip install dicot
      ```
3. Download and place both thermalPaint.py and calibration.py to the same directory.
4. Install [Arduino IDE](https://www.arduino.cc/en/software).
5. Download and place the dual_bend_sensors_serial_send directory containing dual_bend_sensors_serial_send.ino in the Arduino file directory.
6. Connect ThermoBlinds and ThermalPaint brush to your PC and a power source.
7. Check the COM ports allocated to their microcontrollers on your PC and modify the port numbers in the thermalPaint.py and calibration.py.
   - Check the port numvers
     -- Windows: Go to Device Manager > Ports (COM & LPT).
     -- Mac: On Terminal, ```ls /dev/tty.usb*```.
   - Update the port numbers on the codes (in this case, the port for the brush is COM16, and the one for ThermalBlinds is COM3.
     -- calibration.py:
        ```python
        ser = serial.Serial('COM16', 115200)
        ```
     -- thermalPaint.py:
        ```python
        ser = serial.Serial('COM16', 115200)
        cnx = dicot.open('COM3')
        ```
9. Upload the dual_bend_sensors_serial_send.ino from Arduino IDE.
10. On Command Prompt or Terminal, go to the directory you placed the thermalPaint.py and calibration.py.
   * If you are using a Mac, you want to replace
   ```python
   with open(filename, 'w', newline='') as csvfile:
   ```
   with
   ```python
   with open(filename, 'w') as csvfile:
   ```
   in calibration.py.
11. Run a calibration.
   ```python
   python calibration.py
   ```
12. Check if "parameters.csv" is successfully generated in the same directory.
13. Servo motors
   * To control the RS204MD servo motors from your PC, you need to install the software containing the driver (the website is in Japanese, and google translate did not work, so please download [this html file](https://drive.google.com/file/d/1qztwM8tqKWbrD8Aod6qqK9VrmVXrDmzK/view?usp=drive_link), open it with your browser, and follow the instructions.)
14. Run the main program.
   ```python
   python thermalPaint.py
   ```
15. Paint!
