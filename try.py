import socket

server_address = ('', 55000)
message = b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01'  # DNS query for example.com

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message, server_address)
response, server = sock.recvfrom(512)
sock.close()

print("Received response:", response)