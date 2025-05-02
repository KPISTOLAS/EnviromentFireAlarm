from machine import Pin, SPI
import time
import sx127x
from cayennelpp import LPPFrame

# LoRa Pin Definitions (Receiver Pico)
LORA_CS = 13           # GP13
LORA_RST = 12          # GP12
LORA_SCK = 14          # GP14
LORA_MOSI = 15         # GP15
LORA_MISO = 16         # GP16

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
                     parameters={'frequency': 915E6,  # Must match transmitter
                                'tx_power_level': 2,
                                'signal_bandwidth': 125E3,
                                'spreading_factor': 7, 
                                'coding_rate': 5,
                                'preamble_length': 8,
                                'implicitHeader': False,
                                'sync_word': 0x12,
                                'enable_CRC': True})

def decode_lpp_payload(payload):
    """Decode Cayenne LPP payload and print values"""
    frame = LPPFrame()
    frame.parse(payload)
    
    print("\nReceived Sensor Data:")
    for data in frame.data:
        if data['channel'] == 1 and data['type'] == LPPFrame.TEMPERATURE:
            print(f"Temperature: {data['value']:.1f}°C")
        elif data['channel'] == 2 and data['type'] == LPPFrame.HUMIDITY:
            print(f"Humidity: {data['value']:.1f}%")
        elif data['channel'] == 3 and data['type'] == LPPFrame.ANALOG_INPUT:
            print(f"Air Quality: {data['value'] * 65535:.0f} (raw: {data['value']:.3f})")
        elif data['channel'] == 4 and data['type'] == LPPFrame.DIGITAL_INPUT:
            print(f"Rain: {'No rain' if data['value'] else 'Rain detected'}")
        elif data['channel'] == 5 and data['type'] == LPPFrame.ANALOG_INPUT:
            print(f"Wind: {data['value'] * 65535:.0f} (raw: {data['value']:.3f})")

def main():
    print("Starting LoRa Receiver")
    lora.receive()  # Put radio in receive mode
    
    while True:
        if lora.received_packet():
            print(f"RSSI: {lora.packet_rssi()} dBm | SNR: {lora.packet_snr()} dB")
            
            # Read packet
            payload = lora.read_payload()
            
            try:
                decode_lpp_payload(bytes(payload))
            except Exception as e:
                print("Error decoding packet:", e)
            
            # Return to receive mode
            lora.receive()

if __name__ == "__main__":
    main()
