import cv2

img = cv2.imread(r"C:\study\20250918_12agp_adb_program2\datascreenshot_141.png")

alpha = 1.0   # 대비(>1면 대비↑)
beta  = -60    # 밝기(+면 밝아짐)

brighter = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
cv2.imwrite("out_beta.jpg", brighter)
