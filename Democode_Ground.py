from machine import Pin, ADC, RTC
import utime

# --- Configuration ---
CONFIG = {
    # Sleep schedule
    'NIGHT_START': 22,  # 10 PM
    'NIGHT_END': 8,     # 8 AM
    
    # Wake-up thresholds
    'SAFE_TEMP': 30,    # Wake if temp exceeds this (℃)
    'SAFE_SMOKE': 300,  # Wake if smoke exceeds this (ppm)
    
    # Danger thresholds
    'TEMP_THRESHOLDS': [20, 25, 30, 35, 40],
    'HUMIDITY_THRESHOLDS': [60, 50, 40, 30, 20],
    'SMOKE_THRESHOLDS': [100, 300, 500, 700, 900],
    'WIND_THRESHOLDS': [10, 20, 30, 40, 50],
    
    # Environmental factors
    'VEGETATION_DENSITY': 0.5,
    'TERRAIN_SLOPE': 2,
    'VEGETATION_TYPE': 2,
    'VEGETATION_FACTORS': {1: 0.7, 2: 1.0, 3: 0.85},
    
    # Timing
    'DAY_UPDATE_INTERVAL_MS': 5000,
    'NIGHT_CHECK_INTERVAL_MS': 10000
}

# --- Hardware Setup ---
# Sensors
temp_sensor = ADC(26)
humidity_sensor = ADC(27)
smoke_sensor = ADC(28)
rain_sensor = Pin(15, Pin.IN, Pin.PULL_UP)
wind_sensor = Pin(16, Pin.IN, Pin.PULL_UP)

# Outputs
alarm_led = Pin(25, Pin.OUT)
# alarm_buzzer = Pin(20, Pin.OUT)  # Uncomment if using buzzer

# Initialize RTC (set proper time before deployment)
rtc = RTC()
# rtc.datetime((2025, 5, 2, 0, 14, 30, 0, 0))  # Uncomment and set actual time

# --- Wind Speed Measurement ---
wind_pulse_count = 0
last_wind_measurement = 0
last_wind_speed = 0.0  # Cached value

def wind_pulse_handler(pin):
    global wind_pulse_count
    wind_pulse_count += 1

wind_sensor.irq(trigger=Pin.IRQ_RISING, handler=wind_pulse_handler)

# --- Time Utilities ---
def get_current_hour():
    return utime.localtime()[3]

def in_nighttime_range(hour):
    """Handle midnight crossover correctly"""
    if CONFIG['NIGHT_START'] > CONFIG['NIGHT_END']:
        return hour >= CONFIG['NIGHT_START'] or hour < CONFIG['NIGHT_END']
    return CONFIG['NIGHT_START'] <= hour < CONFIG['NIGHT_END']

# --- Sensor Functions ---
def read_temperature():
    try:
        reading = temp_sensor.read_u16()
        voltage = reading * 3.3 / 65535
        temp = (voltage - 0.5) * 100
        if not -10 <= temp <= 100:
            raise ValueError("Implausible temperature")
        return temp
    except Exception as e:
        print(f"[ERROR] Temperature: {e}")
        return 25.0

def read_humidity():
    try:
        reading = humidity_sensor.read_u16()
        return min(max((reading / 65535) * 100, 0), 100)
    except Exception as e:
        print(f"[ERROR] Humidity: {e}")
        return 50.0

def read_smoke():
    try:
        return min(smoke_sensor.read_u16() * (1000 / 65535), 2000)
    except Exception as e:
        print(f"[ERROR] Smoke: {e}")
        return 0.0

def read_rain():
    try:
        return rain_sensor.value()
    except Exception as e:
        print(f"[ERROR] Rain: {e}")
        return 1

