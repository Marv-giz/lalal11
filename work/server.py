import socket
import threading

# Server Configuration
HOST = '127.0.0.1'
PORT = 5555

# Active membership management 
clients = {} # {username: socket_connection}

def broadcast(message, sender_socket):
    """Sends a message to all online group members (Multicast) """
    for client_socket in clients.values():
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except:
                continue

def handle_client(client_socket, addr):
    try:
        # Initial Join: Register username [cite: 19]
        username = client_socket.recv(1024).decode('utf-8')
        clients[username] = client_socket
        print(f"[JOIN] {username} connected from {addr}")
        broadcast(f"{username} has joined the group.".encode('utf-8'), client_socket)

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message: break

            # Check for Private Message (Unicast) [cite: 25]
            # Format: /msg username message
            if message.startswith("/msg"):
                parts = message.split(" ", 2)
                if len(parts) >= 3:
                    target, private_msg = parts[1], parts[2]
                    if target in clients:
                        clients[target].send(f"[PRIVATE from {username}]: {private_msg}".encode('utf-8'))
                    else:
                        client_socket.send(f"User {target} not found.".encode('utf-8'))
            else:
                # Group Message [cite: 23]
                broadcast(f"{username}: {message}".encode('utf-8'), client_socket)

    except:
        pass
    finally:
        # Detect when a member leaves [cite: 32]
        if username in clients:
            del clients[username]
            broadcast(f"{username} has left the group.".encode('utf-8'), client_socket)
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server is running on {HOST}:{PORT}...")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()