import socket

# --- main ---

host = '127.0.0.1'
port = 8080

s = socket.socket()
s.connect((host, port))

print("Connected to the server")

message = "Hello"
print('send:', message)
message = message.encode()
s.send(message)

message = s.recv(1024)
message = message.decode()
print('recv:', message)