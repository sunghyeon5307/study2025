import os, random, shutil, glob

folder = r"C:\study\20250924_12agp_cls\data"          
save_folder = r"C:\study\20250924_12agp_cls\dataset"         
split = 0.8             

random.seed(42)

classes = sorted(next(os.walk(folder))[1])

for split in ["train","val"]:
    for c in classes:
        os.makedirs(os.path.join(save_folder, split, c), exist_ok=True)

for c in classes:
    imgs = sum([glob.glob(os.path.join(folder, c, f"*.{ext}")) 
                for ext in ["png","jpg","jpeg","bmp","webp"]], [])
    random.shuffle(imgs)
    k = int(len(imgs)*split)
    train, val = imgs[:k], imgs[k:]
    for s, lst in [("train",train), ("val",val)]:
        for p in lst:
            shutil.copy2(p, os.path.join(save_folder, s, c, os.path.basename(p)))
print("done")
