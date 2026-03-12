import glob

count = 0
for f in glob.glob("yolo_dataset/labels/train/*.txt"):
    for l in open(f):
        if l.startswith("4 "):
            count += 1

print("toilet_floor in train:", count)
