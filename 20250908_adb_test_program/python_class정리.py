import subprocess

class ADBclient:
    def connected(self):
        '''
        ADB 연결 확인
        adb devices
        '''
        r = subprocess.check_output(["adb", "devices"], text=True)
        return r
    
    def tap_swipe_load(self):
        '''
        ADB 터치/드래그 이벤트 불러오기
        adb shell getevent -lt
        '''
        r = subprocess.Popen(["adb", "shell", "getevent", "-lt"], stdout=subprocess.PIPE, text=True, bufsize=1)
        return r

    def capture_screen(self):
        '''
        ADB 현재 화면 캡쳐 후 불러오기
        adb exec-out screencap -p
        '''
        r = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
        return r

    def reboot(self):
        '''
        ADB 디바이스 재부팅 후 부팅완료까지 대기
        adb reboot
        adb wait-for-device
        '''
        r = subprocess.run(["adb", "reboot"])
        r = subprocess.run(["adb", "wait-for-device"])
        return r
    
    def get_display_resolution(self):
        '''
        ADB 디바이스 화면 해상도 가져오기
        adb shell wm size
        '''
        r = subprocess.check_output(["adb", "shell", "wm", "size"], text=True)
        return r
    
    def get_touch_resolution(self):
        '''
        ADB 디바이스 터치 해상도 가져오기
        adb shell getevent -p
        '''
        r = subprocess.check_output(["adb", "shell", "getevent", "-p"], text=True)
        return r
    
    def convert_touch_to_screen(self, rx, ry, max_x, max_y, screen_w, screen_h):
        '''
        터치 원시 좌표 -> 화면 좌표
        screen_x = round(rx * (screen_w - 1) / max_x)
        screen_y = round(ry * (screen_h - 1) / max_y)
        '''
        px = int(round(rx * (screen_w - 1) / max(1, max_x)))
        py = int(round(ry * (screen_h - 1) / max(1, max_y)))
        return px, py

    
    def send_touch(self, x, y):
        '''
        ADB 터치 좌표 전송
        adb shell input tap x y
        '''
        r = subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])
        return r
    
    def send_swipe(self, x1, y1, x2, y2, duration=100):
        '''
        ADB 드래그(스와이프) 좌표 전송
        adb shell input swipe x1 y1 x2 y2 duration
        '''
        r = subprocess.run(["adb", "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])
        return r
    
    def reconnect(self):
        '''
        ADB 디바이스 재연결
        adb kill-server
        adb start-server
        adb wait-for-device         
        '''
        r = subprocess.run(["adb", "kill-server"])
        r = subprocess.run(["adb", "start-server"])
        r = subprocess.run(["adb", "wait-for-device"])
        return r
    
    def get_memory(self):
        '''
        ADB 디바이스 메모리 사용량 가져오기, 단위 KB
        adb shell cat /proc/meminfo        
        '''
        r = subprocess.check_output(["adb", "shell", "cat", "/proc/meminfo"], text=True)
        return r
    
    def get_logcat(self):
        '''
        ADB Logcat 정보 가져오기
        adb logcat -d -t <lines>
        '''
        r = subprocess.check_output(["adb", "logcat", "-d", "-t", "100"], text=True)
        return r