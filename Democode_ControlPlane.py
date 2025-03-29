import machine
import utime

# ---- PWM INPUT READING ----
class PWMReceiver:
    def __init__(self, pin):
        self.pin = machine.Pin(pin, machine.Pin.IN)
        self.timer = machine.Timer()
        self.start_time = 0
        self.pulse_width = 1500  # Default neutral position

        # Interrupt handler
        self.pin.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.pwm_callback)

    def pwm_callback(self, pin):
        if pin.value() == 1:  # Rising edge
            self.start_time = utime.ticks_us()
        else:  # Falling edge
            self.pulse_width = utime.ticks_diff(utime.ticks_us(), self.start_time)

    def get_value(self):
        return self.pulse_width  # Pulse width in microseconds (1000-2000us)

# ---- INITIALIZE RECEIVER CHANNELS ----
throttle_ch = PWMReceiver(16)  # Throttle (Motor)
aileron_ch = PWMReceiver(17)  # Aileron (Roll)
elevator_ch = PWMReceiver(18)  # Elevator (Pitch)
rudder_ch = PWMReceiver(19)  # Rudder (Yaw)

# ---- PWM OUTPUT SETUP FOR ESC & SERVOS ----
PWM_FREQ = 50  # 50Hz for servos and ESC
motor = machine.PWM(machine.Pin(15))  # ESC (Throttle)
aileron = machine.PWM(machine.Pin(14))  # Roll
elevator = machine.PWM(machine.Pin(13))  # Pitch
rudder = machine.PWM(machine.Pin(12))  # Yaw

# Set frequencies
motor.freq(PWM_FREQ)
aileron.freq(PWM_FREQ)
elevator.freq(PWM_FREQ)
rudder.freq(PWM_FREQ)

# ---- FUNCTION TO MAP RC INPUT TO PWM OUTPUT ----
def map_pwm(value):
    """Convert RC receiver PWM input (1000-2000us) to PWM duty cycle (0-65535)."""
    return int((value - 1000) / 1000 * 65535)

# ---- MAIN LOOP ----
print("Reading RC signals...")
while True:
    try:
        # Read RC signals (1000-2000us)
        throttle_val = throttle_ch.get_value()
        aileron_val = aileron_ch.get_value()
        elevator_val = elevator_ch.get_value()
        rudder_val = rudder_ch.get_value()

        # Map to PWM output
        motor.duty_u16(map_pwm(throttle_val))
        aileron.duty_u16(map_pwm(aileron_val))
        elevator.duty_u16(map_pwm(elevator_val))
        rudder.duty_u16(map_pwm(rudder_val))

        print(f"Throttle: {throttle_val}, Aileron: {aileron_val}, Elevator: {elevator_val}, Rudder: {rudder_val}")
        utime.sleep(0.1)

    except Exception as e:
        print("Error:", e)
