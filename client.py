import socket

serverAddressPort = ("127.0.0.1", 20001)  # Server address and port broadcasting
bufferSize = 1024

received_numbers = []  # List to store received sequence numbers

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
UDPClientSocket.bind(("0.0.0.0", 20002))  # Listen on the same port the server is broadcasting

try:
    while True:
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        received_msg = msgFromServer[0].decode()
        sequence = int(received_msg.split(": ")[1])  # Get the number from the message

        received_numbers.append(sequence)
        print(f"Received sequence: {sequence}")

except KeyboardInterrupt:
    print("Closing client...")

# Process the received numbers (calculate the sum)
if received_numbers:
    total_sum = sum(received_numbers)
    print(f"Total Sum of Received Numbers: {total_sum}")
