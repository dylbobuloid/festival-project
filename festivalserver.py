import hashlib
import pickle
from struct import *
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('127.0.0.1', 13000))
print("SERVER RUNNING")


# Hardcode all ips that will be used


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

    # seq_num = int.from_bytes(packet[0:4], "big")
    seq_num = packet[0:4]
    ack_flag = packet[4:8]
    pay_len = packet[8:12]
    payload = packet[12:32]

    check_sum = packet[32:].decode("ascii")
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

    return h.hexdigest()


def create_packet(seq, ack, pay_load):
    # Creating packet with the format
    # Creating acknowledgement packet

    seq_num = seq
    ack_flag = ack
    payload = pay_load
    pay_len = len(payload.encode("ascii"))

    # Need to pad the payload with extra characters since it is not at the maximum number of bytes
    # Padding payload with " " character
    if len(payload) < 20:
        temp = len(payload)
        for i in range(temp, 20, 1):
            payload = payload + " "

    payload = payload.encode("ascii")

    # Converting each number to 4 bytes as specified in RFC format
    seq_num = seq_num.to_bytes(4, byteorder="big")
    ack_flag = ack_flag.to_bytes(4, byteorder="big")
    pay_len = pay_len.to_bytes(4, byteorder="big")

    # Sequence number, Ack flag, payload length, payload, checkSum

    pkt_no_checksum = seq_num + ack_flag + pay_len + payload
    checksum_num = checksum(pkt_no_checksum)

    checksum_num = checksum_num.encode('ascii')

    # Concatenate all together to create packet
    pkt = seq_num + ack_flag + pay_len + payload + checksum_num

    return pkt


def is_ack(packet):
    # Sequence number, Ack flag, payload length, payload, checkSum

    ack_flag = packet[4:8]

    if ack_flag == 1:
        return True
    else:
        return False


def seq_mismatch(packet):
    # Sequence number, Ack flag, payload length, payload, checkSum

    ack_flag = packet[:4]

    if ack_flag == 0:
        return True
    else:
        return False


while True:
    # Receiving packet from the client
    client_data = serverSocket.recvfrom(1024)

    # Data client has sends both the packet and the address it has received it from
    # packet from client
    packet = client_data[0]

    # save the address it has received it from
    address = client_data[1]

    # Checking that the packet received is valid and that it is not corrupt
    # If is_corrupt is false then the packet is in its correct state

    if not is_corrupt(packet):
        print("[FESTIVAL REQUEST RECEIVED]")
        print("[SENDING ACKNOWLEDGEMENT PACKET]")
        # Sending acknowledgement packet to the client
        serverSocket.sendto(create_packet(0, 1, " "), address)

    else:
        print("[CORRUPTED]")

    # Send greeting
    pay_len = int.from_bytes(packet[8:12], "big")
    payload = "Merry " + packet[12:32].decode("ascii")[:pay_len]
    print("[SENDING GREETING]")
    serverSocket.sendto(create_packet(0, 0, payload), address)

    client_ack = serverSocket.recvfrom(1024)[0]

    if is_corrupt(client_ack):
        print("[PACKET RECEIVED WAS CORRUPTED]")
    elif is_ack(client_ack):
        print("[PACKET RECEIVED WAS NOT AN ACKNOWLEDGEMENT]")
    else:
        print("[ACKNOWLEDGEMENT RECEIVED]")



