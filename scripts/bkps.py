import asyncio
import csv
import time
from bleak import BleakScanner, BleakClient

MUSE_NAME = "MuseS-7EC9"  # Adjust based on your Muse's advertised name
output_csv = "eeg_data.csv"

async def find_muse():
    devices = await BleakScanner.discover()
    for device in devices:
        if device.name is None:
            continue
        if MUSE_NAME in device.name:
            print(f"Found Muse: {device.name} at {device.address}")
            return device.address
    return None

async def connect_and_stream(address, output_csv):
    async with BleakClient(address) as client:
        await client.connect()
        if await client.is_connected():
            print("Connected to the Muse.")

            # Assuming characteristic_uuid is known and specific to Muse EEG data streaming
            characteristic_uuids = [
                "00002a5b-0000-1000-8000-00805f9b34fb",  # Example UUID; replace with actual
                # Add other UUIDs as needed
            ]

            def callback(sender, data):
                with open(output_csv, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow([time.time()] + list(data))

            for uuid in characteristic_uuids:
                await client.start_notify(uuid, callback)
            print("Started streaming data. Press Ctrl+C to stop.")
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                for uuid in characteristic_uuids:
                    await client.stop_notify(uuid)
                print("Stopped streaming data.")
        else:
            print("Failed to connect to Muse.")

async def list_characteristics(address):
    async with BleakClient(address) as client:
        await client.connect()
        if await client.is_connected():
            print("Connected to the Muse.")
            services = await client.get_services()
            for service in services:
                print(f"Service: {service.uuid}")
                for char in service.characteristics:
                    if "notify" in char.properties:
                        print(f"  - Characteristic: {char.uuid}, Properties: {char.properties}")


async def main():
    address = await find_muse()
    if address:
        await list_characteristics(address)
    else:
        print("No Muse devices found.")
    if address:
        await connect_and_stream(address, output_csv)
    else:
        print("No Muse devices found.")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())



from muselsl import stream, list_muses, record
import asyncio

if __name__ == "__main__":
    muses = list_muses()

    if not muses:
        print('No Muses found')
    else:
        address = muses[0]['address']
        print(f"Streaming from {address}")
        stream_process = stream(address)
        stream_process.start()
        duration = 5 # seconds
        filename = "muse_recording.csv" 

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(record(duration, filename))
            print('Recording has ended')
        except KeyboardInterrupt:
            print("Recording stopped by user.")
        finally:
            stream_process.terminate()

import asyncio
from muselsl import stream, list_muses, record

async def record_muse_data(duration=60, filename="muse_recording.csv"):
    muses = await list_muses()
    if not muses:
        print("No Muse found. Make sure your Muse is turned on and in pairing mode.")
        return

    muse = muses[0]
    print(f"Found Muse with address: {muse['address']}. Streaming...")

    # Start streaming
    await stream(muse['address'])

    # Wait a bit for the stream to stabilize
    await asyncio.sleep(5)

    # Start recording
    print(f"Recording EEG data for {duration} seconds...")
    await record(duration, filename)

    print(f"Recording has ended. Data saved to {filename}.")

async def main():
    duration = 60  # Duration in seconds
    filename = "muse_recording.csv"  # Output filename
    await record_muse_data(duration, filename)

# This checks if the script is the main program and ensures it's not executed when imported as a module
if __name__ == "__main__":
    # Run the main function in the asyncio event loop
    asyncio.run(main())
