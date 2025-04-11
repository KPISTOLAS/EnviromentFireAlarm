# EnviromentFireAlarm
A embeded system project for a Fire Alarm in forests using raspberry pi pico w and drone scouting. There are 2 parts in this project, the ground and the aerial system. The ground will collect data and shows us which area is most likely to catch fire. Also, all data will use to mark the area of danger so the aerial system. In the air, there will be a small plane flying above these areas to ensure the alarms. There will be a camera that analyze the data using an AI.
## Ground system
---

## Levels of alert (Algorithm)
The algorith use data from sensors in order to have a result
0)  Safe, No risk
1)  Low Risk, Slightly dry conditions
2)  Moderate Risk, Possible fire conditions
3)  High Risk, Fire likely	
4)  Extreme Danger, Fire detected


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
As we know in the enviroment there are no easy electrical supply systems so we use a Solar Panel and a Battery for power supply. The batteryu is rechargeable and has a with Pulse-code modulation (PCM). Also, we use aa DFRobot Solar Power Manager 5V for manage solar energy and charging a 3.7V Li-ion/LiPo battery at up to 900mA using either a solar panel or USB input.   

1) DFRobot Solar Power Management Module MPPT Chipm, 14$ (https://www.aliexpress.com/item/1005008397923854.html?spm=a2g0o.productlist.main.4.49524f2cDmc2Ke&algo_pvid=3612642c-b378-43d6-b5f3-34fc656b9c54&algo_exp_id=3612642c-b378-43d6-b5f3-34fc656b9c54-3&pdp_ext_f=%7B%22order%22%3A%221%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21EUR%2113.65%2113.65%21%21%21110.36%21110.36%21%40211b629217443653003988586ed6b8%2112000044858814299%21sea%21GR%216288222735%21X&curPageLogUid=ieoCYC3XfnC0&utparam-url=scene%3Asearch%7Cquery_from%3A#nav-review )
2) 1-10 Pieces 600mAh Rechargeable Lithium Ion Battery 3.7 V 402530 Li-polymer Batteries Electric Toy LED Light Headset Bateria, 1pc 7$ (https://www.aliexpress.com/item/1005008518007613.html?spm=a2g0o.productlist.0.0.276e7cd5CT05XD&mp=1&pdp_npi=5%40dis%21EUR%21EUR%2013.48%21EUR%206.74%21%21%21%21%21%40211b612517443723534403431ea2bb%2112000045525560313%21ct%21GR%216288222735%21%211%210)
3) 2V 3V 4V 5.5V 5V 6V 7V 10V Mono/Polycrystalline Mini Solar Panel Battery Module DIY Epoxy Board PET Power Gneration board Model, 5V 200mA 109X83 3$ (https://www.aliexpress.com/item/1005004689060279.html?spm=a2g0o.productlist.main.9.276e7cd5CT05XD&algo_pvid=8ab9e544-c489-42af-84ea-81448fa0f52d&algo_exp_id=8ab9e544-c489-42af-84ea-81448fa0f52d-8&pdp_ext_f=%7B%22order%22%3A%22466%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21EUR%210.56%210.56%21%21%210.62%210.62%21%40211b813f17443723515596391ecfbd%2112000030107576989%21sea%21GR%216288222735%21X&curPageLogUid=zH9tDf6Epqhn&utparam-url=scene%3Asearch%7Cquery_from%3A)
4) Cables


Schematics:
![image](https://github.com/user-attachments/assets/80b162be-9ca9-456f-b7bf-9b3156a49b87)

## ES1 Model
The ES1 system is used to sensor if there is a fire in the area using 


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
