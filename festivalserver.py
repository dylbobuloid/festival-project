import random
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('127.0.0.1', 12000))
print("SERVER RUNNING")



def is_corrupt():
	# 3 Store checkSum number from packet into variable
	# 4 Create checkSum number again using the sequence number, ack flag, payload length, and payload
	# 5.1 Compare the two and if they are the same file not corrupted move onto the next state (chec if ACK flag is 0 if it is make a packet)
	# 6.2 If they are not the same file has been corrupted go back to previous state (waiting to receive festival packet)
	print("hello")

def is_ack():


	print("hello")
	# 7 Checks the acknowledgement flag in the packet whether it is a 0 or 1
	# 8.1 if ACK flag 0 continue and make a packet makePacket()
	# 8.2 if ACK flag 1 go back and



# Make separate class with constructor?
#def makePacket(seq, 0, payloadLen, payload, checkSum):



while True:
	# 1 Wait to receive festival packet from client

    #serverSocket.recvfrom(1024) && isCorrupt(serverSocket.recvfrom(1024)) isAck(serverSocket.recvfrom(1024))

	# Receving packet from the client

	dataFromClient = serverSocket.recvfrom(1024)

	print(dataFromClient)

