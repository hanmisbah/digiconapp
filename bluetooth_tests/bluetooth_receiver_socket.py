import socket
import os

# 🔹 Bluetooth server setup
server_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
port = 3  # Ensure the port matches the sender
server_sock.bind(("", port))
server_sock.listen(1)

print("📡 Bluetooth Server Started... Waiting for connection")

try:
    client_sock, client_info = server_sock.accept()
    print(f"✅ Connection established with {client_info}")

    # 🔹 Save the received file
    received_file = "received_file.txt"
    with open(received_file, "wb") as f:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            f.write(data)

    print(f"📥 File received and saved as {received_file}")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    client_sock.close()
    server_sock.close()
