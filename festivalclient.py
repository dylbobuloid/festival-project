# FestivalClient.py
# We will need the following module to generate randomized lost packets
import sys
import socket
from struct import *

# Create a UDP socket
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 12000
Message = b"Hello, Server"

# create a socket with address and port
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.connect(("127.0.0.1", 12000))

# Prints the message that is being sent
print('sending "%s"' % Message)


def create_packet():
    # Creating packet with the format
    # Sequence number, Ack flag, payload length, payload, checkSum
    packet = pack("i i i 5s i", 1, 0, 5, b"dylan", 1111)
    return packet


try:
    # sent the Message using the clientSock

    sent = clientSock.send(create_packet())
    # Receive response

    print('waiting to receive')

    # get the response & extract data
    message = clientSock.recv(1024)

    print('MESSAGE FROM SERVER: "%s" ' % message.decode("ascii"))


except socket.timeout as inst:
    print('ERROR HAS OCCURRED "%s"' % inst)
    ## handle timeouts

print('closing socket')
clientSock.close()

##close the socket
