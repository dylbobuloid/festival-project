import hashlib
import pickle
from struct import *
from socket import *
from random import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('127.0.0.1', 1062))
print("SERVER RUNNING")

# List of whitelisted IPs
listOfIps = ['192.168.1.72', '192.168.86.70', '192.168.1.253']

# Dictionary of festivals  Key: Value
festival_dict = {"Christmas": "Merry Christmas", "Diwali": "Happy Diwali", "Easter": "Happy Easter",
                 "Eid": "Eid Mubarak"}


def festival_reply(festival):
    if festival in festival_dict:
        for key in festival_dict:
            if festival == key:
                return festival_dict.get(key)

    else:
        print("No greeting found for festival {} is not supported with our protocol".upper().format(festival.upper()))


def is_corrupt(packet):
    # 3 Store checkSum number from packet into variable
    # 4 Create checkSum number again using the sequence number, ack flag, payload length, and payload

    # Recreate packet without the checksum number at the end

    # seq_num = int.from_bytes(packet[0:4], "big")
    seq_num = packet[0:4]
    ack_flag = packet[4:8]
    pay_len = packet[8:12]
    payloadLength = int.from_bytes(pay_len, byteorder='big')
    # Added 12 to payloadLength.
    payload = packet[12:payloadLength + 12]

    check_sum = packet[payloadLength + 12:]
    packet_to_check = seq_num + ack_flag + pay_len + payload

    # Sequence number, Ack flag, payload length, payload, checkSum
    new_checksum = checksum(packet_to_check)

    # if checksum value is the same return false
    if check_sum == new_checksum:
        return False

    # if checksum value not the same return true
    elif check_sum != new_checksum:
        return True


def checksum(pkt):
    h = hashlib.new('md5')
    h.update(pickle.dumps(pkt))
    # Checksum wont match because of hexdigest.
    return h.digest()


def create_packet(seq, ack, pay_load):
    # Creating packet with the format
    # Creating acknowledgement packet
    pay_len = len(pay_load)
    seq_num = seq
    ack_flag = ack
    payload = pay_load
    pay_len = len(payload.encode("ascii"))

    # Need to pad the payload with extra characters since it is not at the maximum number of bytes
    # Padding payload with " " character

    # Removed method to add extra characters.

    payload = payload.encode("ascii")

    # Converting each number to 4 bytes as specified in RFC format
    seq_num = seq_num.to_bytes(4, byteorder="big")
    ack_flag = ack_flag.to_bytes(4, byteorder="big")
    pay_len = pay_len.to_bytes(4, byteorder="big")

    # Sequence number, Ack flag, payload length, payload, checkSum

    pkt_no_checksum = seq_num + ack_flag + pay_len + payload
    checksum_num = checksum(pkt_no_checksum)

    # checksum_num = checksum_num.encode('ascii')

    # Concatenate all together to create packet
    pkt = seq_num + ack_flag + pay_len + payload + checksum_num

    return pkt


def is_ack(packet):
    # Sequence number, Ack flag, payload length, payload, checkSum

    ack_flag = int.from_bytes(packet[4:8], "big")

    if ack_flag == 1:
        return True
    else:
        return False


while True:
    # Receiving packet from the client
    client_data = serverSocket.recvfrom(2048)

    # Data client has sends both the packet and the address it has received it from
    # packet from client
    packet = client_data[0]

    # Saving the sequence number
    seq_num = int.from_bytes(packet[0:4], byteorder="big")

    # Saving payload length
    pay_len = int.from_bytes(packet[8:12], byteorder="big")

    # Adding sequence number and payload length for the acknowledgement sequence number
    ack_seq_num = seq_num + pay_len

    # save the address it has received it from
    address = client_data[1]
    ip = address[0]

    # Checking that the packet received is valid and that it is not corrupt
    # If is_corrupt is false then the packet is in its correct state

    if not is_corrupt(packet):
        print("[FESTIVAL REQUEST RECEIVED]: {}".format(ip))
        # Checking if the received festival is in the list
        festival_reply(packet[12:pay_len + 12].decode("ascii")[:pay_len])
        print("[SENDING ACKNOWLEDGEMENT PACKET] to: {}".format(ip))
        # Sending acknowledgement packet to the client
        serverSocket.sendto(create_packet(ack_seq_num, 1, ""), address)

    else:
        print("[PACKET IS CORRUPTED]")

    # Send greeting
    pay_len = int.from_bytes(packet[8:12], "big")
    # Changed to pay_len + 12
    greeting = festival_reply(packet[12:pay_len + 12].decode("ascii")[:pay_len])
    print("[SENDING GREETING]")

    serverSocket.sendto(create_packet(seq_num, 0, greeting), address)
