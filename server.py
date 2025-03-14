import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 5001))  # Listen on all interfaces
server_socket.listen(5)

while True:
    conn, addr = server_socket.accept()
    data = conn.recv(1024)
    print(f"Received: {data.decode()} from {addr}")
    conn.close()