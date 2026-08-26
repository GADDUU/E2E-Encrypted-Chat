import socket
import threading
import bcrypt
import database
import secrets

HOST = 'localhost'
PORT = 1106

clients = []
active_sessions = {}
public_keys = {} 

def broadcast_message(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"[!] Error broadcasting to a client: {e}")
                clients.remove(client)

def handle_client(client_conn, client_address):
    print(f"[-] New connection from {client_address}")
    current_username = None

    while True:
        try:
            data = client_conn.recv(4096)
            if not data:
                print(f"[-] Client {client_address} disconnected.")
                break

            decoded_data = data.decode('utf-8')
            parts = decoded_data.split('|')

            if parts[0] == "REGISTER":
                username = parts[1]
                password = parts[2]
                password_bytes = password.encode('utf-8')
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password_bytes, salt)

                if database.add_user(username, hashed_password):
                    response = "Registration successful"
                    print(f"[+] Registered user: {username}")
                else:
                    response = "Registration failed: Username already exists"
                    print(f"[!] Registration failed (duplicate): {username}")
                
                client_conn.sendall(response.encode('utf-8'))
                continue

            elif parts[0] == "LOGIN":
                username = parts[1]
                password = parts[2]
                stored_hashed_password = database.get_user_password(username)
                
                if stored_hashed_password:
                    if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
                        current_username = username
                        session_id = secrets.token_hex(16)
                        active_sessions[session_id] = current_username
                        response = f"SUCCESS|{session_id}|Welcome {username}!"
                        print(f"[+] User logged in: {username}")
                    else:
                        response = "Login failed: Incorrect password"
                        print(f"[!] Login failed (wrong password): {username}")
                else:
                    response = "Login failed: User does not exist"
                    print(f"[!] Login failed (not found): {username}")

                client_conn.sendall(response.encode('utf-8'))
                continue

            elif parts[0] == "UPLOAD_PUBLIC_KEY":
                if current_username:
                    public_keys[current_username] = parts[1]
                    print(f"[+] Uploaded public key for: {current_username}")
                else:
                    print(f"[!] Unauthorized key upload attempt from {client_address}")
                continue

            elif parts[0] == "REQUEST_PUBLIC_KEY":
                target_username = parts[1]
                if target_username in public_keys:
                    requested_key = public_keys[target_username]
                    response = f"PUBLIC_KEY_RESPONSE|{target_username}|{requested_key}"
                    client_conn.sendall(response.encode('utf-8'))
                    print(f"[-] Sent {target_username}'s public key to {current_username}")
                else:
                    error_message = f"ERROR|Public key for {target_username} not found"
                    client_conn.sendall(error_message.encode('utf-8'))
                    print(f"[!] Failed key request for {target_username} from {current_username}")
                continue

            message_to_send = f"[{current_username or client_address[1]}]: {decoded_data}"
            broadcast_message(message_to_send, client_conn)

        except Exception as e:
            print(f"[!] Error with client {client_address}: {e}")
            break

    if client_conn in clients:
        clients.remove(client_conn)
    client_conn.close()
    print(f"[-] Connection closed for {client_address}")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"[-] Listening on port {PORT}")

while True:
    client_conn, client_address = server_socket.accept()
    clients.append(client_conn)
    client_thread = threading.Thread(target=handle_client, args=(client_conn, client_address))
    client_thread.start()
    print(f"[-] Active connections: {threading.active_count() - 1}")