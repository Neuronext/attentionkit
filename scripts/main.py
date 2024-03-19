from muselsl import stream, list_muses, record
import subprocess
import time
import os

def record_data(duration, filename):
    print("file name: ", filename)
    muses = list_muses()
    if not muses:
        print("No Muse devices found.")
        return
    muse_address = muses[0]['address']
    print(f"Connecting to Muse: {muse_address}...")

    stream_process = subprocess.Popen(['muselsl', 'stream', '--name', muse_address]) #stdout=subprocess.PIPE)

    # try:
    #     while True:
    #         output = stream_process.stdout.readline()
    #         if not output and stream_process.poll() is not None:
    #             break
    #         if output:
    #             print(output.strip())
    # except KeyboardInterrupt:
    #     # Terminate the stream process if interrupted
    #     stream_process.terminate()
    #     print("Stream terminated.")

    
    time.sleep(3)
    
    print("Recording EEG...")
    record_process = subprocess.Popen(['muselsl', 'record', '--duration', str(duration), '--filename', filename])#stdout=subprocess.PIPE)
    record_process.wait()
    stream_process.terminate()
    print("Disconnected.")

if __name__ == '__main__':
    record_data(3, 'eeg_data.csv')
