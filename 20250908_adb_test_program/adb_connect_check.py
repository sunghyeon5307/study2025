import subprocess

result = subprocess.check_output(["adb", "devices"], text=True)
print(result)