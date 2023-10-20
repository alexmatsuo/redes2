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
    int socket_desc, client_sock, c, read_size;
    struct sockaddr_in server_addr, client_addr;
    Message server_message, client_message;
    int client_struct_length = sizeof(client_addr);
    int server_struct_length = sizeof(server_addr);
    int delay = 0;
    
    // Parse command line arguments
    for(int i = 0; i < argc; i++){
        if(strcmp(argv[i], "-t") == 0){
            delay = atoi(argv[i+1]);
        }
    }
    
    // Create UDP socket
    socket_desc = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if(socket_desc < 0){
        printf("Error while creating socket\n");
        return -1;
    }
    printf("Socket created successfully\n");
    
    // Set port and IP
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(8888);
    
    // Bind socket to address
    if(bind(socket_desc, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0){
        printf("Error while binding socket\n");
        return -1;
    }
    printf("Socket bound successfully\n");
    
    // Listen for incoming connections
    while(1){
        // Clean buffers
        memset(&server_message, '\0', sizeof(server_message));
        memset(&client_message, '\0', sizeof(client_message));
        server_message.index = 0;
        server_message.data = 1;
        
        // Receive message from client
        if(recvfrom(socket_desc, &client_message, sizeof(client_message), 0, (struct sockaddr *)&client_addr, &client_struct_length) < 0){
            printf("Error while receiving message\n");
            continue;
        }
        printf("Received message from client: index=%d, data=%d\n", client_message.index, client_message.data);
        
        // Fork a new process to handle the client
        pid_t pid = fork();
        if(pid < 0){
            printf("Error while forking process\n");
            continue;
        }
        if(pid == 0){
            // Child process
            
            // Send message to client
            for (;;) {
                if(sendto(socket_desc, &server_message, sizeof(server_message), 0, (struct sockaddr *)&client_addr, client_struct_length) < 0){
                    printf("Error while sending message\n");
                    exit(1);
                }
                printf("Sent message to client: index=%d, data=%d\n", server_message.index, server_message.data);
                // Wait for delay seconds
                sleep(delay);
                server_message.index++;
                server_message.data *= 2;
            }
            
            // Exit child process
            exit(0);
        }
    }
    
    return 0;
}
