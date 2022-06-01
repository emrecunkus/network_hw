import socket
import threading
import time


# --- functions ---

def handle_client(conn, addr):
    print("[thread] starting")

    # recv message
    message = conn.recv(1024)

    filename = message.split()[1]

    f = open(filename[1:])

    outputdata = f.read()
    # Fill in start #Fill in end
    print(outputdata)
    # Send one HTTP header line into socket
    # Fill in start#
    conn.send('\nHTTP/1.1 200 OK\n\n'.encode())
    # Fill in end

    # Send the content of the requested file to the connection socket
    for i in range(0, len(outputdata)):
        conn.send(outputdata[i].encode())
    conn.send("\r\n".encode())

   # message = message.decode()
    print("[thread] client:", addr, 'recv:', message)

    # simulate longer work
    time.sleep(5)

    # send answer
    message = "Bye!"
    message = message.encode()
    conn.send(message)
    print("[thread] client:", addr, 'send:', message)

    conn.close()

    print("[thread] ending")


# --- main ---

host = '127.0.0.1'
port = 8080

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
             1)  # solution for "[Error 89] Address already in use". Use before bind()
s.bind((host, port))
s.listen(1)

all_threads = []

try:
    while True:
        print("Waiting for client")
        conn, addr = s.accept()

        print("Client:", addr)

        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()

        all_threads.append(t)
except KeyboardInterrupt:
    print("Stopped by Ctrl+C")
finally:
    if s:
        s.close()
    for t in all_threads:
        t.join()
