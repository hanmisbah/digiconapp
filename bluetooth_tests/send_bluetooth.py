import os
import time
from bleak import BleakClient, BleakScanner # type: ignore

# Replace this with your phone's Bluetooth MAC address
TARGET_BLUETOOTH_ADDRESS = "94:32:51:15:41:05"  # Update with JODU's actual address

# File to send
FILE_PATH = "test_file.txt"

async def send_file():
    device = await BleakScanner.find_device_by_address(TARGET_BLUETOOTH_ADDRESS)
    
    if device is None:
        print("❌ Device not found. Make sure Bluetooth is on and paired!")
        return
    
    async with BleakClient(device) as client:
        print("✅ Connected to device:", device)
        
        # Simulate file transfer (Bleak does not support full file transfer)
        with open(FILE_PATH, "rb") as file:
            data = file.read()
            print(f"📤 Sending {len(data)} bytes to {TARGET_BLUETOOTH_ADDRESS}...")

            # Example: Send data chunk-by-chunk (this part depends on your phone's Bluetooth support)
            for chunk in [data[i:i+20] for i in range(0, len(data), 20)]:
                await client.write_gatt_char("UUID_HERE", chunk)  # Replace "UUID_HERE" with correct Bluetooth UUID
                time.sleep(0.5)  # Simulate delay

        print("✅ File sent successfully!")

# Run the Bluetooth transfer
import asyncio
asyncio.run(send_file())
