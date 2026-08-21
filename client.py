import socket
import threading

# Define the host and port for the client
HOST = 'localhost'
PORT = 1106

# Function to continuously receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            # Receive data from the server
            data = client_socket.recv(1010)
            if not data:
                print("Server has closed the connection")
                break
            # Decode and print the received data from bytes to string
            decoded_data = data.decode('utf-8')
            print(f"Received from server: {decoded_data}")
        except Exception as e:
            print(f"Error receiving data from server: {e}")
            break

# Initialize the TCP Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"Connected to the server at {HOST}:{PORT}")

# Start a separate thread to handle receiving messages from the server
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# Keep the connection open to send data to the server
while True:
    # Get user input to send to the server
    data_to_send = input("")

    # Check if the user wants to exit
    if data_to_send.lower() == 'exit':
        print("Exiting the client")
        break

    #Encode and send the data to the server
    client_socket.sendall(data_to_send.encode('utf-8'))
    print(f"Message sent to the server successfully: {data_to_send}")

# Close the client socket
client_socket.close()