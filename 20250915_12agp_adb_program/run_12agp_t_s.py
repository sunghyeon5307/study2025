import subprocess
import time

file = "touch_log.tsv"
swipe = 1000
rest = 1.0

with open(file, "r", encoding="utf-8") as f:
    for line in f:
        p = line.strip().split()
        if not p:
            continue

        if p[0] == "T" and len(p) ==3:
            _, x, y = p
            subprocess.run(["adb", "shell", "input", "tap", x, y])
        elif p[0] == "S" and len(p) == 5:
            _, x1, y1, x2, y2 = p
            subprocess.run(["adb", "shell", "input", "swipe", x1, y1, x2, y2, str(swipe)])
        time.sleep(rest)