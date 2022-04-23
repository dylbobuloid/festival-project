from struct import *

#storing bytes as data

packed_data = pack("iif", 6, 19, 4.73)
#print("printing the data packed into a structure", packed_data)



# Each integer and float is 4 bytes each
#print(calcsize("i"))
#print(calcsize("i"))
#print(calcsize("iif"))

## converting byte data back into human readable form

#original_data = unpack("iif", packed_data)
#print("This is the original data back ", original_data)

#print("Original data back but using the bytes", unpack("iif", b'\x06\x00\x00\x00\x13\x00\x00\x00)\\\x97@'))

message = "hello"
# have to specify number of characters in the string
packet = pack("i i i 5s i", 1, 0, 5, b"dylan", 1111)
print(packet)
print(unpack("i i i 5s i", b'\x01\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00dylan\x00\x00\x00W\x04\x00\x00'))
#packed = b'\x01\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00h\x00\x00\x00W\x04\x00\x00'


#print(unpack("i i i 4s i", packed))

#packed = pack('i 4s f', 10, b'hello', 2500)
#print(packed)
#print(unpack('i 4s f',b'\n\x00\x00\x00hell\x00@\x1cE'))


#unpacked = unpack('i 4s f', packed)
#print(unpacked)



