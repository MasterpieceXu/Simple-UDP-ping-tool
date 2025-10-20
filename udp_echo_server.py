import argparse
from socket import *

def start_server(host, port):
    # AF_INET: IPv4; SOCK_DGRAM: UDP
    server_socket = socket(AF_INET, SOCK_DGRAM)
    
    # Bind the socket to the address and port
    # '0.0.0.0' means listen on all available interfaces
    try:
        server_socket.bind((host, port))
        print(f'Server started, listening on {host}:{port}...')
    except OSError as e:
        print(f'Bind failed: {e}. (Port {port} might be in use)')
        return

    while True:
        try:
            # 2048 is the buffer size
            message, client_address = server_socket.recvfrom(2048)
            
            # Print the received message and client address
            print(f'Received message from {client_address}: {message.decode("utf-8")}')
            
            # Echo the received message back to the client
            server_socket.sendto(message, client_address)
            
        except KeyboardInterrupt:
            print('\nServer is shutting down...')
            break
        except Exception as e:
            print(f'An error occurred: {e}')
            
    server_socket.close()
    print('Server closed.')

def main():
    parser = argparse.ArgumentParser(description='A simple UDP Echo server')
    
    parser.add_argument('--host', type=str, default='0.0.0.0',
                        help="Host address to listen on (default: '0.0.0.0', listens on all interfaces)")
    parser.add_argument('--port', type=int, default=12000,
                        help='Port number to listen on (default: 12000)')
    
    args = parser.parse_args()
    
    start_server(args.host, args.port)

if __name__ == '__main__':
    main()