from machine import Pin, ADC, I2C
import utime
from dht import DHT22  # Library for DHT22 Sensor

# Sensor Pins
dht_pin = Pin(2)  # DHT22 sensor on GP2
mq2_pin = ADC(26)  # MQ-2 Gas Sensor on GP26 (ADC0)
flame_pin = Pin(3, Pin.IN)  # Flame sensor on GP3
soil_pin = ADC(27)  # Soil Moisture Sensor on GP27 (ADC1)
wind_pin = ADC(28)  # Wind Speed Sensor on GP28 (ADC2)

# Initialize DHT22
dht = DHT22(dht_pin)

# Fire Risk Thresholds (Modify as needed)
TEMP_THRESHOLD_LOW = 30  # °C
TEMP_THRESHOLD_HIGH = 35  # °C
HUMIDITY_THRESHOLD = 30  # %
GAS_THRESHOLD_MODERATE = 300  # Analog value
GAS_THRESHOLD_HIGH = 500  # Analog value
FLAME_DETECTED = 0  # 0 means fire detected
SOIL_DRY_THRESHOLD = 400  # Analog value (0-1023)
WIND_SPEED_MODERATE = 15  # Wind in km/h (analog range)
WIND_SPEED_HIGH = 25  # Wind in km/h (analog range)

def read_sensors():
    """Read all sensor values"""
    dht.measure()
    temp = dht.temperature()
    humidity = dht.humidity()
    gas_value = mq2_pin.read_u16() // 64  # Scale 16-bit ADC to 10-bit (0-1023)
    flame_value = flame_pin.value()  # 0 = Fire detected, 1 = No fire
    soil_value = soil_pin.read_u16() // 64  # Scale ADC
    wind_value = wind_pin.read_u16() // 64  # Scale ADC

    return temp, humidity, gas_value, flame_value, soil_value, wind_value

def get_fire_risk(temp, humidity, gas, flame, soil, wind):
    """Determine fire danger level (0-4)"""
    if flame == FLAME_DETECTED or gas > GAS_THRESHOLD_HIGH:
        return 4  # 🔥 Extreme Fire Danger
    
    elif (temp > TEMP_THRESHOLD_HIGH and humidity < HUMIDITY_THRESHOLD) or \
         (gas > GAS_THRESHOLD_MODERATE and wind > WIND_SPEED_HIGH) or \
         (soil < SOIL_DRY_THRESHOLD and wind > WIND_SPEED_HIGH):
        return 3  # 🔴 High Fire Risk
    
    elif (temp > TEMP_THRESHOLD_LOW and humidity < HUMIDITY_THRESHOLD) or \
         (gas > GAS_THRESHOLD_MODERATE) or \
         (wind > WIND_SPEED_MODERATE):
        return 2  # 🟠 Moderate Fire Risk
    
    elif soil < SOIL_DRY_THRESHOLD:
        return 1  # 🟡 Low Fire Risk
    
    return 0  # 🟢 Safe

while True:
    temp, humidity, gas, flame, soil, wind = read_sensors()
    risk_level = get_fire_risk(temp, humidity, gas, flame, soil, wind)

    risk_messages = {
        0: "🟢 SAFE - No fire risk",
        1: "🟡 LOW RISK - Dry conditions",
        2: "🟠 MODERATE RISK - Fire possible",
        3: "🔴 HIGH RISK - Fire likely!",
        4: "🔥🚨 EXTREME DANGER - FIRE DETECTED! 🚨🔥"
    }

    print(f"🌡 Temp: {temp}°C  💧 Humidity: {humidity}%")
    print(f"🔥 Gas Level: {gas}  🚨 Flame: {flame}")
    print(f"🌱 Soil Moisture: {soil}  💨 Wind Speed: {wind}")
    print(f"⚠️ Fire Risk Level: {risk_level} - {risk_messages[risk_level]}\n")

    utime.sleep(2)  # Delay for stability
