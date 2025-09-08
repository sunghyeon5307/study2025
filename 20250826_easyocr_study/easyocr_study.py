import easyocr as eo

reader = eo.Reader(['ko', 'en'], gpu=True)

img_path="image3.png"
result = reader.readtext(img_path, detail=0)

print(result)