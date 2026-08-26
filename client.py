import socket
import sys
import threading
from Crypto.PublicKey import RSA

HOST = 'localhost'
PORT = 1106

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                print("\n[!] Connection closed by server.")
                break
            decoded_data = data.decode('utf-8')
            print(f"\n{decoded_data}")
        except Exception as e:
            print(f"\n[!] Error receiving data: {e}")
            break

def generate_rsa_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"[-] Connected to server at {HOST}:{PORT}")

print("\n--- WELCOME TO E2E CHAT ---")
print("1. Register")
print("2. Login")
choice = input("[-] Enter your choice (1 or 2): ")

if choice == '1':
    username = input("[-] Enter a new username: ")
    password = input("[-] Enter a new password: ")
    auth_message = f"REGISTER|{username}|{password}"
    client_socket.sendall(auth_message.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print(f"[-] Server: {response}")
    client_socket.close()
    sys.exit()

elif choice == '2':
    username = input("[-] Enter your username: ")
    password = input("[-] Enter your password: ")
    auth_message = f"LOGIN|{username}|{password}"
    client_socket.sendall(auth_message.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    parts = response.split('|')

    if parts[0] == "SUCCESS":
        session_id = parts[1]
        print(f"[+] Login successful: {parts[2]}")
        print(f"[-] Session ID stored: {session_id}")
        
        print("[-] Initializing RSA key pair...")
        my_private_key, my_public_key = generate_rsa_key_pair()
        
        print("[-] Uploading public key to server...")
        upload_key_message = f"UPLOAD_PUBLIC_KEY|{my_public_key.decode('utf-8')}"
        client_socket.sendall(upload_key_message.encode('utf-8'))
    else:
        print(f"[!] Server: {response}")
        client_socket.close()
        sys.exit()
else:
    print("[!] Invalid choice.")
    client_socket.close()
    sys.exit()

print("\n--- ENTERING SECURE CHAT ---")
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

target_username = input("\n[-] Enter the username you want to chat with: ")
key_request_message = f"REQUEST_PUBLIC_KEY|{target_username}"
client_socket.sendall(key_request_message.encode('utf-8'))
print(f"[-] Public key request sent for user: {target_username}")

while True:
    data_to_send = input("")
    if data_to_send.lower() == 'exit':
        print("[-] Exiting...")
        break
    client_socket.sendall(data_to_send.encode('utf-8'))
    print(f"[+] Message sent: {data_to_send}")

client_socket.close()