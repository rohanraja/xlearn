import subprocess
import os
import time
import sys

mid = sys.argv[1]
pid = sys.argv[2]
totWorkers = int(sys.argv[3])

files = range(totWorkers)
command = "python"
processes = set()
max_processes = 5

for name in files:
    processes.add(subprocess.Popen([command, "train.py", mid, pid, str(name)]))
    if len(processes) >= max_processes:
        os.wait()
        processes.difference_update([
            p for p in processes if p.poll() is not None])
        
for p in processes:
    if p.poll() is None:
        p.wait()
