import time
from save_touch import read_touch, write_touch 
from method.dump import dump_save_keyword
from method.cls import cls_save_keyword
from method.ocr import ocr_save_keyword

def save_method(dump_result, cls_result, ocr_result):
    if dump_result >= cls_result and dump_result >= ocr_result:
        method = "dump"
        id = dump_keyword
    elif cls_result >= dump_result and cls_result >= ocr_result:
        method = "cls"
        id = cls_keyword
    else:
        method = "ocr"
        id = ocr_keyword
    with open("log.tsv", "a", encoding="utf-8") as f:
        f.write(f"ID:{id}\nMETHOD:{method}\n\n")



if __name__ == "__main__":
    try:
        while True:
            # 좌표 값 읽고 스크립트에 저장
            x,y = read_touch()
            write_touch(x, y)

            # dump, cls, ocr 화면 분류 및 정확도 계산
            dump_keyword, dump_result = dump_save_keyword()
            cls_keyword, cls_result = cls_save_keyword()
            ocr_keyword, ocr_result = ocr_save_keyword()

            # 분류 방법 중 가장 정확도가 높은 방법 스크립트에 저장
            save_method(dump_result, cls_result, ocr_result)

            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
