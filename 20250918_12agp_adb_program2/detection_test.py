from ultralytics import YOLO
import cv2

model = YOLO('best2.pt')
img = r"C:\study\20250918_12agp_adb_program2\out_beta.jpg"
result = model.predict(source=img, conf=0.45, verbose=False)[0]

annotated1 = result.plot()
h, w = annotated1.shape[:2]
screen1 = cv2.resize(annotated1, (w//4, h//4), interpolation=cv2.INTER_AREA)

cv2.imshow("home", screen1)
cv2.waitKey(0)
cv2.destroyAllWindows()