import time
from save_read_touch import read_touch, write_touch 
from method.dump import save_keyword
from method.cls import keyword as cls_keyword
from method.ocr import ocr_keyword

def save_method(dump_result, cls_result, ocr_result):
    if dump_result >= cls_result and dump_result >= ocr_result:
        method = "dump"
    elif cls_result >= dump_result and cls_result >= ocr_result:
        method = "cls"
    else:
        method = "ocr"
    with open("log.tsv", "a", encoding="utf-8") as f:
        f.write(f"method:{method}\n\n")


if __name__ == "__main__":
    try:
        while True:
            x,y = read_touch()
            write_touch(x, y)

            dump_keyword, dump_result = save_keyword()

            cls_result = cls_keyword()

            ocr_result = ocr_keyword()
            save_method(dump_result, cls_result, ocr_result)

            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
