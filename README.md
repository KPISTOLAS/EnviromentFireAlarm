# Forest Fire Alarm System Using Raspberry Pi Pico W and Drone Scouting

This is an embedded systems project focused on early fire detection in forested areas. The system is divided into three main components: a dashboard, a ground unit, and an aerial unit.
1) Ground System: Gathers environmental data (e.g., temperature, humidity, smoke levels) to assess fire risk in specific regions. It processes this data to identify high-risk zones.
2) Dashboard: Displays real-time data and visualizes fire risk areas on a map. It helps operators monitor the situation and make informed decisions.
3) Aerial System: A lightweight autonomous aircraft (drone or small plane) flies over high-risk zones to verify alarms. It is equipped with a camera that captures images and video, which are analyzed to confirm fire presence.

The collected data enhances situational awareness and supports faster, more accurate responses to potential wildfires.
## Ground system
---

## Levels of alert (Algorithm)
The algorith use data from sensors in order to have a result
0)  Safe, No risk
1)  Very Low Risk
2)  Low Risk
3)  Moderate Risk
4)  High Risk
5)  Extreme Danger, Fire detected


## List of Equipment

1) Raspberry Pi Pico W (with WiFi for data transmission)
2) Temperature & Humidity (DHT22)
3) Gas Sensor (MQ-2)
4)  Infrared Flame Sensor)
5)  Optical Smoke Sensor
6)  Soil Moisture Sensor
7)  Holybro Airspeed Sensor
8)  Solar Panel (6V, 2W)
9)  TP4056 Charge Controllerv
10)  18650 Li-Ion Battery (3.7V)
11)  Boost Converter (MT3608)
12)  Frame

## Power System
As we know in the enviroment there are no easy electrical supply systems so we use a Solar Panel and a Battery for power supply. The battery is rechargeable and has a with Pulse-code modulation (PCM). Also, we use aa DFRobot Solar Power Manager 5V for manage solar energy and charging a 3.7V Li-ion/LiPo battery at up to 900mA using either a solar panel or USB input. Finally, i use a Power Supply Module to power raspberry pi pico and to give power to sensors.

1) DFRobot Solar Power Management Module MPPT Chipm, 14$ 
2) 1-10 Pieces 600mAh Rechargeable Lithium Ion Battery 3.7 V 402530 Li-polymer Batteries Electric Toy LED Light Headset Bateria, 1pc 7$ 
3) 2V 3V 4V 5.5V 5V 6V 7V 10V Mono/Polycrystalline Mini Solar Panel Battery Module DIY Epoxy Board PET Power Gneration board Model, 5V 200mA 109X83 3$
4) MB102 Breadboard Power Supply Module 3.3V/5V 3$
5) Cables


Schematics:
![image](https://github.com/user-attachments/assets/66e57dae-e51a-481d-a4f9-1400aa7a7e74)


## ES1 Model
The ES1 system is used to sensor if there is a fire in the area. We use 2 sensores, one smoke sensor and one temperature/ humidity sensor. Also, we use 2 parameters, the dencity of the forest and the hill's inclint

## 🔧 System Overview

The system is made up of the following components:

### 1. **Raspberry Pi Pico W**
- Main microcontroller.
- Handles data collection and transmission.
- Capable of low-power operation for remote deployments.

### 2. **DHT22 Sensor**
- Measures **temperature** and **humidity**.
- Key for identifying dry and hot conditions that increase fire risk.

### 3. **MQ2 Gas Sensor**
- Detects **smoke**, **methane**, **LPG**, and other combustible gases.
- Analog output for sensing smoke density.

### 4. **LoRa Module (RA-02)**
- Enables **long-range communication**.
- Sends collected data wirelessly to a remote dashboard or base station.

## 5. **Rain Sensor**
- Measures presence and intensity of rainfall.
- Helps determine local weather conditions.

## 6. **Wind Speed Sensor (Anemometer)**
- Measures wind speed using rotating cups.
- Outputs pulses which can be measured for speed.
---

## 📡 System Architecture

[Sensors] --> [Pico W] --> [LoRa Module] --> [Remote Receiver/Dashboard]


- Data from sensors is read by the Pico W.
- If thresholds are exceeded (e.g. high temp + smoke), a warning is sent.
- LoRa is used for communication in remote, off-grid areas.

---

## 🖼️ Circuit Diagram

> Ensure to update the image path above with the correct one in your repo.

### Wiring Summary

| Component    | Pin                | Pico W Pin       |
|--------------|--------------------|------------------|
| DHT22        | VCC                | 3.3V             |
|              | GND                | GND              |
|              | DATA               |GPIO (e.g. GP15) + 10kΩ|
| MQ2          | VCC                | 3.3V             |
|              | GND                | GND              |
|              | A0 (Analog Out)    | GP26 (ADC)       |
| LoRa RA-02   | MISO               | GP16             |
|              | MOSI               | GP15             |
|              | SCK                | GP14             |
|              | NSS (CS)           | GP13             |
|              | RST                | GP12             |
|              | GND                | GND              |
|              | VCC                | 3.3V             |
| Rain Sensor	 | VCC                | 3.3V             |
|              | GND                | GND              |
|              | DO                 | GP18             |
| Wind Sensor	 | VCC                | 3.3V             |
|              | GND                | GND              |
|              | Signal             | GP16             |


## Schematics:
![image](https://github.com/user-attachments/assets/1ab83d7f-21eb-4c7e-a765-565a8dcd5b87)


---

## 🧠 How It Works

1. **Monitoring**: Continuously reads data from DHT22 and MQ2.
2. **Threshold Detection**: If environmental conditions suggest a fire (e.g. high temperature, low humidity, and smoke), the system triggers a warning.
3. **Communication**: The data is transmitted via LoRa to a receiver/base station.
4. **Action**: Remote systems (or operators) can trigger an alert, or deploy drones for further scouting.

---
## Aerial system

## List of Equipment
1) Raspberry Pi Pico W (with WiFi for data transmission)
2) Brushless DC Motor (for propulsion)
3)  Electronic Speed Controller
4)  Servos (for ailerons, rudder, and elevator control)
5)  FPV (First-Person View) Camera (for live video streaming)
6)  Raspberry Pi-compatible Camera (for taking pictures)
7)  LiPo Battery (3S or 4S)
8)  Gyroscope/Accelerometer (MPU6050) (stabilization)
9)  Barometer (BMP180) (altitude sensing)
10)  GPS Module (NEO-6M) (navigation)
11)  Frame
12)  Controller
