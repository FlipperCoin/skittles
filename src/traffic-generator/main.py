import os
from time import sleep

import records_generator
import simple_tcp_server

# Config 

# Keys
SERVER_IP = "SERVER_IP"
SERVER_PORT = "SERVER_PORT"
SERVER_MAX_UNAUTHORIZED_CONNECTIONS = "SERVER_MAX_UNAUTHORIZED_CONNECTIONS"
RECORD_ENCODING = "RECORD_ENCODING"
MODE = "MODE" # options: SQN / MSG

# Defaults
SERVER_IP_DEFAULT = '0.0.0.0'
SERVER_PORT_DEFAULT = 30000
SERVER_MAX_UNAUTHORIZED_CONNECTIONS_DEFAULT = 10
RECORD_ENCODING_DEFAULT = 'ascii'
MODE_DEFAULT = 'SQN'


def client_worker(client, *args, **kwargs):
    mode = os.getenv(MODE, MODE_DEFAULT)
    # Send header
    client.send(bytes(records_generator.get_header(mode), os.getenv(RECORD_ENCODING, RECORD_ENCODING_DEFAULT)))
    while True:
        # Build random record
        record = records_generator.gen_record(mode)
        try:
            client.send(bytes(record, os.getenv(RECORD_ENCODING, RECORD_ENCODING_DEFAULT)))
        except ConnectionAbortedError:
            print("client disconnected")
            return
        
        # Take it easy
        sleep(0.2)

def main():
    max_unautherized_connections = int(os.getenv(SERVER_MAX_UNAUTHORIZED_CONNECTIONS, SERVER_MAX_UNAUTHORIZED_CONNECTIONS_DEFAULT))
    ip = os.getenv(SERVER_IP, SERVER_IP_DEFAULT)
    port = int(os.getenv(SERVER_PORT, SERVER_PORT_DEFAULT))

    simple_tcp_server.start_server(ip, port, client_worker, max_unautherized_connections)

if __name__ == "__main__":
    main()