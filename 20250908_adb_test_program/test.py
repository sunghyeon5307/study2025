import subprocess

process = subprocess.Popen(
    ["adb", "shell", "getevent", "-lt"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True
)

for line in process.stdout:
    print(line.strip())


