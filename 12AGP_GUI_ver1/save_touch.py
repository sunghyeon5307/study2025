import subprocess

def read_touch():
    p = subprocess.Popen(["adb", "shell", "getevent", "-lt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
    x=y=None
    for line in p.stdout:
        if "ABS_X" in line:
            x = int(line.split()[-1], 16)
            print("X =", x)
        elif "ABS_Y" in line:
            y = int(line.split()[-1], 16)
            print("Y =", y)
            return x, y

def write_touch(x, y):
    with open("log.tsv", "a", encoding="utf-8") as f:
        f.write(f"X={x},Y={y}\n")
    return f"X = {x}\nY = {y}" 

