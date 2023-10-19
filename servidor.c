#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>

typedef struct Message{
    int index;
    int data;
} Message;

int main( int argc, char *argv []){
    int socket_desc;
    int delay;
    for(int i=0; i < argc;i++){
        if(argv == '-t'){
            delay = argv[i+1];
        }
    }
    struct sockaddr_in server_addr, client_addr;
    Message server_message, client_message;
    int client_struct_length = sizeof(client_addr);
    int server_struct_length = sizeof(server_addr);
    // Clean buffers:
    memset(&server_message, '\0', sizeof(server_message));
    memset(&client_message, '\0', sizeof(client_message));
    
    // Create UDP socket:
    socket_desc = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    
    if(socket_desc < 0){
        printf("Error while creating socket\n");
        return -1;
    }
    printf("Socket created successfully\n");
    
    // Set port and IP:
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(2000);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    
    // Bind to the set port and IP:
    if(bind(socket_desc, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0){
        printf("Couldn't bind to the port\n");
        return -1;
    }
    printf("Done with binding\n");
    
    printf("Listening for incoming messages...\n\n");

    // Recieve message from client to get address
    if (recvfrom(socket_desc, &client_message, sizeof(client_message), 0,
         (struct sockaddr*)&client_addr, &client_struct_length) < 0){
        printf("Couldn't receive\n");
        return -1;
    }
    printf("Received message from IP: %s and port: %i\n",
           inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
    
    printf("Msg from client: %d\n", client_message.data);
    
    // Send message to clients :
    int j = 0;
    for(int i = 1; i < 33 ; i*=2,j++){
        server_message.index = j;
        server_message.data = i;
        if  (sendto(socket_desc, &server_message, sizeof(server_message), 0, (struct sockaddr*)&client_addr, client_struct_length) < 0){
            printf("Unable to send message\n");
            return -1;
        }
        printf("Sending %d to client\n", server_message.data);
    }
    
    // Respond to client:
    server_message.data = client_message.data;
    
    if (sendto(socket_desc, &server_message, sizeof(server_message), 0,
         (struct sockaddr*)&client_addr, client_struct_length) < 0){
        printf("Can't send\n");
        return -1;
    }
    
    // Close the socket:
    close(socket_desc);
    
    return 0;
}
