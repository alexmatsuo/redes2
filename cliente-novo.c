#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

typedef struct Message {
    int index;
    int data;
} Message;

void handle_client(int socket_desc, struct sockaddr_in client_addr, int addrlen) {
    Message client_message, server_message;

    // Clean buffers:
    memset(&client_message, '\0', sizeof(client_message));
    memset(&server_message, '\0', sizeof(server_message));

    // Receive message from client:
    if (recvfrom(socket_desc, &client_message, sizeof(client_message), 0, (struct sockaddr*)&client_addr, &addrlen) < 0) {
        printf("Error while receiving message\n");
        return;
    }

    // Print the message received:
    printf("Received message from client: %d\n", client_message.data);

    // Send a message to the client:
    server_message.data = client_message.data;
    if (sendto(socket_desc, &server_message, sizeof(server_message), 0, (struct sockaddr*)&client_addr, addrlen) < 0) {
        printf("Error while sending message\n");
        return;
    }

    // Close the socket:
    close(socket_desc);
}

int main(int argc, char *argv[]) {
    int socket_desc;
    struct sockaddr_in server_addr, client_addr;
    Message server_message;
    int addrlen = sizeof(client_addr);
    int i;

    // Clean buffers:
    memset(&server_message, '\0', sizeof(server_message));

    // Create UDP socket:
    socket_desc = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

    if (socket_desc < 0) {
        printf("Error while creating socket\n");
        return -1;
    }
    printf("Socket created successfully\n");

    // Set port and IP:
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(2000);
    server_addr.sin_addr.s_addr = INADDR_ANY;

    // Bind socket to port:
    if (bind(socket_desc, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        printf("Error while binding socket\n");
        return -1;
    }
    printf("Socket bound successfully\n");

    while (1) {
        // Accept a new client:
        if (recvfrom(socket_desc, &server_message, sizeof(server_message), 0, (struct sockaddr*)&client_addr, &addrlen) < 0) {
            printf("Error while accepting client\n");
            continue;
        }

        // Fork a new process to handle the client:
        pid_t pid = fork();
        if (pid == 0) {
            // Child process:
            handle_client(socket_desc, client_addr, addrlen);
            return 0;
        } else if (pid < 0) {
            // Error:
            printf("Error while forking process\n");
            continue;
        } else {
            // Parent process:
            printf("Forked process %d to handle client\n", pid);
        }
    }

    // Close the socket:
    close(socket_desc);

    return 0;
}