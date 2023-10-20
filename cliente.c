#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Message{
    int index;
    int data;
} Message;

int main(int argc, char *argv[]) {
    int socket_desc, server_struct_length, read_size;
    struct sockaddr_in server_addr;
    Message server_message, client_message;
    server_struct_length = sizeof(server_addr);
    
    // Clean buffers:
    memset(&server_message, '\0', sizeof(server_message));
    memset(&client_message, '\0', sizeof(client_message));
    
    // Create socket:
    socket_desc = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    
    if(socket_desc < 0){
        printf("Error while creating socket\n");
        return -1;
    }
    printf("Socket created successfully\n");
    
    // Set port and IP:
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(8888);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    
    // Send the message to server:
    client_message.data = 1;
    client_message.index = 0;
    if(sendto(socket_desc, &client_message, sizeof(client_message), 0,
         (struct sockaddr*)&server_addr, server_struct_length) < 0){
        printf("Unable to send message\n");
        return -1;
    }
    
    printf("Message sent successfully\n");
    // Receive the server's response:
    for (;;) {

        if(recvfrom(socket_desc, &server_message, sizeof(server_message), 0,
            (struct sockaddr*)&server_addr, &server_struct_length) < 0){
            printf("Error while receiving server's msg\n");
            return -1;
        }
        
        printf("Received message from server: index=%d, data=%d\n", server_message.index, server_message.data);
    }
    
    return 0;
}