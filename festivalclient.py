# FestivalClient.py
import hashlib
import pickle
import socket

# Create a UDP socket
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 12000
Message = b"Hello, Server"

# create a socket with address and port
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.connect(("127.0.0.1", 13000))

# Prints the message that is being sent
print('sending "%s"' % Message)


def create_packet():
    # Creating packet with the format
    seq_num = 0
    ack_flag = 0
    payload = b"Christmas"
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


def checksum(pkt):
    h = hashlib.new('md5')
    h.update(pickle.dumps(pkt))

    return h.hexdigest()


def is_ack():
    # 7 Checks the acknowledgement flag in the packet whether it is a 0 or 1
    # 8.1 if ACK flag 0 continue and make a packet makePacket()
    # 8.2 if ACK flag 1 go back and
    return 0


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
