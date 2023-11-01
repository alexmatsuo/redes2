import socket
import pickle
import time
import logging

# Configure logging for the server
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a file handler for writing logs to a file
file_handler = logging.FileHandler('server_logs.log')
file_handler.setLevel(logging.INFO)

# Add the file handler to the logger
logger = logging.getLogger()
logger.addHandler(file_handler)

localIP = "127.0.0.1"
localPort = 8888
bufferSize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

logging.info("UDP server up and streaming")

class Packet:
    def __init__(self, index, data):
        self.index = index
        self.data = data

packet = Packet(index=0, data=1)
delay = 1

while True:
    try:
        serialized_packet = pickle.dumps(packet)
        UDPServerSocket.sendto(serialized_packet, ("127.0.0.1", 8889))
        logging.info(f"Index - {packet.index}, Data - {packet.data}")
        packet.index += 1
        packet.data += 1
        time.sleep(delay)
    except KeyboardInterrupt:
        logging.info("Server stopped.")
        break
