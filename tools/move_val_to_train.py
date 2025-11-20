import os
import random
import shutil
from pathlib import Path

# Base paths
base_dir = Path("D:/Ai Systems Group/data/weeds_yolo")
img_val = base_dir / "images" / "val"
img_train = base_dir / "images" / "train"
lbl_val = base_dir / "labels" / "val"
lbl_train = base_dir / "labels" / "train"

# How many to move
n_to_move = 27

# Get all image files in validation
val_images = [f for f in img_val.glob("*.*") if f.suffix.lower() in [".jpg", ".png", ".jpeg"]]

# Randomly choose 30
to_move = random.sample(val_images, n_to_move)

for img_path in to_move:
    label_path = lbl_val / f"{img_path.stem}.txt"

    # Move image
    shutil.move(str(img_path), img_train / img_path.name)

    # Move label if exists
    if label_path.exists():
        shutil.move(str(label_path), lbl_train / label_path.name)
    else:
        print(f"⚠️ No label found for {img_path.name}")

print(f"✅ Moved {len(to_move)} images and their labels from val → train.")
