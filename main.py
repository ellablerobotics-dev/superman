# motor_server.py (Raspberry Pi Pico W, MicroPython)
import network
import socket
import time
from machine import Pin, PWM

WIFI_SSID = "superman"
WIFI_PASSWORD = "myherostudent"

PORT = 8081

# ===Worm Motors ====
# Define the pins connected to the L298N
#FrontRightWheel
FR_IN1_PIN = 0
FR_IN2_PIN = 1
FR_ENA_PIN = 2

#FrontLeftWheel
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

STEP = 5                    # UP/DOWN step in percent

# 0..100 speed percent mapped to PWM duty
speed_percent = 0

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

#usage
#(wheel, direction, speed) --> (which wheel, direction, speed)
#wheel: front1, front2, rear3, rear4
#direction: forward, backward
#speed: 0-100
def move_wheel(wheel, direction, speed):  #value: front1, forward, 0-100
    speed_value = int(speed / 100 * 65535)  #convert speed 0-100 to sensor value
    
    if wheel=="front1":
        if(direction=="forward"):
            FR_in1.value(0) # Set direction
            FR_in2.value(1)
        else:
            FR_in1.value(1) # Set direction
            FR_in2.value(0)
            
        FR_ena.duty_u16(speed_value) # Set speed        
    elif wheel=="front2":
        if(direction=="forward"):
            FR_in3.value(1) # Set direction
            FR_in4.value(0)
        else:
            FR_in3.value(0) # Set direction
            FR_in4.value(1)
            
        FR_enb.duty_u16(speed_value) # Set speed
    elif wheel=="rear1":
        if(direction=="forward"):
            FR_in5.value(1) # Set direction
            FR_in6.value(0)
        else:
            FR_in5.value(0) # Set direction
            FR_in6.value(1)
        
        FR_enc.duty_u16(speed_value) # Set speed
    elif wheel=="rear2":
        if(direction=="forward"):
            FR_in7.value(0) # Set direction
            FR_in8.value(1)
        else:
            FR_in7.value(1) # Set direction
            FR_in8.value(0)
        
        FR_end.duty_u16(speed_value) # Set speed        
    else:
        print("do nothing yet")
        

    
def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        print("Connecting Wi-Fi...")
        for _ in range(40):  # ~20s
            if wlan.isconnected():
                break
            time.sleep(0.5)
    if not wlan.isconnected():
        raise RuntimeError("Wi-Fi failed")
    ip = wlan.ifconfig()[0]
    print("Wi-Fi connected, IP:", ip)
    return ip

def handle_command(line: str) -> str:
    """
    Commands:
      SPEED <0-3> <0-100>    0 means forward, 1 means backward, 2 means left, 3 means right    
    """
    line = (line or "").strip()
    if not line:
        return "ERR empty"

    parts = line.upper().split()
    cmd = parts[0]
    cmddirection=parts[1]
    cmdspeed = parts[2]
    print("Print cmd:", cmd)
    print("Print direction (0 forward, 1 backward, 2 left, 3 right): ", cmddirection)
    print("Speed: ", cmdspeed)
    
    if cmd == "SPEED":
        print("Start signal")
        if len(parts) != 3:
            return "ERR usage: SPEED 0-100"
        try:
            direction = int(parts[1])  #finalize direction
            speed_p = int(parts[2])	   #finalize speed
        except ValueError:
            return "ERR not a number"

        print(f"OK, {speed_percent} {direction}")
        
        if direction==0: #forward
            move_wheel("front1", "forward", speed_p)  #value: front1, forward, 0-100
            move_wheel("front2", "forward", speed_p)  #value: front2, forward, 0-100
            move_wheel("rear1", "forward", speed_p)  #value: rear1, forward, 0-100
            move_wheel("rear2", "forward", speed_p)  #value: rear2, forward, 0-100
        elif direction==1: #backward
            move_wheel("front1", "backward", speed_p)  #value: front1, forward, 0-100
            move_wheel("front2", "backward", speed_p)  #value: front2, forward, 0-100
            move_wheel("rear1", "backward", speed_p)  #value: rear1, forward, 0-100
            move_wheel("rear2", "backward", speed_p)  #value: rear2, forward, 0-100
        elif direction==2: #left
            move_wheel("front1", "forward", speed_p)  #value: front1, forward, 0-100
            move_wheel("front2", "backward", speed_p)  #value: front2, forward, 0-100
            move_wheel("rear1", "forward", speed_p)  #value: rear1, forward, 0-100
            move_wheel("rear2", "backward", speed_p)  #value: rear2, forward, 0-100
        elif direction==3: #right
            move_wheel("front1", "backward", speed_p)  #value: front1, forward, 0-100
            move_wheel("front2", "forward", speed_p)  #value: front2, forward, 0-100
            move_wheel("rear1", "backward", speed_p)  #value: rear1, forward, 0-100
            move_wheel("rear2", "forward", speed_p)  #value: rear2, forward, 0-100
        else:
            stop_motor()
        return "OK SPEED {}".format(speed_p)

    if cmd == "STOP":
        stop_motor()
        return "OK STOP"

    if cmd == "GET":
        return "OK SPEED {}".format(speed_percent)
    
    return "ERR unknown (SPEED/UP/DOWN/STOP/GET)"

def run_server():
    ip = wifi_connect()
    stop_motor()

    s = socket.socket()
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except Exception:
        pass

    s.bind((ip, PORT))
    s.listen(1)
    print("Motor server listening on {}:{}".format(ip, PORT))

    while True:
        client, addr = s.accept()
        try:
            client.settimeout(5)
            data = client.recv(128)
            if not data:
                client.close()
                continue

            line = data.decode("utf-8", "ignore")
            # only first line
            line = line.split("\n")[0].split("\r")[0]
            print("From", addr, ":", repr(line))

            resp = handle_command(line)
            client.send((resp + "\n").encode("utf-8"))
        except Exception as e:
            try:
                client.send(("ERR " + str(e) + "\n").encode("utf-8"))
            except Exception:
                pass
        finally:
            client.close()

run_server()

