import machine
import utime
import network
import urequests
import ov2640  # Camera driver for OV2640

# ---- WiFi Credentials ----
SSID = "Your_WiFi_SSID"
PASSWORD = "Your_WiFi_Password"
AI_SERVER_URL = "http://192.168.1.100:5000/analyze"  # AI Server (Flask API)

# ---- PWM INPUT READING ----
class PWMReceiver:
    def __init__(self, pin):
        self.pin = machine.Pin(pin, machine.Pin.IN)
        self.timer = machine.Timer()
        self.start_time = 0
        self.pulse_width = 1500  # Default neutral position
        self.pin.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.pwm_callback)

    def pwm_callback(self, pin):
        if pin.value() == 1:  # Rising edge
            self.start_time = utime.ticks_us()
        else:  # Falling edge
            self.pulse_width = utime.ticks_diff(utime.ticks_us(), self.start_time)

    def get_value(self):
        return self.pulse_width  # Pulse width in microseconds (1000-2000us)

# ---- INITIALIZE RECEIVER CHANNELS ----
throttle_ch = PWMReceiver(16)
aileron_ch = PWMReceiver(17)
elevator_ch = PWMReceiver(18)
rudder_ch = PWMReceiver(19)

# ---- PWM OUTPUT SETUP FOR ESC & SERVOS ----
PWM_FREQ = 50  # 50Hz for servos and ESC
motor = machine.PWM(machine.Pin(15))  
aileron = machine.PWM(machine.Pin(14))  
elevator = machine.PWM(machine.Pin(13))  
rudder = machine.PWM(machine.Pin(12))  

motor.freq(PWM_FREQ)
aileron.freq(PWM_FREQ)
elevator.freq(PWM_FREQ)
rudder.freq(PWM_FREQ)

# ---- FUNCTION TO MAP RC INPUT TO PWM OUTPUT ----
def map_pwm(value):
    """Convert RC receiver PWM input (1000-2000us) to PWM duty cycle (0-65535)."""
    return int((value - 1000) / 1000 * 65535)

# ---- CONNECT TO WiFi ----
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while not wlan.isconnected():
        utime.sleep(1)
    
    print("Connected to WiFi:", wlan.ifconfig())

# ---- CAPTURE IMAGE ----
def capture_image():
    camera = ov2640.OV2640()
    camera.init()
    camera.set_pixformat(ov2640.PIXFORMAT_JPEG)
    camera.set_framesize(ov2640.FRAME_SIZE_QVGA)  # 320x240 resolution
    img = camera.capture()
    
    with open("image.jpg", "wb") as f:
        f.write(img)
    
    print("Image Captured!")
    return img

# ---- SEND IMAGE TO AI SERVER ----
def send_image(img):
    headers = {"Content-Type": "image/jpeg"}
    response = urequests.post(AI_SERVER_URL, headers=headers, data=img)
    print("AI Response:", response.text)
    return response.text

# ---- MAIN LOOP ----
print("Starting Drone Control and AI Vision System...")
connect_wifi()

while True:
    try:
        # ---- Read RC Signals ----
        throttle_val = throttle_ch.get_value()
        aileron_val = aileron_ch.get_value()
        elevator_val = elevator_ch.get_value()
        rudder_val = rudder_ch.get_value()

        # ---- Control Servos and Motor ----
        motor.duty_u16(map_pwm(throttle_val))
        aileron.duty_u16(map_pwm(aileron_val))
        elevator.duty_u16(map_pwm(elevator_val))
        rudder.duty_u16(map_pwm(rudder_val))

        print(f"Throttle: {throttle_val}, Aileron: {aileron_val}, Elevator: {elevator_val}, Rudder: {rudder_val}")

        # ---- Capture and Send Image Every 5 Seconds ----
        if utime.ticks_ms() % 5000 < 100:  # Capture every ~5 seconds
            img = capture_image()
            send_image(img)

        utime.sleep(0.1)

    except Exception as e:
        print("Error:", e)
