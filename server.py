import socket
import pickle
import time
import logging
import sys

# Configurações de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cria um handler para salvar os logs em um arquivo
file_handler = logging.FileHandler('server_logs.log')
file_handler.setLevel(logging.INFO)

# Cria um formatador de logs
logger = logging.getLogger()
logger.addHandler(file_handler)

# Configurações do servidor
localIP = "127.0.0.1"
localPort = 8888
bufferSize = 1024

# Cria o socket UDP
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

# Mensagem de inicialização do servidor
logging.info("UDP server up and streaming")

# Classe que representa um pacote
class Packet:
    def __init__(self, index, data):
        self.index = index
        self.data = data

# Cria um pacote inicial
packet = Packet(index=0, data=2)

# Delay padrão entre cada envio de pacote
delay = 1

# Se o usuário passar um delay como argumento, usa o delay passado
if len(sys.argv) > 1:
    delay = float(sys.argv[1])

# Lista de clientes conectados
clients_connected = []

# Faz o socket não bloquear a execução do programa
UDPServerSocket.settimeout(0)

while True:
    try:
        # Serializa o pacote
        serialized_packet = pickle.dumps(packet)
        
        # Tenta receber dados do cliente
        try: 
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        except BlockingIOError:
            bytesAddressPair = None
            
        # Tenta adicionar o cliente na lista de clientes conectados
        try:
            clients_connected.append(bytesAddressPair[1])
        except:
            pass
        
        # Se a lista de clientes conectados não estiver vazia, envia o pacote para todos os clientes conectados
        if clients_connected:
            for client in clients_connected:
                UDPServerSocket.sendto(serialized_packet, client)
                logging.info(f"Client - {client[0]}:{client[1]}, Index - {packet.index}, Data - {packet.data}")
            print()
            packet.index += 1
            packet.data += 2
        # Espera um tempo antes de enviar o próximo pacote
        time.sleep(delay)
    except KeyboardInterrupt:
        logging.info("Server stopped.")
        break
