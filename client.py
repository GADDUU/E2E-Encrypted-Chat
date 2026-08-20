import socket

# Define the host and port for the client
HOST = 'localhost'
PORT = 1106

# Initialize the TCP Socket (IPv4, TCP stream)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server on localhost at port 1106
client_socket.connect((HOST, PORT))

# Prepare the data to send
data_to_send = "Hello Server, this is a message from client."

# Encode the data to bytes and send it to the server
client_socket.sendall(data_to_send.encode('utf-8'))
print(f"Message sent to the server successfully: {data_to_send}")

# Close the client socket
client_socket.close()