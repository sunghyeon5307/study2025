import subprocess
import time

INFILE = "touch_log.tsv"

with open(INFILE, "r", encoding="utf-8") as f:
    for i in f:
        parts = i.strip().split()
        _, x, y = parts  


        subprocess.run(["adb", "shell", "input", "tap", x, y])

        time.sleep(1)                                                       