# 터치 패널 고유 범위 -> 화면 해상도 픽셀
import subprocess, re, sys


dev_path = "/dev/input/event7"
min_x, max_x = 0, 4095        
min_y, max_y = 0, 4095         
w, h = 1080, 2400 

def raw_to_pixel(rx, ry):
    sx = (rx - min_x) / max(1, (max_x - min_x))
    sy = (ry - min_y) / max(1, (max_y - min_y))
    px = int(round(sx * w))
    py = int(round(sy * h))
    return px, py

LINE_RE = re.compile(r"^\[\s*(\d+\.\d+)\]\s+(/dev/input/event\d+):\s+(\S+)\s+(\S+)\s+(.*)$")

process = subprocess.Popen(
    ["adb", "shell", "getevent", "-lt"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
    bufsize=1
)

start_ts = None
raw_x = None
raw_y = None
tracking = None 

file_out = open("touch_log.tsv", "w", encoding="utf-8")

try:
    for line in process.stdout:
        line = line.strip()
        if not line.startswith("["):
            continue

        m = LINE_RE.match(line)
        if not m:
            continue

        ts = float(m.group(1))
        dev = m.group(2)
        etype = m.group(3)  
        code  = m.group(4)  
        rest  = m.group(5)

        if dev != dev_path:
            continue

        if start_ts is None:
            start_ts = ts

        if etype == "EV_ABS":
            if code == "ABS_MT_POSITION_X":
                raw_x = int(rest.split()[-1], 16)
            elif code == "ABS_MT_POSITION_Y":
                raw_y = int(rest.split()[-1], 16)
            elif code == "ABS_MT_TRACKING_ID":              
                v = int(rest.split()[-1], 16)
                if v != 0xFFFFFFFF:
                    tracking = v 
                else:
                    if raw_x is not None and raw_y is not None:
                        px, py = raw_to_pixel(raw_x, raw_y)
                        t_ms = int(round((ts - start_ts) * 1000))
                        out_line = f"{t_ms}\t{px}\t{py}"

                        print(out_line)
                        file_out.write(out_line + "\n")

                    tracking = None
                    raw_x = raw_y = None

except KeyboardInterrupt:
    pass
finally:
    try:
        process.terminate()
    except Exception:
        pass
