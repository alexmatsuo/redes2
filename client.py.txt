import socket
import pickle
import logging

# Trata dos logs 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cria um file handler para escrever os logs em um arquivo
file_handler = logging.FileHandler('client_logs.log')
file_handler.setLevel(logging.INFO)

# Cria um formatador para formatar os logs
logger = logging.getLogger()
logger.addHandler(file_handler)

# Classe para definir a estrutura da mensagem
class Packet:
    def __init__(self, index, data):
        self.index = index
        self.data = data

# Tamanho do buffer
bufferSize = 1024

# Configura socket
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Define porta para o cliente
port = 8889

# Tenta fazer bind na porta, se não conseguir, tenta a próxima
binded = False
while not binded:
    try:    
        UDPClientSocket.bind(("127.0.0.1", port))
        binded = True
    except OSError:
        port += 1

# Imprime porta que o cliente está escutando
logging.info("UDP client listening on port: " + str(port) + "\n")

total_data = 0
total_packets_received = 0
previous_index = -1
packets_lost = 0
packets_out_of_order = 0

# Envia mensagem para o servidor para conectar a ele
bytesToSend = str.encode("Connect message")
UDPClientSocket.sendto(bytesToSend, ("127.0.0.1", 8888))

try:
    # Recebe pacotes do servidor e imprime o index e o dado recebido
    while True:
        serialized_packet, _ = UDPClientSocket.recvfrom(bufferSize)
        packet = pickle.loads(serialized_packet)
        total_packets_received += 1

        # Check for packet order and count lost/out of order packets
        if packet.index == previous_index + 1:
            total_data += packet.data
        else:
            if packet.index > previous_index + 1:
                packets_lost += packet.index - (previous_index + 1)
            else:
                packets_out_of_order += 1

        logging.info(f"Received: Index - {packet.index}, Data - {packet.data}")
        previous_index = packet.index

except KeyboardInterrupt:
    # Imprime a soma total de dados recebidos e estatísticas de pacotes
    logging.info(f"Total sum of received data: {total_data}")
    logging.info(f"Total packets received: {total_packets_received}")
    logging.info(f"Total packets lost: {packets_lost}")
    logging.info(f"Packets out of order: {packets_out_of_order}")
