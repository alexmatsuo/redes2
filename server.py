import socket
import time
import sys
import pickle 

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
message = 0
delay = 1  # Default delay

if len(sys.argv) > 1:
    delay = float(sys.argv[1])

while True:
    try:
        # Serialize the packet object to bytes using pickle
        serialized_packet = pickle.dumps(packet)
        UDPServerSocket.sendto(serialized_packet, (localIP, localPort))

        print(f"Index - {packet.index}, Data - {packet.data}")
        packet.index += 1
        packet.data += 1
        message += 1
        time.sleep(delay)
    except KeyboardInterrupt:
        print("\n")
        break