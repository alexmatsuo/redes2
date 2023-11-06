import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server's IP address and port number
client_socket.connect(('localhost', 8888))

# Receive data from the server and write it to a file
with open('received_data.txt', 'wb') as file:
    data = client_socket.recv(1024)
    while data:
        file.write(data)
        data = client_socket.recv(1024)

# Close the connection
client_socket.close()