from pylsl import StreamInlet, resolve_byprop
import pandas as pd
import numpy as np
from time import time, strftime, gmtime

def record_eeg_simple(duration, filename):
    print("Looking for an EEG stream...")
    streams = resolve_byprop('type', 'EEG', timeout=10)
    if not streams:
        print("Can't find EEG stream.")
        return

    inlet = StreamInlet(streams[0])
    print("Connected to EEG stream.")

    timestamps = []
    eeg_data = []
    start_time = time()
    while time() - start_time < duration:
        sample, timestamp = inlet.pull_sample()
        eeg_data.append(sample)
        timestamps.append(timestamp)

    eeg_df = pd.DataFrame(data=eeg_data, columns=['Channel1', 'Channel2', 'Channel3', 'Channel4'])
    eeg_df['Timestamps'] = timestamps

    eeg_df.to_csv(filename, index=False)
    print(f"Recording complete, data saved to {filename}")

if __name__ == "__main__":
    record_eeg_simple(5, "eeg_recording.csv")
