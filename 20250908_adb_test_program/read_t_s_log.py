import subprocess, re, math

dev_path = "/dev/input/event7"   
min_x, max_x = 0, 4095
min_y, max_y = 0, 4095
w, h = 1080, 2400


def raw_to_pixel(rx, ry):
    px = int(round((rx - min_x) * w / max(1, (max_x - min_x))))
    py = int(round((ry - min_y) * h / max(1, (max_y - min_y))))

    return px, py



LINE = re.compile(r"^\[\s*(\d+\.\d+)\]\s+(/dev/input/event\d+):\s+(\S+)\s+(\S+)\s+(.*)$")


p = subprocess.Popen(["adb", "shell", "getevent", "-lt"], stdout=subprocess.PIPE, text=True, bufsize=1)

f = open("touch_log.tsv", "w", encoding="utf-8")
down_x = down_y = last_x = last_y = None

try:
    for line in p.stdout:
        m = LINE.match(line.strip())
        if not m: continue
        dev, etype, code, rest = m.group(2), m.group(3), m.group(4), m.group(5)
        if dev != dev_path: continue

        if etype == "EV_ABS":
            v = int(rest.split()[-1], 16)
            if code == "ABS_MT_POSITION_X":
                last_x = v;  down_x = v if down_x is None else down_x
            elif code == "ABS_MT_POSITION_Y":
                last_y = v;  down_y = v if down_y is None else down_y
            elif code == "ABS_MT_TRACKING_ID":
                if v != 0xFFFFFFFF:  
                    down_x = down_y = last_x = last_y = None
                else:            
                    if None not in (down_x, down_y, last_x, last_y):
                        x1, y1 = raw_to_pixel(down_x, down_y)
                        x2, y2 = raw_to_pixel(last_x, last_y)


                        dist = math.hypot(x2 - x1, y2 - y1)
                        if dist >= 50:
                            f.write(f"S\t{x1}\t{y1}\t{x2}\t{y2}\n")
                            print(f"S\t{x1}\t{y1}\t{x2}\t{y2}")
                        else:
                            f.write(f"T\t{x1}\t{y1}\n")
                            print(f"T\t{x1}\t{y1}")


                    down_x = down_y = last_x = last_y = None
finally:
    try: p.terminate()
    except: pass
    f.close()

