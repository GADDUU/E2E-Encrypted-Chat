import socket
import sys
import threading

HOST = 'localhost'
PORT = 1106

# Function to continuously receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1010)
            if not data:
                print("\nServer has closed the connection")
                break
            decoded_data = data.decode('utf-8')
            print(f"\nReceived from server: {decoded_data}")
        except Exception as e:
            print(f"\nError receiving data from server: {e}")
            break

# Initialize the TCP Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"\nConnected to the server at {HOST}:{PORT}")

# ========================================
# AUTH MENU
# ========================================
print("\n--- WELCOME TO E2E CHAT ---")
print("1. Register")
print("2. Login")

choice = input("Enter your choice (1 or 2): ")

if choice == '1':
    username = input("Enter a new username: ")
    password = input("Enter a new password: ")

    auth_message = f"REGISTER|{username}|{password}"
    client_socket.sendall(auth_message.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(f"Server response: {response}")

    client_socket.close()
    sys.exit()

elif choice == '2':
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    auth_message = f"LOGIN|{username}|{password}"
    client_socket.sendall(auth_message.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')

    parts = response.split('|')

    if parts[0] == "SUCCESS":
        session_id = parts[1]
        welcome_message = parts[2]

        print(f"Login successful! {welcome_message}")
        print(f"[-] Session ID securely stored: {session_id}")

else:
    print("Invalid choice. Existing the client")
    client_socket.close()
    sys.exit()
# ========================================



# Start a separate thread to handle receiving messages from the server
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# Keep the connection open to send data to the server
while True:
    data_to_send = input("")

    if data_to_send.lower() == 'exit':
        print("Exiting the client")
        break

    client_socket.sendall(data_to_send.encode('utf-8'))
    print(f"Message sent to the server successfully: {data_to_send}")

# Close the client socket
client_socket.close()