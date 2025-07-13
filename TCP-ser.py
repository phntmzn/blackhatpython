# Import socket module for network communication
import socket
# Import threading module to handle multiple connections concurrently
import threading

# IP address to bind the server to (listen on all interfaces)
IP = '0.0.0.0'
# List of ports on which the server will listen
PORTS = [80, 443]


# Function to start a server socket on a given port
# It listens for incoming connections and starts a new thread for each client
def start_server(port):
    # Create a TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the specified IP and port
    server.bind((IP, port))
    # Start listening for incoming connections, with a backlog of 5
    server.listen(5)
    print(f"[*] Listening on {IP}:{port}")

    while True:
        # Accept a new client connection
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]} on port {port}")
        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Main function to start server threads on all specified ports
def main():
    # Iterate over each port and start a server thread
    for port in PORTS:
        thread = threading.Thread(target=start_server, args=(port,))
        thread.start()

# Function to handle communication with a connected client
# It receives data from the client, prints it, and sends an acknowledgment
def handle_client(client_socket):
    # Example: receive data and close connection
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACK')

if __name__ == '__main__':
    main()
