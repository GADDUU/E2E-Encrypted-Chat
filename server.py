import socket
import threading
import bcrypt
import database

HOST = 'localhost'
PORT = 1106

# List to keep track of all connected clients
clients = []

# Function to broadcast messages to all connected clients
def broadcast_message(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message to client: {e}")
                clients.remove(client) # Remove the client from the list if sending fails

# Function to handle each client connection independently
def handle_client(client_conn, client_address):
    print(f"New connection thread started for client: {client_address}")

    while True:
        try:
            data = client_conn.recv(1010)

            if not data:
                print(f"Client at address {client_address} has disconnected")
                break

            decoded_data = data.decode('utf-8')

            parts = decoded_data.split('|')

            # Handle registration and login requests
            if parts[0] == "REGISTER":
                username = parts[1]
                password = parts[2]

                password_bytes = password.encode('utf-8')
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password_bytes, salt)

                success = database.add_user(username, hashed_password)

                if success:
                    response = "Registration successful"
                    print(f"User {username} registered successfully")
                else:
                    response = "Registration failed: Username already exists"
                    print(f"Registration failed for user {username}: Username already exists")

                client_conn.sendall(response.encode('utf-8'))

                continue  # Skip broadcasting the registration message to other clients

            elif parts[0] == "LOGIN":
                username = parts[1]
                password = parts[2]

                stored_hashed_password = database.get_user_password(username)
                if stored_hashed_password is None:
                    response = "Login failed: User does not exist"
                    print(f"Login failed for user {username}: User does not exist")
                else:
                    password_bytes = password.encode('utf-8')
                    if bcrypt.checkpw(password_bytes, stored_hashed_password):
                        response = "Login successful"
                        print(f"User {username} logged in successfully")
                    else:
                        response = "Login failed: Incorrect password"
                        print(f"Login failed for user {username}: Incorrect password")

                client_conn.sendall(response.encode('utf-8'))

                continue  # Skip broadcasting the login message to other clients


            message_to_send = f"Message from {client_address}: {decoded_data}"

            broadcast_message(message_to_send, client_conn)

        except Exception as e:
            print(f"Error receiving data from client {client_address}: {e}")
            break

    client_conn.close()
    print(f"Connection with {client_address} closed")

# Initialize the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"Server is listening on port {PORT}")

# Main loop to accept incoming client connections
while True:
    client_conn, client_address = server_socket.accept()

    clients.append(client_conn)
    print(f"Accepted new connection from {client_address}")

    client_thread = threading.Thread(target = handle_client, args = (client_conn, client_address))

    client_thread.start()

    print(f"Active threads: {threading.active_count()}")
    
server_socket.close()