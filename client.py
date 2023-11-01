import socket
import pickle

# localIP = "127.0.0.1"
# localPort = 8888
bufferSize = 1024
serverAddressPort   = ("127.0.0.1", 8888)

msgFromClient = "Hello UDP Server"
bytesToSend = str.encode(msgFromClient)

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

print("UDP client listening")

class Packet:
    def __init__(self, index, data):
        self.index = index
        self.data = data

total_data = 0

UDPClientSocket.sendto(bytesToSend, serverAddressPort)

try:
    while True:
        serialized_packet = UDPClientSocket.recvfrom(bufferSize)
        packet = pickle.loads(serialized_packet)
        print(f"Received: Index - {packet.index}, Data - {packet.data}")
        total_data += packet.data

except KeyboardInterrupt:
    print(f"\nTotal sum of received data: {total_data}\n")
