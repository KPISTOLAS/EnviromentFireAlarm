# 🌲 Forest Fire Detection System Using Raspberry Pi Pico W and Drone Scoutingv

An embedded IoT solution designed for early detection of forest fires, integrating ground-based sensors, aerial surveillance, and real-time data visualization.​
--- 
##🔍 Overview
This system comprises three primary components:
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


## 🧰 Hardware Components

1) Raspberry Pi Pico (W)
2) Temperature & Humidity (DHT22)
3) Gas Sensor (MQ-2)
4)  Rain Sensor	
5)  Anemometer
6)  3.7V Li-ion/LiPo Battery	
7)  DFRobot Solar Power Manager 5V	
8)  5V Solar Panel (1W–2.5W)	
9)  MB102 Breadboard Power Supply Module	
10) Frame
    
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

## 🧰 Hardware Components
1) Raspberry Pi Pico W (with WiFi for data transmission)
2) Brushless DC Motor (for propulsion)
3) OpenMV Cam M7
4) Servos (for ailerons, rudder, and elevator control)
5) RC Transmitter/Receiver 
6) Frame
7) Controller
8) Battery

## Aditional
1) Micro SD card (for the camera)
2) LoRa Module or ESP32 (for communication if needed)
3) GPS Module
4) INAV (for advanced autopilot)
   
---
## Frame

    The frame will be created using AI tool for 3D design such as meshy.ai, or we will use a existing design from thingiverse.com or cults3d.com

---


## Dashboard

        We can use a Geographic Information Systems (GIS) or thingsboard.io (Open-source IoT Platform) or thingspeak (Matlab product).
