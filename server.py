import socket
import time
import sys

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and streaming")

sequence = 0
delay = 1  # Default delay

if len(sys.argv) > 1:
    delay = float(sys.argv[1])

while True:
    sequence += 1
    message = f"Sequence: {sequence}"
    bytesToSend = str.encode(message)

    # Broadcast message to all clients
    UDPServerSocket.sendto(bytesToSend, (localIP, localPort))

    print(f"Streamed: {message}")

    time.sleep(delay)
