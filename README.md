# Add a new command-line switch -U to the Dropbear ssh server

Author: Orwa Watad

This command-line switch (e.g. dropbear -U) will make dropbear wait for UDP packet on port 53 (by default).

A specific UDP port can be opened with the command-line -p (e.g. dropbear -Up port_number).

By sending valid packets, you can open new TCP ports for the server. then the server does not need to run again.

## Content files

What the folder contains:

- dropbear-source.zip - this zip file contains the source code from this link [Dropbear SSH](https://matt.ucc.asn.au/dropbear/dropbear.html)
- dropbear-U - this zip file contains the code of the server after my changes to add a new command-line switch -U

## build

First, unzip the attached file "dropbear-U.zip", in addition to server files, you will find the following files:
- client.c - I created it while working on the server for an experiment.
- client.py - Python script sends a packet to a UDP port (with a specific struct).
- test.py - Python script to test the server if it is working properly after adding the command-line switch.

To build the server, enter the following commands while you are in the folder (I have been using powers 'sudo'):

```bash
make clean
./configure
make
```

## Run

To run the server with and wait for UDP packet on port 53:

```bash
dropbear -U
```

Then the server will open port number 53 and wait for UDP packet.

You can check open ports by this command:

```bash
netstat -tulpn
```

To open a specific new TCP port you should use the python script 'client.py' with the following command:

```bash
python3 client.py
```

Follow the instructions that appear, then send the package.

For Example (with python script - client.py):

```bash
ubuntu@ubuntu:~/Documents/GitHub/dropbear$ python3 client.py 
Hello, to send packets please enter the following data:
please enter the destination address (empty is your local address): 
please enter the destination port: 53
please enter the magic number: 0xDEADBEEF
please enter the new port for tcp: 22
please enter the shell command: 
msg from server: The magic number is correct! -> The port opened successfully.
```

For Example (with c file - client.c):

```bash
ubuntu@ubuntu:~/Documents/GitHub/dropbear$ ./client 192.168.146.130 53 3735928559 22 null
Size struct: 264
The magic number is correct! -> The port opened successfully.
```



You can monitor the ports via the command I mentioned earlier.

NOTICE:

- To send a packet with 'client.py', the magic number can be written in two ways: 0xDEADBEEF or DEADBEEF.
- To send a packet with 'client.c', the magic number can be written only in the following way: 3735928559.

The structure of the packet that the client sends is as follows:

```c
struct listen_package_t
{
    uint32_t magic;
    uint16_t port_number;
    char shell_command[256];
};
```


## Testing

Attached a file named: test.py
It can be run by the following command:

```bash
python3 test.py
```

For example:


```bash
ubuntu@ubuntu:~/Documents/GitHub/dropbear$ python3 test.py
----------------------------------------------------------------------
Ran 10 tests in 0.052s

OK
```

# Valgrind

I tested the original code with valgrind and my code after changes and get the same result:

The source code with this command: 'sudo valgrind --leak-check=full dropbear', And open some ports.
```bash
==18631== Warning: noted but unhandled ioctl 0x5441 with no size/direction hints.
==18631==    This could cause spurious value errors to appear.
==18631==    See README_MISSING_SYSCALL_OR_IOCTL for guidance on writing a proper wrapper.
==18633== could not unlink /tmp/vgdb-pipe-from-vgdb-to-18633-by-root-on-???
==18633== could not unlink /tmp/vgdb-pipe-to-vgdb-from-18633-by-root-on-???
==18633== could not unlink /tmp/vgdb-pipe-shared-mem-vgdb-18633-by-root-on-???
==18631== 
==18631== HEAP SUMMARY:
==18631==     in use at exit: 65 bytes in 1 blocks
==18631==   total heap usage: 4,705 allocs, 4,704 frees, 782,397 bytes allocated
==18631== 
==18631== LEAK SUMMARY:
==18631==    definitely lost: 0 bytes in 0 blocks
==18631==    indirectly lost: 0 bytes in 0 blocks
==18631==      possibly lost: 0 bytes in 0 blocks
==18631==    still reachable: 65 bytes in 1 blocks
==18631==         suppressed: 0 bytes in 0 blocks
==18631== Reachable blocks (those to which a pointer was found) are not shown.
==18631== To see them, rerun with: --leak-check=full --show-leak-kinds=all
==18631== 
==18631== For counts of detected and suppressed errors, rerun with: -v
==18631== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
The code after changes with this command: 'sudo valgrind --leak-check=full dropbear -U' And open some ports.
```bash
==18565== Warning: noted but unhandled ioctl 0x5441 with no size/direction hints.
==18565==    This could cause spurious value errors to appear.
==18565==    See README_MISSING_SYSCALL_OR_IOCTL for guidance on writing a proper wrapper.
==18566== could not unlink /tmp/vgdb-pipe-from-vgdb-to-18566-by-root-on-???
==18566== could not unlink /tmp/vgdb-pipe-to-vgdb-from-18566-by-root-on-???
==18566== could not unlink /tmp/vgdb-pipe-shared-mem-vgdb-18566-by-root-on-???
==18565== 
==18565== HEAP SUMMARY:
==18565==     in use at exit: 65 bytes in 1 blocks
==18565==   total heap usage: 4,754 allocs, 4,753 frees, 803,759 bytes allocated
==18565== 
==18565== LEAK SUMMARY:
==18565==    definitely lost: 0 bytes in 0 blocks
==18565==    indirectly lost: 0 bytes in 0 blocks
==18565==      possibly lost: 0 bytes in 0 blocks
==18565==    still reachable: 65 bytes in 1 blocks
==18565==         suppressed: 0 bytes in 0 blocks
==18565== Reachable blocks (those to which a pointer was found) are not shown.
==18565== To see them, rerun with: --leak-check=full --show-leak-kinds=all
==18565== 
==18565== For counts of detected and suppressed errors, rerun with: -v
==18565== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
==18537== 
==18537== HEAP SUMMARY:
==18537==     in use at exit: 0 bytes in 0 blocks
==18537==   total heap usage: 124 allocs, 124 frees, 81,563 bytes allocated
==18537== 
==18537== All heap blocks were freed -- no leaks are possible
==18537== 
==18537== For counts of detected and suppressed errors, rerun with: -v
==18537== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
``` 

------


## Where changes have occurred:

-- Complete changes can be found [HERE](https://github.com/theorwa/dropbear-2019.78/commit/33fc0cc880547305643065783f193460fabcad0f)

Most of the changes occurred in the main file: svr_main.c

But I also needed to make minor changes to the following files:

- default_options.h 
```c
#define DROPBEAR_DEFPORT_UDP "53"
```
- runopts.h
```c
bool is_udp;
```
- svr-runopts.c
```c
"-U   	Listen for UDP packet on port 53" // Orwa Watad

...

case 'U':
	  svr_opts.is_udp = true;
	  break;

...

if (svr_opts.is_udp)
	svr_opts.ports[0] = m_strdup(DROPBEAR_DEFPORT_UDP);
else
	svr_opts.ports[0] = m_strdup(DROPBEAR_DEFPORT);
```

- sysoptions.h

```c
#define MAX_LISTEN_ADDR_UDP (DROPBEAR_MAX_PORTS*3) // Orwa Watad
```

- netio.c (in the function: dropbear_listen)

```c
if (svr_opts.is_udp){
	hints.ai_socktype = SOCK_DGRAM;
}
else{
	hints.ai_socktype = SOCK_STREAM;
}

...

if (!svr_opts.is_udp) // Orwa Watad
	set_sock_nodelay(sock);

...

if (!svr_opts.is_udp){
	if (listen(sock, DROPBEAR_LISTEN_BACKLOG) < 0){
          // code
	}
}
```

------

## Changes in the main file (svr_main.c):

```c
#ifndef MAGIC_KEY
#define MAGIC_KEY 0xDEADBEEF
#endif

struct listen_package_t
{
    uint32_t magic;
    uint16_t port_number;
    char shell_command[256];
};

...

int listensocks_udp[MAX_LISTEN_ADDR_UDP]; // Orwa watad
size_t listensockcount_udp = 0; // Orwa watad

...

if (svr_opts.is_udp)
	/* Set up the listening sockets */ // UDP
	listensockcount_udp = listensockets(listensocks_udp, MAX_LISTEN_ADDR_UDP, &maxsock, true);
else
	/* Set up the listening sockets */ // TCP
	listensockcount = listensockets(listensocks, MAX_LISTEN_ADDR, &maxsock, false);

if (listensockcount == 0 && listensockcount_udp == 0)
{
	dropbear_exit("No listening ports available.");
}

for (i = 0; i < listensockcount_udp; i++) {
	FD_SET(listensocks_udp[i], &fds);
}

...

// Inside for(;;) with select

for (i = 0; i < listensockcount_udp; i++) {
	FD_SET(listensocks_udp[i], &fds);
}

...

for (i = 0; i < listensockcount_udp; i++) {
	if (!FD_ISSET(listensocks_udp[i], &fds)) 
		continue;
        .... // handle each UDP socket wich has somthing to say (package has arrived)

...

// 'listensockets' function

svr_opts.is_udp = is_udp; // Enables dropbear_listen function yo open a new TCP port

```


## What I learned from this task



## License
[MIT](https://choosealicense.com/licenses/mit/)