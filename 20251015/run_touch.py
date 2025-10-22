import subprocess
import time

file = "log.tsv"

with open(file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line.startswith("X="):
            x = line.split(",")[0].split("=")[1]
            y = line.split(",")[1].split("=")[1]
            subprocess.run(["adb", "shell", "input", "tap", x, y])
            time.sleep(1)
            subprocess.run(["adb", "shell"])
