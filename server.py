import socket
import pickle
import time

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
delay = 1

while True:
    try:
        serialized_packet = pickle.dumps(packet)
        UDPServerSocket.sendto(serialized_packet, ("127.0.0.1", 8889))  # Send to client's address and port
        print(f"Index - {packet.index}, Data - {packet.data}")
        packet.index += 1
        packet.data += 1
        time.sleep(delay)
    except KeyboardInterrupt:
        print("\n")
        break
