# ThermalPaint

## Heat is applied from ThermoBlinds according to the color painted with ThermalPaint brush.
thermalPaint.py detects the color painted with ThermoPaint brush (a brush with a pair of bend sensors and a webcam) and controls ThermoBlinds based on the color.
For more details about ThermoBlinds, please refer to the following papers:
- Sosuke Ichihashi, Arata Horie, Masaharu Hirose, Zendai Kashino, Shigeo Yoshida, and Masahiko Inami. 2021. High-Speed Non-Contact Thermal Display Using Infrared Rays and Shutter Mechanism. In Adjunct Proceedings of the 2021 ACM International Joint Conference on Pervasive and Ubiquitous Computing and Proceedings of the 2021 ACM International Symposium on Wearable Computers (UbiComp '21). Association for Computing Machinery, New York, NY, USA, 565–569. https://doi.org/10.1145/3460418.3480160
- Sosuke Ichihashi, Arata Horie, Masaharu Hirose, Zendai Kashino, Shigeo Yoshida, Sohei Wakisaka, and Masahiko Inami. 2022. ThermoBlinds: Non-Contact, Highly Responsive Thermal Feedback for Thermal Interaction. In ACM SIGGRAPH 2022 Emerging Technologies (SIGGRAPH '22). Association for Computing Machinery, New York, NY, USA, Article 10, 1–2. https://doi.org/10.1145/3532721.3535569

## Directory structure
```r
ThermalPaint/ThermalPaint/
├── .pixi/
│   ├── envs/              # Conda/pypi env. Created by pixi install
│   └── ...
├── src/thermalpaint/      # Source code
│   ├── __init__.py        # Main program
│   ├── calibration.py     # Calibration program
│   ├── config.py          # Config helper
│   ├── hardware.py        # Hardware handling helper
│   └── utils.py           # Utility helper (color to heat conversion)
├── data/
│   └── config.csv         # Config data
├── dual_bend_sensors_serial_send
│   └── dual_bend_sensors_serial_send.ino # Arduino code
├── pixi.toml              # Project manifest (dependencies)
└── ...
```

## Quick start
1. Install [pixi](https://pixi.prefix.dev/latest/installation/).
   ```powershell
   powershell -ExecutionPolicy Bypass -c "irm -useb https://pixi.sh/install.ps1 | iex"
   ```
2. Restart powershell.
3. Verify installation.
   ```
   pixi --version
   ```
4. Change directory to `ThermalPaint/ThermalPaint`.
5. Install dependencies.
   ```
   pixi install
   ```
6. Install [Arduino IDE](https://www.arduino.cc/en/software).
7. Install [RS30xPacketUtil](http://micutil.com/rx/rs30xpacketutil.html).

   To control the RS204MD servo motors from your PC, you need to install the software containing the driver (the website is in Japanese, and google translate sometimes does not work well, so please download [this html file](https://drive.google.com/file/d/1qztwM8tqKWbrD8Aod6qqK9VrmVXrDmzK/view?usp=drive_link), open it with your browser, and follow the instructions.)
8. Connect ThermoBlinds and ThermalPaint brush to your PC and a wall power.
9. Check the COM ports for the Arduino and the servo motor driver on Arduino IDE and RS30xPacketUtil.
10. Update the port numbers in `src/thermalpaint/config.py`.
      ```py
      # --- Configuration Constants ---
      COM_PORT_BRUSH = 'COM4'   # Arduino Sensor
      COM_PORT_MOTOR = 'COM11'  # Dicot Motor
      ```
11. (For MAC users) Update the following line in `src/thermalpaint/config.py`.

      For Windows
      ```py
      with open(filename, 'w', newline='') as csvfile:
      ```
      For Mac
      ```py
      with open(filename, 'w') as csvfile:
      ```
12. Upload the `dual_bend_sensors_serial_send.ino` to the Arduino on Arduino IDE.
13. Run a calibration.
      ```
      pixi run python src/thermalpaint/calibration.py
      ```
      `data/config.csv` should be updated.
14. Run the main program.
      ```
      pixi run python src/thermalpaint/__init__.py
      ```
15. Paint!
