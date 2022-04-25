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
    # Recreates the checksum of the packet
    h = hashlib.new('md5')
    h.update(pickle.dumps(pkt))

    return h.hexdigest()


def create_packet():
    # Creating packet with the format
    # Creating acknowledgement packet

    seq_num = 0
    ack_flag = 0
    payload = b""
    pay_len = len(payload)

    # Converting each number to 4 bytes as specified in RFC format
    seq_num = seq_num.to_bytes(4, byteorder="little")
    ack_flag = ack_flag.to_bytes(4, byteorder="little")
    pay_len = pay_len.to_bytes(4, byteorder="little")

    # Sequence number, Ack flag, payload length, payload, checkSum

    pkt_no_checksum = seq_num + ack_flag + pay_len + payload
    checksum_num = checksum(pkt_no_checksum)

    checksum_num = checksum_num.encode('ascii')

    # Concatenate all together to create packet
    pkt = seq_num + ack_flag + pay_len + payload + checksum_num

    return pkt


while True:
    # Receiving packet from the client
    client_data = serverSocket.recvfrom(1024)

    # Data client has sends both the packet and the address it has received it from
    # packet from client
    packet = client_data[0]

    # save the address it has received it from
    address = client_data[1]

    # Checking that the packet received is valid and that it is not corrupt

    if not is_corrupt(packet):
        print("TEST SUCCESSFUL PACKET IS NOT CORRUPTED")
        print("SENDING ACKNOWLEDGEMENT PACKET")
        # Sending acknowledgement packet to the client
        serverSocket.sendto(create_packet(), address)


    else:
        print("CORRUPTED")
