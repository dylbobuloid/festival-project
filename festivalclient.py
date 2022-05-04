# FestivalClient.py
import hashlib
import pickle
import socket
import time

# Create a UDP socket
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 12000

# create a socket with address and port
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.connect(("127.0.0.1", 13000))


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


def checksum(pkt):
    # Takes packet and passes into md5 to generate checkSum number
    h = hashlib.new('md5')
    h.update(pickle.dumps(pkt))

    return h.hexdigest()


def is_ack(packet):
    # Sequence number, Ack flag, payload length, payload, checkSum

    ack_flag = packet[4:8]

    if ack_flag == 1:
        return True
    else:
        return False


def is_corrupt(packet):
    # Storing all packet items in variables
    seq_num = packet[0:4]
    ack_flag = packet[4:8]
    pay_len = packet[8:12]
    payload = packet[12:32]

    # Store checkSum number from packet into variable
    check_sum = packet[32:].decode("ascii")

    # Recreating packet using: sequence number, Ack flag, payload length, payload without checkSum
    packet_to_check = seq_num + ack_flag + pay_len + payload

    # Passing packet into method to generate checkSum
    new_checksum = checksum(packet_to_check)

    # if checksum value is the same return false
    if check_sum == new_checksum:
        return False

    # if checksum value not the same return true
    elif check_sum != new_checksum:
        return True

    # sent the Message using the clientSock
    print('CLIENT RUNNING')

    # Sending a packet with the festival request to the server


try:
    clientSock.send(create_packet(0, 0, "Christmas"))
    print('FESTIVAL REQUEST SENT')

    # Starting the timer
    timeout = time.time() + 60
    print('waiting to receive acknowledgement')

    while True:

        if time.time() > timeout:
            print("it took too long to send the packet")
        else:
            # get the response & extract data
            ack_pkt = clientSock.recv(1024)

            if is_corrupt(ack_pkt):
                print("PACKET RECEIVED WAS CORRUPTED")
            elif is_ack(ack_pkt):
                print("PACKET RECEIVED WAS NOT AN ACKNOWLEDGEMENT")
            else:
                print("ACKNOWLEDGEMENT RECEIVED")

            greeting_pkt = clientSock.recv(1024)

            if is_corrupt(greeting_pkt):
                print("PACKET RECEIVED WAS CORRUPTED")
            else:
                pay_len = int.from_bytes(greeting_pkt[8:12], "big")
                payload = greeting_pkt[12:32].decode("ascii")[:pay_len]
                print("GREETING RECEIVED ({})".format(payload))

                # Send acknowledgement
                clientSock.send(create_packet(0, 1, " "))
                print("ACKNOWLEDGEMENT SENT")


except socket.timeout as inst:
    print('ERROR HAS OCCURRED "%s"' % inst)
    ## handle timeouts

# print('closing socket')
# clientSock.close()

##close the socket
