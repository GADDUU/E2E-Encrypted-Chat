import socket

# Define the host and port for the client
HOST = 'localhost'
PORT = 1106

# Initialize the TCP Socket (IPv4, TCP stream)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))
print(f"Connected to the server at {HOST}:{PORT}")

# Keep the connection open to send data to the server
while True:
    # Get user input to send to the server
    data_to_send = input("Enter data to send to the server (or type 'exit' to quit): ")

    # Check if the user wants to exit
    if data_to_send.lower() == 'exit':
        print("Exiting the client")
        break

    #Encode and send the data to the server
    client_socket.sendall(data_to_send.encode('utf-8'))
    print(f"Message sent to the server successfully: {data_to_send}")

# Close the client socket
client_socket.close()