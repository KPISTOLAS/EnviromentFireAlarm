from machine import Pin, SPI, ADC
import time
import dht
from cayennelpp import LPPFrame
import sx127x

# Sensor Pin Definitions
DHT_PIN = 15          # GP15 for DHT22
MQ2_PIN = 26           # GP26 (ADC0) for MQ2
RAIN_PIN = 18          # GP18 for rain sensor
WIND_PIN = 28          # GP28 (ADC2) for wind sensor (changed from GP16 to avoid conflict)

# LoRa Pin Definitions
LORA_CS = 13           # GP13
LORA_RST = 12          # GP12
LORA_SCK = 14          # GP14
LORA_MOSI = 15         # GP15
LORA_MISO = 16         # GP16

# Initialize DHT22 sensor
dht_sensor = dht.DHT22(Pin(DHT_PIN))

# Initialize analog sensors
mq2 = ADC(Pin(MQ2_PIN))
wind_sensor = ADC(Pin(WIND_PIN))

# Initialize rain sensor (digital)
rain_sensor = Pin(RAIN_PIN, Pin.IN)

# Initialize LoRa
spi = SPI(0,
          baudrate=10000000,
          polarity=0,
          phase=0,
          bits=8,
          firstbit=SPI.MSB,
          sck=Pin(LORA_SCK),
          mosi=Pin(LORA_MOSI),
          miso=Pin(LORA_MISO))

lora = sx127x.SX127x(spi,
                     pins={'dio_0': 20,  # Not used but required by library
                           'ss': Pin(LORA_CS),
                           'reset': Pin(LORA_RST)},
                     parameters={'frequency': 915E6,  # Adjust for your region
                                'tx_power_level': 14,
                                'signal_bandwidth': 125E3,
                                'spreading_factor': 7,
                                'coding_rate': 5,
                                'preamble_length': 8,
                                'implicitHeader': False,
                                'sync_word': 0x12,
                                'enable_CRC': True})
'''
def read_sensors():
    """Read all sensors and return values"""
    # Read DHT22
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    
    # Read MQ2 (0-65535)
    mq2_value = mq2.read_u16()
    
    # Read Rain Sensor (0 or 1)
    rain_status = rain_sensor.value()
    
    # Read Wind Sensor (0-65535)
    wind_value = wind_sensor.read_u16()
    
    return {
        'temperature': temperature,
        'humidity': humidity,
        'mq2': mq2_value,
        'rain': rain_status,
        'wind': wind_value
    }
'''
def send_lora_data(data):
    """Pack data into Cayenne LPP and send via LoRa"""
    frame = LPPFrame()
    
    # Add data to Cayenne LPP frame
    frame.add_temperature(1, data['temperature'])
    frame.add_humidity(2, data['humidity'])
    frame.add_analog_input(3, data['mq2'] / 65535)  # Scale to 0-1
    frame.add_digital_input(4, data['rain'])
    frame.add_analog_input(5, data['wind'] / 65535)  # Scale to 0-1
    
    # Send LoRa packet
    lora.begin_packet()
    lora.write(frame.bytes())
    lora.end_packet()
    
    print("Packet sent:", frame.bytes())

def main():
    print("Starting LoRa sensor node")
    
    while True:
        try:
            # Read sensors
            sensor_data = read_sensors()
            
            # Print sensor values
                  '''
            print("Temperature: {:.1f}°C".format(sensor_data['temperature']))
            print("Humidity: {:.1f}%".format(sensor_data['humidity']))
            print("MQ2 Value:", sensor_data['mq2'])
            print("Rain Status:", "Dry" if sensor_data['rain'] else "Wet")
            print("Wind Value:", sensor_data['wind'])
            print()
            '''
            
            # Send data via LoRa
            send_lora_data(sensor_data)
            
            # Wait before next transmission
            time.sleep(30)
            
        except Exception as e:
            print("Error:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
