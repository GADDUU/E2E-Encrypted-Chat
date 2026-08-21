import socket
import threading

# Define the host and port for the server
HOST = 'localhost'
PORT = 1106

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

        except Exception as e:
            # Break the loop if an error occurs
            print(f"Error receiving data from client {client_address}: {e}")
            break

    # Close the client socket connection
    client_conn.close()
    print(f"Connection with {client_address} closed")

# Initialize a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Start listening for incoming connections
server_socket.listen()
print(f"Server is listening on port {PORT}")

# Main loop to accept incoming client connections
while True:
    # Accept a new client connection
    client_conn, client_address = server_socket.accept()
    print(f"Accepted new connection from {client_address}")

    # Create a new thread to handle the client connection
    client_thread = threading.Thread(target = handle_client, args = (client_conn, client_address))

    # Start the client handling thread
    client_thread.start()

    # Print the number of active threads (including the main thread)
    print(f"Active threads: {threading.active_count()}")
    
# Close the server socket 
server_socket.close()