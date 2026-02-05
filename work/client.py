import socket
import threading

def receive_messages(client_socket):
    """Continuously listen for messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(f"\n{message}\n> ", end="")
        except:
            print("Disconnected from server.")
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    username = input("Enter your username to join the group: ")
    client.send(username.encode('utf-8'))

    # Start thread to receive messages in background
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    print("--- Commands ---")
    print("Type message to send to group.")
    print("Type '/msg <username> <message>' for private chat.")
    print("----------------")

    while True:
        msg = input("> ")
        if msg.lower() == 'exit':
            break
        client.send(msg.encode('utf-8'))

if __name__ == "__main__":
    start_client()