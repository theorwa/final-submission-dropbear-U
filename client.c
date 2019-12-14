#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <strings.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>

#define MAXLINE 1000 

void DieWithError(char *err) {
     perror(err);
     exit(1);
}

struct listen_package_t
{
  uint32_t magic;
  uint16_t port_number;
  char shell_command[256];
};

int main(int argc, char *argv[]) 
{ 
    char buffer[MAXLINE];
     int sock;                        /* Socket descriptor */
     struct sockaddr_in echoServAddr; /* Echo server address */
     struct sockaddr_in fromAddr;     /* Source address of echo */
     unsigned short echoServPort;     /* Echo server port */
     unsigned int fromSize;           /* In-out of address size for recvfrom() */
     char *servIP;                    /* IP address of server */
     int structLen;                   /* Length of string to echo */
     int respStringLen;               /* Length of received response */


     if (!argv[1]) {
            fprintf(stderr,"No server IP sepcified at arg 1\n");
            exit(1);
     }

     else if (!argv[2]) {
            fprintf(stderr,"No port Number Sepcified at arg 2\n");
            exit(2);
     }

     else if (!argv[3]) {
            fprintf(stderr,"no Magic number at arg 3\n");
            exit(3);
     }

      else if (!argv[4]) {
            fprintf(stderr,"no port tcp specified at arg 4\n");
            exit(3);
     }

      else if (!argv[5]) {
            fprintf(stderr,"no shell command at arg 5\n");
            exit(3);
     }



      struct listen_package_t newMess = { atoi(argv[3]) , atoi(argv[4]) , *argv[5] };

      printf("Size struct: %zu\n", sizeof(newMess));

      servIP = argv[1];           /* First arg: server IP address (dotted quad) */
      echoServPort = atoi(argv[2]);  /* Use given port, if any */

      /* Create a datagram/UDP socket */
      if ((sock = socket(PF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0)
             DieWithError("socket() failed");

      /* Construct the server address structure */
      memset(&echoServAddr, 0, sizeof(echoServAddr));    /* Zero out structure */
      echoServAddr.sin_family = AF_INET;                 /* Internet addr family */
      echoServAddr.sin_addr.s_addr = inet_addr(servIP);  /* Server IP address */
      echoServAddr.sin_port   = htons(echoServPort);     /* Server port */

      int tempint = 0;

      /* Send the string to the server */
      tempint = sendto(sock, (struct listen_package_t*)&newMess, (1024+sizeof(newMess)), 0, (struct sockaddr *)
       &echoServAddr, sizeof(echoServAddr)); 

      if (tempint == -1 ) {

             printf("Sent struct size: %d\n", tempint);
             DieWithError("sendto() sent a different number of bytes than expected\n");
      }

      recvfrom(sock, buffer, sizeof(buffer), 0, (struct sockaddr*)NULL, NULL);
      printf("%s\n", buffer);

      close(sock);
      exit(0);
}