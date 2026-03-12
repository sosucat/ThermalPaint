# ThermalPaint
[![Homepage](https://img.shields.io/badge/🔗_Project_Page-black)]()
[![Author](https://img.shields.io/badge/Author_Website-black?logo=googlescholar&logoColor=white)](https://sosuke-ichihashi.com/)
[![Research paper](https://img.shields.io/badge/Research_Paper-black?logo=acm)](https://doi.org/10.1145/3731459.3779344)
[![Watch on YouTube](https://img.shields.io/badge/Watch_on_YouTube-750014?logo=youtube)]()

In Thermal Painting, the artist feels physical warmth according to the color they are painting.
ThermalPaint detects the color painted with the ThermalPaint brush (a brush with a bend sensor and a webcam) and controls heat output on the painter.
For more detail and user study results, please refer to our [paper](https://doi.org/10.1145/3731459.3779344) and [video](https://youtu.be/mg1KRw85CI4).

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

### Stroke & Color Detection
Brush stroke, stroke and color detections are done with a bend sensor and a webcam.
The bend sensor data is communicated from the [Xiao nrf52840 Sense board](https://wiki.seeedstudio.com/XIAO_BLE/#getting-started) via BLE.
Alternatively, you can use an Arduino board and communicate the sensor data via wired serial communication.
Both Xiao and Arduino sketch files can be found in ThermalPaint/bendsensing.
For the hardware configuration, please refer to [our paper](https://doi.org/10.1145/3731459.3779344) as well as the hardware Readme doc.

### Thermal Feedback using ThermoBlinds
Heat is dynamically provided with the thermal feedback device we developed. For more details about the heating mechanism, please refer to the following publications:
- Sosuke Ichihashi, Arata Horie, Masaharu Hirose, Zendai Kashino, Shigeo Yoshida, and Masahiko Inami. 2021. High-Speed Non-Contact Thermal Display Using Infrared Rays and Shutter Mechanism. In Adjunct Proceedings of the 2021 ACM International Joint Conference on Pervasive and Ubiquitous Computing and Proceedings of the 2021 ACM International Symposium on Wearable Computers (UbiComp '21). Association for Computing Machinery, New York, NY, USA, 565–569. [https://doi.org/10.1145/3460418.3480160](https://doi.org/10.1145/3460418.3480160)
- Sosuke Ichihashi, Arata Horie, Masaharu Hirose, Zendai Kashino, Shigeo Yoshida, Sohei Wakisaka, and Masahiko Inami. 2022. ThermoBlinds: Non-Contact, Highly Responsive Thermal Feedback for Thermal Interaction. In ACM SIGGRAPH 2022 Emerging Technologies (SIGGRAPH '22). Association for Computing Machinery, New York, NY, USA, Article 10, 1–2. [https://doi.org/10.1145/3532721.3535569](https://doi.org/10.1145/3532721.3535569)

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
9. Update the port numbers in `src/thermalpaint/config.py`. If you use wired Arduino for bend detection, update its port number as well.
      ```py
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
14. Run the calibration program.
      ```
      pixi run python src/thermalpaint/calibration.py
      ```
15. Run the main program.
      ```
      pixi run python src/thermalpaint/__init__.py
      ```
16. Paint!
