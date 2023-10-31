import socket
import time
import sys
import pickle  # For serialization

localIP = "127.0.0.1"
localPort = 8888
bufferSize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and streaming")

class Packet:
    def __init__(self, index, data):
        self.index = index
        self.data = data

packet = Packet(index=0, data=1)
delay = 1  # Default delay

if len(sys.argv) > 1:
    delay = float(sys.argv[1])

while True:
    # Serialize the packet object to bytes using pickle
    serialized_packet = pickle.dumps(packet)

    # Broadcast message to all clients
    UDPServerSocket.sendto(serialized_packet, (localIP, localPort))

    print(f"Index - {packet.index}, Data - {packet.data}")
    packet.index += 1
    packet.data += 1

    time.sleep(delay)