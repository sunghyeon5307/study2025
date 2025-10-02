import subprocess

for i in range(1, 151):
    filename = f"{i}.png"
    with open(filename, "wb") as f:
        f.write(subprocess.check_output(["adb", "exec-out", "screencap", "-p"]))
    print(f"{filename} saved")
