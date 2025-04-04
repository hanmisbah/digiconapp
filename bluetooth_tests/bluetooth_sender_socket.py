import socket
import bluetooth  # Make sure you have PyBluez installed
import os

# 🔍 Step 1: Scan for Bluetooth devices
print("🔍 Scanning for Bluetooth devices...")
nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True)

if not nearby_devices:
    print("❌ No Bluetooth devices found. Make sure the receiver is discoverable.")
    exit()

# 🔹 Show the available devices
print("✅ Found devices:")
for i, (addr, name) in enumerate(nearby_devices):
    print(f"{i + 1}. {name} ({addr})")

# 🔹 Step 2: Let user select a device
choice = int(input("Select a device number: ")) - 1
TARGET_BLUETOOTH_ADDRESS = nearby_devices[choice][0]  # Get selected device's MAC
port = 3  # Ensure this matches the receiver's port

# 🔹 Step 3: File to send
file_path = "test_file.txt"

# Create a test file if it doesn't exist
if not os.path.exists(file_path):
    with open(file_path, "w") as f:
        f.write("Hello from the sender side!")

try:
    # 🔹 Create Bluetooth socket
    sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    
    print(f"🔗 Connecting to {TARGET_BLUETOOTH_ADDRESS} on port {port}...")
    sock.connect((TARGET_BLUETOOTH_ADDRESS, port))
    print("✅ Connected to the receiver!")

    # 🔹 Read and send the file data
    with open(file_path, "rb") as f:
        data = f.read()
        sock.sendall(data)

    print("📤 File sent successfully!")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    sock.close()
