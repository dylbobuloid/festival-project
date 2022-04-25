import hashlib
import pickle
import random
from struct import *
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('127.0.0.1', 13000))
print("SERVER RUNNING")


def rdt_recv(rcvpkt):
    # packet = rcvpkt.decode()

    # Sequence number, Ack flag, payload length, payload, checkSum

    packet = unpack("i i i 9s 32s ", rcvpkt)

    # Assigning each item from tuple to appropriate variable
    seq_num = packet[0]
    ack_flag = packet[1]
    pay_len = packet[2]

    payload = packet[3].decode("ascii")
    check_sum = packet[4].decode("ascii")


def is_corrupt(packet):
    # 3 Store checkSum number from packet into variable
    # 4 Create checkSum number again using the sequence number, ack flag, payload length, and payload

    # Recreate packet without the checksum number at the end

    packet = unpack("i i i 9s 32s ", packet)

    check_sum = packet[4]

    # Sequence number, Ack flag, payload length, payload, checkSum
    new_checksum = checksum(pack("i i i 9s 32s", packet[0], packet[1], packet[2], packet[3], packet[4]))

    # if checksum value is the same return true
    if check_sum == new_checksum:
        return True

    # if checksum value not the same return false
    elif check_sum != new_checksum:
        return False


def checksum(pkt):
    # Turns packet into a tuple
    packet_with_checksum = unpack("i i i 9s 32s", pkt)
    # Takes checkSum out of that packet
    check_sum = packet_with_checksum[4].decode("ascii")

    # Recreates the checksum of the packet
    h = hashlib.new('md5')
    h.update(pickle.dumps(pkt))

    return h.hexdigest()


while True:
    # 1 Wait to receive festival packet from client

    # serverSocket.recvfrom(1024) && isCorrupt(serverSocket.recvfrom(1024))

    # Receving packet from the client

    client_data = serverSocket.recvfrom(1024)
    print(client_data)

    # Data client has sends both the packet and the address it has received it from

    # packet from client
    packet = client_data[0]

    # save the address it has received it from
    address = client_data[1]

    # Checking that the packet received is valid and that it is not corrupt

    if not is_corrupt(packet):
        print("TEST SUCCESSFUL PACKET IS NOT CORRUPTED")
    else:
        print("CORRUPTED")


