import subprocess, re

dev_path = "/dev/input/event1"  
min_x, max_x = 0, 1079
min_y, max_y = 0, 1919
w, h = 1080, 1920

def clamp(v, lo, hi):
    return lo if v < lo else (hi if v > hi else v)

def raw_to_pixel(rx, ry):
    sx = (rx - min_x) / max(1, (max_x - min_x))
    sy = (ry - min_y) / max(1, (max_y - min_y))
    px = int(round(sx * (w - 1)))
    py = int(round(sy * (h - 1)))
    return clamp(px, 0, w - 1), clamp(py, 0, h - 1)

LINE_RE = re.compile(r"^\[\s*(\d+\.\d+)\]\s+(/dev/input/event\d+):\s+(\S+)\s+(\S+)\s+(.*)$")

p = subprocess.Popen(
    ["adb", "shell", "getevent", "-lt"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

start_ts = None
raw_x = raw_y = None
f = open("touch_log.tsv", "w", encoding="utf-8")

try:
    for line in p.stdout:
        m = LINE_RE.match(line.strip())
        if not m: 
            continue
        ts, dev, etype, code, rest = float(m.group(1)), m.group(2), m.group(3), m.group(4), m.group(5)
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
                if v == 0xFFFFFFFF and raw_x is not None and raw_y is not None:
                    px, py = raw_to_pixel(raw_x, raw_y)
                    t_ms = int(round((ts - start_ts) * 1000))
                    out = f"{t_ms}\t{px}\t{py}"
                    print(out)
                    f.write(out + "\n")
                    raw_x = raw_y = None
finally:
    try: p.terminate()
    except: pass
    try: p.wait(timeout=2)
    except: pass
    try: f.close()
    except: pass

