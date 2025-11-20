import os
import random
import shutil
from pathlib import Path

# ==== CONFIG ====
BASE = Path(r"D:/Ai Systems Group/data/weeds_yolo_mask")
IMAGES_SRC = BASE / "images"
LABELS_SRC = BASE / "labels"

TRAIN_TARGET = 70
VAL_TARGET = 21
SEED = 42
random.seed(SEED)

# ==== OUTPUT FOLDERS ====
IMAGES_TRAIN = IMAGES_SRC / "train"
IMAGES_VAL   = IMAGES_SRC / "val"
LABELS_TRAIN = LABELS_SRC / "train"
LABELS_VAL   = LABELS_SRC / "val"
for p in [IMAGES_TRAIN, IMAGES_VAL, LABELS_TRAIN, LABELS_VAL]:
    p.mkdir(parents=True, exist_ok=True)

# ==== COLLECT MATCHED IMAGE/LABEL PAIRS ====
image_exts = {".jpg", ".jpeg", ".png"}
all_imgs = [p for p in IMAGES_SRC.iterdir() if p.is_file() and p.suffix.lower() in image_exts]

pairs = []
missing = []
for img in all_imgs:
    lbl = LABELS_SRC / f"{img.stem}.txt"
    if lbl.exists():
        pairs.append((img, lbl))
    else:
        missing.append(img.name)

if missing:
    print(f"[WARN] {len(missing)} images have no label and will be ignored:")
    for n in missing[:10]:
        print("   -", n)
    if len(missing) > 10:
        print("   ...")

random.shuffle(pairs)

need = TRAIN_TARGET + VAL_TARGET
if len(pairs) < need:
    print(f"[INFO] Only {len(pairs)} matched pairs found; "
          f"cannot take {need}. Will use as many as available with same ratio.")
    # keep ~77% train, ~23% val if not enough pairs
    train_take = min(len(pairs), int(round(len(pairs) * TRAIN_TARGET / max(need,1))))
    val_take   = len(pairs) - train_take
else:
    train_take = TRAIN_TARGET
    val_take   = VAL_TARGET

train_pairs = pairs[:train_take]
val_pairs   = pairs[train_take:train_take + val_take]

print(f"Using pairs -> Train: {len(train_pairs)} | Val: {len(val_pairs)} | Total matched: {len(pairs)}")

def copy_pair(img_path: Path, lbl_path: Path, dst_img_dir: Path, dst_lbl_dir: Path):
    dst_img = dst_img_dir / img_path.name
    dst_lbl = dst_lbl_dir / f"{img_path.stem}.txt"
    shutil.copy2(img_path, dst_img)
    shutil.copy2(lbl_path, dst_lbl)

for img, lbl in train_pairs:
    copy_pair(img, lbl, IMAGES_TRAIN, LABELS_TRAIN)

for img, lbl in val_pairs:
    copy_pair(img, lbl, IMAGES_VAL, LABELS_VAL)

print("✅ Split complete.")
print("Train images dir:", IMAGES_TRAIN)
print("Val images dir:  ", IMAGES_VAL)
print("Train labels dir:", LABELS_TRAIN)
print("Val labels dir:  ", LABELS_VAL)
