import time
from touch_read_save import read_touch, write_touch 

if __name__ == "__main__":
    try:
        while True:
            x,y = read_touch()
            write_touch(x, y)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass