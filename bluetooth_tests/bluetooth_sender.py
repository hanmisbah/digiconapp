import asyncio
from bleak import BleakClient # type: ignore

# Replace this with your mobile device's Bluetooth address
DEVICE_ADDRESS = "CC:F9:F0:0D:58:DB"

async def send_file():
    try:
        async with BleakClient(DEVICE_ADDRESS) as client:
            print("✅ Connected to Bluetooth device.")

            # Read the file (change 'test_file.txt' to your file)
            with open("test_file.txt", "rb") as file:
                data = file.read()

            # Send data
            await client.write_gatt_char("00002a6e-0000-1000-8000-00805f9b34fb", data)
            print("📁 File sent successfully!")

    except Exception as e:
        print(f"❌ Failed to send file: {e}")

asyncio.run(send_file())
