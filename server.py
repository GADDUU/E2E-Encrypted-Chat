import socket

# Define the host and port for the server
HOST = 'localhost'
PORT = 1106

# Initialize a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Start listening for incoming connections
server_socket.listen()
print(f"Server is listening on port {PORT}")

# Accept a new connection
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

# Receive data from the client
data = client_socket.recv(1010)

#Decode the received data from bytes to string
decoded_data = data.decode('utf-8')
print(f"Received data: {decoded_data}")

# Close the client socket
client_socket.close()
# Close the server socket
server_socket.close()