import socket
import pickle

class Packet:
    def __init__(self, index, data):
        self.index = index
        self.data = data

bufferSize = 1024
serverAddressPort = ("127.0.0.1", 8889)

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.bind(("127.0.0.1", 8889))

print("UDP client listening")

total_data = 0

try:
    while True:
        serialized_packet, _ = UDPClientSocket.recvfrom(bufferSize)
        packet = pickle.loads(serialized_packet)
        print(f"Received: Index - {packet.index}, Data - {packet.data}")
        total_data += packet.data
except KeyboardInterrupt:
    print(f"\nTotal sum of received data: {total_data}\n")
