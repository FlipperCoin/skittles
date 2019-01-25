import os
import threading
import socket
import queue
from time import sleep

import simple_tcp_server

# Config 

# Keys
SERVER_IP = "SERVER_IP"
SERVER_PORT = "SERVER_PORT"
SERVER_MAX_UNAUTHORIZED_CONNECTIONS = "SERVER_MAX_UNAUTHORIZED_CONNECTIONS"
RECORD_ENCODING = "RECORD_ENCODING"
SOURCE_HOST = "SOURCE_HOST"
SOURCE_PORT = "SOURCE_PORT"
SOURCE_RECONNECT_INTERVAL = "SOURCE_RECONNECT_INTERVAL"
SOURCE_HOST_MAX_CONNECTION_ATTEMPTS = "SOURCE_HOST_MAX_CONNECTION_ATTEMPTS"

# Defaults
SERVER_IP_DEFAULT = '0.0.0.0'
SERVER_PORT_DEFAULT = '32000'
SERVER_MAX_UNAUTHORIZED_CONNECTIONS_DEFAULT = '10'
RECORD_ENCODING_DEFAULT = 'ascii'
SOURCE_HOST_DEFAULT = 'traffic-generator'
SOURCE_PORT_DEFAULT = '30000'
SOURCE_RECONNECT_INTERVAL_DEFAULT = "2"
SOURCE_HOST_MAX_CONNECTION_ATTEMPS_DEFAULT = "10"


clients = queue.Queue(0) 
header = None
header_lock = threading.Lock()
header_queue = queue.Queue(0)
lines = queue.Queue(0)

def client_worker(client, *args, **kwargs):
    is_initialized = False
    clients.put((client, is_initialized))

def loadbalancer_worker():
    global header
    while True:
        client, is_initialized = clients.get(block=True)
        if not is_initialized:
            if header is None:
                header_lock.acquire()
                if header is None:
                    header = header_queue.get(block=True)
                header_lock.release()
            client.send(bytes(header, os.getenv(RECORD_ENCODING, RECORD_ENCODING_DEFAULT)))
            is_initialized = True

        line = lines.get(block=True)
        try:
            client.send(bytes(line, os.getenv(RECORD_ENCODING, RECORD_ENCODING_DEFAULT)))
        except Exception:
            print("Trying to send data to a client raised an exception, removing client...")
            continue

        clients.put((client, is_initialized))

def source_worker(source_client, *args, **kwargs):
    global header
    leftovers = bytes()
    while True:
        try:
            # if using encodings other than ascii / other 1 byte encodings, 
            # there's probably a bug here if cutting in the middle of a symbol
            recv_data = source_client.recv(4096)
        except Exception:
            print("Server diconnected, reconnecting...")
            connect_to_source()
            return

        corrected_data = leftovers + recv_data
        data_str = str(corrected_data, os.getenv(RECORD_ENCODING, RECORD_ENCODING_DEFAULT))

        split_records = data_str.split('\n')
        for i, record in enumerate(split_records):
            # if last splitted item
            if i == (len(split_records) -1):
                if len(record) != 0:
                    leftovers = record
                else:
                    break
            if header is None:
                header = record + '\n'
                header_queue.put(header)
            else:
                lines.put(record + '\n')

def connect_to_source():
    host = os.getenv(SOURCE_HOST, SOURCE_HOST_DEFAULT)
    port = int(os.getenv(SOURCE_PORT, SOURCE_PORT_DEFAULT))

    source_client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    attempts_left = int(os.getenv(SOURCE_HOST_MAX_CONNECTION_ATTEMPTS, SOURCE_HOST_MAX_CONNECTION_ATTEMPS_DEFAULT))
    while attempts_left > 0:
        try:
            source_client.connect((host, port))
            break
        except Exception as e:
            print("Failed to connect to source host %s:%d, expection : %s" % (host, port, str(e)))
            sleep(int(os.getenv(SOURCE_RECONNECT_INTERVAL, SOURCE_RECONNECT_INTERVAL_DEFAULT)))
            attempts_left -= 1
    
    if attempts_left == 0:
        print("Max connection attempts to source exceeded, exiting...")
        exit(1)

    source_thread = threading.Thread(target=source_worker, args=(source_client,))
    source_thread.start()

def main():
    # Start loadbalancer worker
    loadbalancer_thread = threading.Thread(target=loadbalancer_worker)
    loadbalancer_thread.start()

    # Start server
    max_unautherized_connections = int(os.getenv(SERVER_MAX_UNAUTHORIZED_CONNECTIONS, SERVER_MAX_UNAUTHORIZED_CONNECTIONS_DEFAULT))
    ip = os.getenv(SERVER_IP, SERVER_IP_DEFAULT)
    port = int(os.getenv(SERVER_PORT, SERVER_PORT_DEFAULT))

    simple_tcp_server.start_server(ip, port, client_worker, max_unautherized_connections) 

    # Connect to source
    connect_to_source()

if __name__ == "__main__":
    main()