import socket
import threading

def listener(server, client_worker, *args, **kwargs):
    while True:
        client = server.accept()
        print("client connected")
        client_worker_thread = threading.Thread(target=client_worker, args=(client))
        client_worker_thread.start()

def start_server(ip, port, client_worker, max_unautherized_connections):
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    server.bind((ip, port))
    server.listen(max_unautherized_connections)

    listener_thread = threading.Thread(target=listener, args=(server, client_worker))
    listener_thread.start()
