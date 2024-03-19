# courtesy of https://github.com/alexandrebarachant/muse-lsl?tab=readme-ov-file

import subprocess

duration = 5
command = ['muselsl', 'record_direct', '--duration', str(duration)]
subprocess.run(command)
print("Recording completed.")