def measure_wind_speed():
    global wind_pulse_count, last_wind_measurement, last_wind_speed
    try:
        current_time = utime.ticks_ms()
        elapsed = utime.ticks_diff(current_time, last_wind_measurement)
        
        if elapsed >= 5000:  # Update every 5 seconds
            wind_speed_ms = wind_pulse_count / (elapsed / 1000)
            last_wind_speed = wind_speed_ms * 3.6  # km/h
            wind_pulse_count = 0
            last_wind_measurement = current_time
            
            if not 0 <= last_wind_speed <= 100:
                raise ValueError("Implausible wind speed")
        
        return last_wind_speed
    except Exception as e:
        print(f"[ERROR] Wind: {e}")
        return 0.0

# --- Danger Calculation ---
def get_parameter_level(value, thresholds):
    for i, threshold in enumerate(thresholds):
        if value < threshold:
            return i
    return 5  # Extreme

def calculate_fire_danger(temp, humidity, smoke, rain, wind):
    temp_level = get_parameter_level(temp, CONFIG['TEMP_THRESHOLDS'])
    humidity_level = get_parameter_level(humidity, CONFIG['HUMIDITY_THRESHOLDS'])
    smoke_level = get_parameter_level(smoke, CONFIG['SMOKE_THRESHOLDS'])
    wind_level = get_parameter_level(wind, CONFIG['WIND_THRESHOLDS'])
    
    danger_score = (
        temp_level * 0.25 +
        humidity_level * 0.2 +
        smoke_level * 0.2 +
        wind_level * 0.2 +
        (0 if rain else 1) * 0.5 +  # rain_factor * 5 * 0.1 simplified
        (CONFIG['VEGETATION_DENSITY'] * 
         CONFIG['VEGETATION_FACTORS'][CONFIG['VEGETATION_TYPE']] * 
         CONFIG['TERRAIN_SLOPE'] * 0.05)
    )
    
    return ["Safe", "Very Low", "Low", "Moderate", "High", "Extreme"][min(max(round(danger_score), 0), 5)]

# --- Alarm System ---
def trigger_alarm(level):
    print(f"🚨 ALARM: {level} fire risk!")
    alarm_led.on()
    # alarm_buzzer.on()  # Uncomment if using buzzer

def clear_alarm():
    alarm_led.off()
    # alarm_buzzer.off()

# --- Main Operations ---
def display_readings():
    temp = read_temperature()
    humidity = read_humidity()
    smoke = read_smoke()
    rain = read_rain()
    wind = measure_wind_speed()
    
    danger = calculate_fire_danger(temp, humidity, smoke, rain, wind)
    
    print("\n--- Fire Danger Assessment ---")
    print(f"Danger Level: {danger}")
    print(f"Temperature: {temp:.1f}°C | Humidity: {humidity:.1f}%")
    print(f"Smoke: {smoke:.1f} ppm | Wind: {wind:.1f} km/h")
    print(f"Rain: {'No' if rain else 'Yes'}")
    print("-----------------------------")
    
    if danger in ("High", "Extreme"):
        trigger_alarm(danger)
    else:
        clear_alarm()

def enter_sleep_mode():
    print(f"🌙 Sleeping until {CONFIG['NIGHT_END']}:00 or alarm trigger")
    clear_alarm()
    
    while in_nighttime_range(get_current_hour()):
        temp = read_temperature()
        smoke = read_smoke()
        
        if temp > CONFIG['SAFE_TEMP'] or smoke > CONFIG['SAFE_SMOKE']:
            print(f"🔥 EMERGENCY: Temp={temp:.1f}℃, Smoke={smoke:.1f}ppm")
            trigger_alarm("Nighttime Alert")
            break
        
        utime.sleep_ms(CONFIG['NIGHT_CHECK_INTERVAL_MS'])
    
    print("☀️ Resuming normal operation")

# --- Main Loop ---
try:
    while True:
        if in_nighttime_range(get_current_hour()):
            enter_sleep_mode()
        else:
            display_readings()
            utime.sleep_ms(CONFIG['DAY_UPDATE_INTERVAL_MS'])
            
except KeyboardInterrupt:
    clear_alarm()
    print("System stopped by user")
    
