import asyncio
from bleak import BleakScanner, BleakClient

# The device name we set in the Arduino code
DEVICE_NAME = "XIAO_Flex"

# The 16-bit UUID (0x19B2) expanded to the standard 128-bit format
CHARACTERISTIC_UUID = "000019b2-0000-1000-8000-00805f9b34fb"

# This callback function runs automatically every time the XIAO sends a new angle
def notification_handler(sender, data):
    # The data arrives as raw bytes. We decode it back into a text string.
    angle_str = data.decode('utf-8')
    print(f"Bend Angle: {angle_str}°")

async def main():
    print(f"Scanning for {DEVICE_NAME}...")
    
    # 1. Scan the airwaves for your specific board
    device = await BleakScanner.find_device_by_name(DEVICE_NAME)
    
    if device is None:
        print(f"Could not find {DEVICE_NAME}. Is the board powered on?")
        return

    print(f"Found {DEVICE_NAME} at {device.address}! Connecting...")

    # 2. Connect to the board
    async with BleakClient(device) as client:
        print("Successfully connected!")
        
        # 3. Subscribe to the data stream
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        print("Listening for sensor data... (Press Ctrl+C to stop)")
        
        # 4. Keep the script running forever so the handler can catch incoming data
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nDisconnecting gracefully...")
            await client.stop_notify(CHARACTERISTIC_UUID)

if __name__ == "__main__":
    # Bleak relies on Python's asyncio to handle real-time background tasks
    asyncio.run(main())