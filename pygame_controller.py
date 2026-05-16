import pygame
import socket
import time

SERVER_IP = "192.168.200.101"
SERVER_PORT = 8081

SEND_INTERVAL = 0.12  # seconds, prevents flooding server


def connect_to_server():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER_IP, SERVER_PORT))
            print("Connected to server")
            return sock
        except OSError:
            print("Server not ready, reconnecting...")
            time.sleep(1)


def send_command(sock, command):
    try:
        sock.sendall((command + "\n").encode("utf-8"))
        return sock
    except OSError:
        print("Connection lost")
        sock.close()
        return connect_to_server()


def get_arrow_command():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        return "SPEED 0 50"
    elif keys[pygame.K_DOWN]:
        return "SPEED 1 50"
    elif keys[pygame.K_LEFT]:
        return "SPEED 2 50"
    elif keys[pygame.K_RIGHT]:
        return "SPEED 3 50"
    else:
        return "SPEED 0 0"


pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Arrow Key TCP Client")

clock = pygame.time.Clock()
sock = connect_to_server()

last_command = None
last_send_time = 0

running = True

while running:
    now = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    command = get_arrow_command()

    command_changed = command != last_command
    time_to_repeat = now - last_send_time >= SEND_INTERVAL

    # Send immediately when command changes
    # Send slowly when holding same key
    if command_changed or time_to_repeat:
        sock = send_command(sock, command)
        last_command = command
        last_send_time = now

    screen.fill((30, 30, 30))
    pygame.display.flip()
    clock.tick(60)

sock.close()
pygame.quit()