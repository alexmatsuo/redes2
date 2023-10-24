import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP address and port number
server_socket.bind(('localhost', 8888))

# Listen for incoming connections
server_socket.listen()

# Start sending data to clients
while True:
    # Accept a new connection
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} has been established!")

    # Send data to the client
    with open('data.txt', 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)

    # Close the connection
    client_socket.close()