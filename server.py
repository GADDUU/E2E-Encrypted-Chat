import socket
import threading

# Define the host and port for the server
HOST = 'localhost'
PORT = 1106

# List to keep track of all connected clients
clients = []

# Function to broadcast messages to all connected clients
def broadcast_message(message, sender_conn):
    for client in clients:
        # Check condition to avoid sending the message back to the sender
        if client != sender_conn:
            try:
                # Send the message to the client
                client.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message to client: {e}")
                clients.remove(client) # Remove the client from the list if sending fails

# Function to handle each client connection independently
def handle_client(client_conn, client_address):
    print(f"New connection thread started for client: {client_address}")

    # Keep the connection open to receive data from the client 
    while True:
        try:
            # Receive data from the client
            data = client_conn.recv(1010)

            # If no data is received, the client has disconnected
            if not data:
                print(f"Client at address {client_address} has disconnected")
                break

            # Decode and print the received data from bytes to string
            decoded_data = data.decode('utf-8')
            print(f"Received data from {client_address}: {decoded_data}")

            # Format the message to show who sent it
            message_to_send = f"Message from {client_address}: {decoded_data}"

            # Call the broadcast function to send the message
            broadcast_message(message_to_send, client_conn)

        except Exception as e:
            # Break the loop if an error occurs
            print(f"Error receiving data from client {client_address}: {e}")
            break

    # Close the client socket connection
    client_conn.close()
    print(f"Connection with {client_address} closed")

# Initialize the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"Server is listening on port {PORT}")

# Main loop to accept incoming client connections
while True:
    # Accept a new client connection
    client_conn, client_address = server_socket.accept()

    # Add the new client connection to the list of clients
    clients.append(client_conn)
    print(f"Accepted new connection from {client_address}")

    # Create a new thread to handle the client connection
    client_thread = threading.Thread(target = handle_client, args = (client_conn, client_address))

    # Start the client handling thread
    client_thread.start()

    # Print the number of active threads (including the main thread)
    print(f"Active threads: {threading.active_count()}")
    
# Close the server socket 
server_socket.close()