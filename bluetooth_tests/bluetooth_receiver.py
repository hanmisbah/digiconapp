import bluetooth

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1  # Common port for Bluetooth RFCOMM file transfer
server_sock.bind(("", port))
server_sock.listen(1)

print("📡 Bluetooth Server Started... Waiting for connection")

client_sock, client_info = server_sock.accept()
print(f"✅ Connection accepted from {client_info}")

# Receive file data and write to file
file_name = "received_file.jpg"
with open(file_name, "wb") as f:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        f.write(data)

print(f"📩 File received and saved as {file_name}")
client_sock.close()
server_sock.close()
