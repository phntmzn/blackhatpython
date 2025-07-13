import sys
import socket
import threading

def hexdump(src, length=16):
        result = []
        digits = 2

        if isinstance(src, bytes):
                src = src
        else:
                src = src.encode()

        for i in range(0, len(src), length):
                s = src[i:i+length]
                hexa = ' '.join(["%0*X" % (digits, b) for b in s])
                text = ''.join([chr(b) if 0x20 <= b < 0x7F else '.' for b in s])
                result.append("%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text))

        print('\n'.join(result))

def receive_from(connection):
        buffer = b""
        connection.settimeout(2)
        try:
                while True:
                        data = connection.recv(4096)
                        if not data:
                                break
                        buffer += data
        except Exception:
                pass
        return buffer

def request_handler(buffer):
        # perform packet modifications
        return buffer

def response_handler(buffer):
        # perform packet modifications
        return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))

        if receive_first:
                remote_buffer = receive_from(remote_socket)
                hexdump(remote_buffer)
                remote_buffer = response_handler(remote_buffer)
                if len(remote_buffer):
                        print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
                        client_socket.sendall(remote_buffer)

        while True:
                local_buffer = receive_from(client_socket)
                if len(local_buffer):
                        print("[==>] Received %d bytes from localhost." % len(local_buffer))
                        hexdump(local_buffer)
                        local_buffer = request_handler(local_buffer)
                        remote_socket.sendall(local_buffer)
                        print("[==>] Sent to remote.")

                remote_buffer = receive_from(remote_socket)
                if len(remote_buffer):
                        print("[<==] Received %d bytes from remote." % len(remote_buffer))
                        hexdump(remote_buffer)
                        remote_buffer = response_handler(remote_buffer)
                        client_socket.sendall(remote_buffer)
                        print("[<==] Sent to localhost.")

                if not len(local_buffer) and not len(remote_buffer):
                        client_socket.close()
                        remote_socket.close()
                        print("[*] No more data. Closing connections.")
                        break

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
                server.bind((local_host, local_port))
        except Exception:
                print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
                print("[!!] Check for other listening sockets or correct permissions.")
                sys.exit(0)

        print("[*] Listening on %s:%d" % (local_host, local_port))
        server.listen(5)

        while True:
                client_socket, addr = server.accept()
                print("[==>] Received incoming connection from %s:%d" % (addr[0], addr[1]))
                proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
                proxy_thread.start()

def main():
        if len(sys.argv[1:]) != 5:
                print("Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
                print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
                sys.exit(0)

        local_host = sys.argv[1]
        local_port = int(sys.argv[2])
        remote_host = sys.argv[3]
        remote_port = int(sys.argv[4])
        receive_first = sys.argv[5].lower() == "true"

        server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == "__main__":
        main()
