import os
import multiprocessing
import time
from muselsl import stream, list_muses, record

def record_eeg(duration, filename):
    # Ensure the directory exists
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    muses = list_muses()
    if not muses:
        print("No Muse found. Make sure your Muse is turned on and in pairing mode.")
        return

    muse_address = muses[0]['address']
    print(f"Connecting to Muse: {muse_address}...")

    # Attempt to start the Muse stream
    try:
        streaming_process = multiprocessing.Process(target=stream, args=(muse_address,))
        streaming_process.start()

        # Wait a bit for the stream to start
        time.sleep(5)  # Adjust this delay as needed

        # Record EEG data
        print("Starting EEG recording...")
        record_process = multiprocessing.Process(target=record, args=(duration, filename))
        record_process.start()
        record_process.join()  # Wait for the recording process to finish

    except KeyboardInterrupt:
        print("Disconnected.")
    finally:
        if streaming_process.is_alive():
            streaming_process.terminate()
        print("Recording complete.")

if __name__ == "__main__":
    # Parameters
    recording_duration = 5  # seconds
    filename = "./eeg_recording.csv"

    record_eeg(recording_duration, filename)
