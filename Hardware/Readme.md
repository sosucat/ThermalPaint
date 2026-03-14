# ThermalPaint Brush Hardware
<img src="assets/Brush.svg" width="600px" max-width="100%" alt="Photo of the Thermal Brush, consisting of a switch, lipo battery, microcontroller, circuit board with pull-up resistors, and a bend sensor. They are all mounted near the ferrule on the brush using a 3D-printed part." /><br>
Here, we describe the hardware configuration of ThermalPaint Brush, a brush that detects its stroke direction and the color being painted in real-time.
For the heater hardware configuration, please refer to our papers ([1](https://doi.org/10.1145/3460418.3480160), [2](https://doi.org/10.1145/3532721.3535569)) as well as [my website](https://sosuke-ichihashi.com/thermoblinds/).

## Brush
The brush can be anything as long as you can fix a bend sensor and a webcam to it.
In our example, we used a [2.5" brush](https://a.co/d/09egNIkl). The 3D models of our sensor and camera mounts are for this specific brush, so please get this if you want to use our mounts.<br>
If you are comfortable with CAD or are ok with fixing the components using more manual ways (e.g., hot glue), please feel free to pick whatever brush you want.

## Sensor & Camera Mounts
The 3D models for the sensor and camera mounts are available in [3d_model](./3d_model).<br>
Alternatively, you could simply hot glue everyting to your brush and use a chopstick or something as the camera mount.

## Microcontroller
We have tried two microcontroller options: Arduino (wired) and [Xiao nrf52840](https://wiki.seeedstudio.com/XIAO_BLE/) (BLE).<br>
The wired connection gives you more seamless integration of the color and heat thanks to its smaller latency.<br>
The BLE gives you more comfortable painting experience by eliminating sensor lines between the brush and PC.<br>
The software on this repo is the one for BLE. If you want to use a wired connection, please contact pengu1n.i843@gmail or make a new issue on this repo.

## Bend Sensor
We have tried two bend sensor options: [typical resistance-based bend sensor](https://www.adafruit.com/product/182) and [Bend Labs waterproof bend sensor](https://www.digikey.com/short/fcwhv7dz).
**We highly recommend the Bend Labs sensor** because it is waterproof and measures bendings in both directions.
If you use a typical resistance-based bend sensor, you need to use two of them to detect both right and left strokes. Then, you need to apply [waterproof flexible polymer](https://a.co/d/00INWjTv) on them, which is pretty labor-heavy.<br>
The software on this repo is for the Bends Labs sensor, which communicates with the Xiao microcontroller via I2C.

## Webcam
You can use pretty much any webcam.
The camera mount 3D model we provided is for [Logitech C270](https://a.co/d/01MAVrKs).
If your PC is connected to multiple cameras including the built-in one, you need to update the index in the code so the opencv can access the camera mounted on the brush.
Please refer to the Readme in the root directory for more details.

## Wiring
<img src="assets/Xiao-BendLabs.png" width="300px" max-width="100%" alt="Wiring diagram. Xiao's 3V3 connects to the sensor's VCC. GND, SDA, SCL connect to the corresponding GND. SDA and SCL pins of the bend sensor. The SDA, SCL, nRST pins are pulled-up with resistors. The NDRDY is floated." /><br>
This is the example for the Xiao board. If you use Arduino, please refer to [the documentation](https://docs.arduino.cc/learn/communication/wire/). Since the sensor's logic level is 3.3V, you might need to use a logic level shifter if you use a 5V board like Uno.


### Stroke & Color Detection
Brush stroke, stroke and color detections are done with a bend sensor and a webcam.
The bend sensor data is communicated from the [Xiao nrf52840 Sense board](https://wiki.seeedstudio.com/XIAO_BLE/#getting-started) via BLE.
Alternatively, you can use an Arduino board and communicate the sensor data via wired serial communication.
Both Xiao and Arduino sketch files can be found in ThermalPaint/bendsensing.
For the hardware configuration, please refer to [our paper](https://doi.org/10.1145/3731459.3779344) as well as the hardware Readme doc.

### Thermal Feedback using ThermoBlinds
Heat is dynamically provided with the thermal feedback device we developed. For more details about the heating mechanism, please refer to the following publications:
