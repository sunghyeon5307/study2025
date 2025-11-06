import cv2, numpy as np, matplotlib.pyplot as plt

img = cv2.cvtColor(cv2.imread(r"C:\study\20251104\b3486276dddc45a04b97bafbd9a7bf37.jpg"), cv2.COLOR_BGR2RGB)
plt.figure(figsize=(8,6))
plt.imshow(img); plt.title("좌상→우상→우하→좌하 순서로 4점 클릭 후 Enter")
pts = plt.ginput(4, timeout=-1)  
plt.close()

src = np.float32(pts)  

W, H = 400, 200
dst = np.float32([[0,0],[W,0],[W,H],[0,H]])
M = cv2.getPerspectiveTransform(src, dst)

rectified = cv2.warpPerspective(cv2.cvtColor(img, cv2.COLOR_RGB2BGR), M, (W, H))
cv2.imwrite(r"C:\study\20251104\result.jpg", rectified)
