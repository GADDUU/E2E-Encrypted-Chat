import sqlite3

# Function to initialize the database and create the necessary tables
def initialize_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('my_database.db')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Create a table named 'users' if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("[DATABASE] Database initialized and 'users' table created successfully")

# Function to add a new user to the database
def add_user(username, password):
    # Connect to the SQLite database
    conn = sqlite3.connect('my_database.db')
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Insert the new user into the 'users' table
    try:
        # Use '?' placeholders to prevent SQL injection
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        # Commit the changes
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Handle the case where the username already exists
        return False
    finally:
        # Close the connection
        conn.close()

# Function to retrieve a user's password from the database
def get_user_password(username):
    # Connect to the SQLite database
    conn = sqlite3.connect('my_database.db')
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Retrieve the password for the given username
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone() # Fetch the first row of the result
    conn.close() 

    # Return the password if the user exists, otherwise return None
    return result[0] if result else None

if __name__ == "__main__":
    initialize_database()

    # # --- TEST SCRIPT ---
# if __name__ == '__main__':
#     # 1. Khởi tạo CSDL
#     initialize_database()
    
#     print("\n--- KỊCH BẢN 1: THÊM NGƯỜI DÚNG MỚI ---")
#     # Thử thêm một user tên là 'alice' với mật khẩu giả 'mat_khau_123'
#     thanh_cong = add_user('alice', 'mat_khau_123')
#     if thanh_cong:
#         print("[-] Đăng ký thành công tài khoản 'alice'!")
#     else:
#         print("[!] Lỗi: Tài khoản 'alice' đã tồn tại!")
        
#     print("\n--- KỊCH BẢN 2: THỬ ĐĂNG KÝ TRÙNG TÊN ---")
#     # Thử thêm 'alice' một lần nữa
#     thanh_cong_lan_2 = add_user('alice', 'mat_khau_khac_456')
#     if not thanh_cong_lan_2:
#         print("[-] Chính xác! Hệ thống đã tự động chặn đăng ký trùng tên 'alice'.")
        
#     print("\n--- KỊCH BẢN 3: LẤY THÔNG TIN ĐĂNG NHẬP ---")
#     # Thử lấy mật khẩu của 'alice'
#     mat_khau_truy_xuat = get_user_password('alice')
#     print(f"[-] Mật khẩu của alice trong CSDL là: {mat_khau_truy_xuat}")
    
#     # Thử lấy mật khẩu của một người không tồn tại
#     mat_khau_nguoi_la = get_user_password('bob_la_ai_do')
#     if mat_khau_nguoi_la is None:
#         print("[-] Chính xác! Hệ thống báo None vì không tìm thấy user 'bob_la_ai_do'.")