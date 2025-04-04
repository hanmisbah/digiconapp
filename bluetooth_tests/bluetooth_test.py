import asyncio
from bleak import BleakScanner # type: ignore

async def check_bluetooth():
    print("🔍 Scanning for Bluetooth devices...")
    devices = await BleakScanner.discover()
    
    if devices:
        print("\n✅ Bluetooth is available. Found devices:")
        for device in devices:
            print(f"- {device.name} ({device.address})")
    else:
        print("\n❌ No Bluetooth devices found. Make sure Bluetooth is enabled.")

# Run the function
asyncio.run(check_bluetooth())
