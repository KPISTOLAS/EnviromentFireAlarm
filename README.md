# EnviromentFireAlarm
A embeded system project for a Fire Alarm in forests using raspberry pi pico w and drone scouting. There are 2 parts in this project, the ground and the aerial system. The ground will collect data and shows us which area is most likely to catch fire. Also, all data will use to mark the area of danger so the aerial system. In the air, there will be a small plane flying above these areas to ensure the alarms. There will be a camera that analyze the data using an AI.
## Ground system

## List of Equipment

1) Raspberry Pi Pico W (with WiFi for data transmission)
2) Temperature & Humidity (DHT22)
3) Gas Sensor (MQ-2
4)  Infrared Flame Sensor)
5)  Optical Smoke Sensor
6)  Soil Moisture Sensor
7)  Holybro Airspeed Sensor
8)  Solar Panel (6V, 2W)
9)  TP4056 Charge Controllerv
10)  18650 Li-Ion Battery (3.7V)
11)  Boost Converter (MT3608)
12)  Frame

## Levels of alert
0)  Safe, No risk
1)  Low Risk, Slightly dry conditions
2)  Moderate Risk, Possible fire conditions
3)  High Risk, Fire likely	
4)  Extreme Danger, Fire detected

Schematics:
![circuit_image](https://github.com/user-attachments/assets/33410e80-0e8d-4954-8cd2-0472d11ad471)

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
