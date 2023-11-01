import socket
import pickle
import logging

# Configure logging for the client
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a file handler for writing logs to a file
file_handler = logging.FileHandler('client_logs.log')
file_handler.setLevel(logging.INFO)

# Add the file handler to the logger
logger = logging.getLogger()
logger.addHandler(file_handler)

class Packet:
    def __init__(self, index, data):
        self.index = index
        self.data = data

bufferSize = 1024
serverAddressPort = ("127.0.0.1", 8889)

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.bind(("127.0.0.1", 8889))

logging.info("UDP client listening")

total_data = 0

try:
    while True:
        serialized_packet, _ = UDPClientSocket.recvfrom(bufferSize)
        packet = pickle.loads(serialized_packet)
        logging.info(f"Received: Index - {packet.index}, Data - {packet.data}")
        total_data += packet.data
except KeyboardInterrupt:
    logging.info(f"Total sum of received data: {total_data}")
