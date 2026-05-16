from machine import Pin, PWM
import time

# Define the pins connected to the L298N
#FrontRightWheel
FR_IN1_PIN = 0
FR_IN2_PIN = 1
FR_ENA_PIN = 2

FR_IN3_PIN = 3
FR_IN4_PIN = 4
FR_ENB_PIN = 5

#rear wheel
FR_IN5_PIN = 6
FR_IN6_PIN = 7
FR_ENC_PIN = 8

FR_IN7_PIN = 9
FR_IN8_PIN = 10
FR_END_PIN = 11

# Initialize the pins as output
FR_in1 = Pin(FR_IN1_PIN, Pin.OUT)
FR_in2 = Pin(FR_IN2_PIN, Pin.OUT)
FR_ena = PWM(Pin(FR_ENA_PIN))

# Initialize the pins as output
FR_in3 = Pin(FR_IN3_PIN, Pin.OUT)
FR_in4 = Pin(FR_IN4_PIN, Pin.OUT)
FR_enb = PWM(Pin(FR_ENB_PIN))

# Initialize the pins as output
FR_in5 = Pin(FR_IN5_PIN, Pin.OUT)
FR_in6 = Pin(FR_IN6_PIN, Pin.OUT)
FR_enc = PWM(Pin(FR_ENC_PIN))

# Initialize the pins as output
FR_in7 = Pin(FR_IN7_PIN, Pin.OUT)
FR_in8 = Pin(FR_IN8_PIN, Pin.OUT)
FR_end = PWM(Pin(FR_END_PIN))

# Configure PWM frequency (e.g., 1000 Hz)
FR_ena.freq(1000)
FR_enb.freq(1000)
FR_enc.freq(1000)
FR_end.freq(1000)

def stop_motor():
    FR_in1.value(0)
    FR_in2.value(0)
    FR_ena.duty_u16(0) # Stop the motor
    
    FR_in3.value(0)
    FR_in4.value(0)
    FR_enb.duty_u16(0) # Stop the motor

    FR_in5.value(0)
    FR_in6.value(0)
    FR_enc.duty_u16(0) # Stop the motor
    
    FR_in7.value(0)
    FR_in8.value(0)
    FR_end.duty_u16(0) # Stop the motor  
    print("Motor stopped")

def move_forward(speed_percent):
    # Speed is a percentage (0 to 100), converted to 0-65535 for duty_u16
    speed_value = int(speed_percent / 100 * 65535)
    #in1.value(1) # Set direction
    #in2.value(0)
    #ena.duty_u16(speed_value) # Set speed
    FR_in1.value(0) # Set direction
    FR_in2.value(1)
    FR_ena.duty_u16(speed_value) # Set speed
    
    FR_in3.value(1) # Set direction
    FR_in4.value(0)
    FR_enb.duty_u16(speed_value) # Set speed

    FR_in5.value(0) # Set direction
    FR_in6.value(1)
    FR_enc.duty_u16(speed_value) # Set speed
    
    FR_in7.value(0) # Set direction
    FR_in8.value(1)
    FR_end.duty_u16(speed_value) # Set speed    
    print(f"Moving forward at {speed_percent}% speed")

def move_backward(speed_percent):
    speed_value = int(speed_percent / 100 * 65535)
    FR_in1.value(1) # Set direction
    FR_in2.value(0)
    FR_ena.duty_u16(speed_value) # Set speed
    FR_in3.value(0) # Set direction
    FR_in4.value(1)
    FR_enb.duty_u16(speed_value) # Set speed
    
    FR_in5.value(1) # Set direction
    FR_in6.value(0)
    FR_enc.duty_u16(speed_value) # Set speed
    FR_in7.value(1) # Set direction
    FR_in8.value(0)
    FR_end.duty_u16(speed_value) # Set speed       
    print(f"Moving backward at {speed_percent}% speed")

# Main test sequence
try:
    move_forward(35)
    time.sleep(3) # Run for 3 seconds

    stop_motor()
    time.sleep(1) # Stop for 1 second

    move_backward(35)
    time.sleep(3) # Run backward for 3 seconds

    stop_motor()

except KeyboardInterrupt:
    stop_motor() # Ensure motor stops on manual interruption



