# Thermal Painting
[![Homepage](https://img.shields.io/badge/🔗_Project_Page-black)]()
[![Author](https://img.shields.io/badge/Author_Website-black?logo=googlescholar&logoColor=white)](https://sosuke-ichihashi.com/)
[![Research paper](https://img.shields.io/badge/Research_Paper-black?logo=acm)](https://doi.org/10.1145/3731459.3779344)
[![Watch on YouTube](https://img.shields.io/badge/Watch_on_YouTube-750014?logo=youtube)]()

In Thermal Painting, artists feel physical warmth according to the color they are painting.
Our system detects the color painted with the ThermalPaint brush (a brush with a bend sensor and a webcam) and controls heat output on the painter.
For more details and the user study results, please refer to our [paper](https://doi.org/10.1145/3731459.3779344) and [video](https://youtu.be/mg1KRw85CI4).


## Hardware
The system consists of the ThermalPaint Brush, which detects colors when painted, a PC to run the program, and the ThermoBlinds heater.
Please refer to the [Hardware page](./Hardware) for more details.


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
6. Install [RS30xPacketUtil](http://micutil.com/rx/rs30xpacketutil.html).

   To control the RS204MD servo motors from your PC, you need to install the software containing the driver (the website is in Japanese, and google translate sometimes does not work well, so please download [this html file](https://drive.google.com/file/d/1qztwM8tqKWbrD8Aod6qqK9VrmVXrDmzK/view?usp=drive_link), open it with your browser, and follow the instructions.)
7. Connect ThermoBlinds and ThermalPaint brush to your PC and a wall power.
8. Check the COM port for the servo motor driver on RS30xPacketUtil.
9. Update the port number in `src/thermalpaint/config.py`.
      # --- Configuration Constants ---
      COM_PORT_MOTOR = 'COM11'  # Dicot Motor
      ```
10. (For MAC users) Update the following line in `src/thermalpaint/config.py`.
      For Windows
      ```py
      with open(filename, 'w', newline='') as csvfile:
      ```
      For Mac
      ```py
      with open(filename, 'w') as csvfile:
      ```
11. Upload [the Bend_BLE sketch](./Bend_BLE) to your Xiao nrf52840 microcontroller.
12. Run the calibration program.
      ```
      pixi run python src/thermalpaint/calibration.py
      ```
      If a wrong webcam is detected, update the camera ID in the following lines:
      ```py
      #Calibration.py L12 & __init__.py L19
      self.cap = cv2.VideoCapture(0)
      ```
13. Run the main program.
      ```
      pixi run python src/thermalpaint/__init__.py
      ```
14. Paint!


## Publication
Supratim Pait, Sosuke Ichihashi, Xingyu Li, Haiqing Xu, and Noura Howell. 2026. Designing for Defamiliarization with Thermal Painting: Exploring Experiences of Dynamic Warmth in Painters' Creative Processes. In Proceedings of the Twentieth International Conference on Tangible, Embedded, and Embodied Interaction (TEI '26). Association for Computing Machinery, New York, NY, USA, Article 84, 1–11. [https://doi.org/10.1145/3731459.3779344](https://doi.org/10.1145/3731459.3779344)
```bibtex
@inproceedings{10.1145/3731459.3779344,
author = {Pait, Supratim and Ichihashi, Sosuke and Li, Xingyu and Xu, Haiqing and Howell, Noura},
title = {Designing for Defamiliarization with Thermal Painting: Exploring Experiences of Dynamic Warmth in Painters' Creative Processes},
year = {2026},
isbn = {9798400718687},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3731459.3779344},
doi = {10.1145/3731459.3779344},
abstract = {Thermal Painting is a probe to explore multisensory painting, aiming to defamiliarize, or present the familiar creative practice of painting in an unfamiliar way for artists. The system provides dynamic thermal feedback based on what color the artist is painting. In a qualitative, exploratory pilot study with 20 artists, we investigated how thermal sensations influenced their creative process. Artists described how thermal feedback impacted color selection, brush movements, comfort and flow, thematic associations, and memory triggers. This prompts plans for future work around design improvements, an in-situ field study, thermal associations, and multisensory defamiliarization. This project offers preliminary insights into the interplay of thermal sensation and creative process.},
booktitle = {Proceedings of the Twentieth International Conference on Tangible, Embedded, and Embodied Interaction},
articleno = {84},
numpages = {11},
keywords = {Painting, Creativity, Thermal Feedback},
location = {
},
series = {TEI '26}
}
```
