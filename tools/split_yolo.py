import os, shutil, random
from pathlib import Path

# Base folder that contains "images" and "labels"
BASE = Path(r"C:\Users\Supreme Leader David\Downloads\project-5-at-2025-11-10-14-02-182665ef")
IMAGES = BASE / "images"
LABELS = BASE / "labels"

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

# Desired split (e.g., 0.8 => 80% train / 20% val)
SPLIT_RATIO = 0.6
SEED = 42

# Ensure target dirs exist
for s in ("train", "val"):
    (BASE / "images" / s).mkdir(parents=True, exist_ok=True)
    (BASE / "labels" / s).mkdir(parents=True, exist_ok=True)

# Gather files
all_imgs = [p for p in IMAGES.iterdir() if p.is_file() and p.suffix.lower() in IMG_EXTS]
all_lbls = {p.stem: p for p in LABELS.iterdir() if p.is_file() and p.suffix.lower() == ".txt"}

# Keep only pairs (image + label with same stem)
pairs = []
missing_labels = []
for img in all_imgs:
    stem = img.stem
    lbl = all_lbls.get(stem)
    if lbl is None:
        missing_labels.append(img.name)
    else:
        pairs.append((img, lbl))

print(f"Found images: {len(all_imgs)}")
print(f"Found labels: {len(all_lbls)}")
print(f"Usable pairs: {len(pairs)}")
if missing_labels:
    print(f"Images missing labels: {len(missing_labels)} (showing up to 10): {missing_labels[:10]}")

if not pairs:
    raise SystemExit("No (image,label) pairs found. Check filenames and folders.")

# Split
random.seed(SEED)
random.shuffle(pairs)
n_train = int(len(pairs) * SPLIT_RATIO)
train_pairs = pairs[:n_train]
val_pairs   = pairs[n_train:]

def safe_copy(src: Path, dst_dir: Path):
    dst = dst_dir / src.name
    # Overwrite if exists to allow re-runs without errors
    shutil.copy2(src, dst)

for img, lbl in train_pairs:
    safe_copy(img, BASE / "images" / "train")
    safe_copy(lbl, BASE / "labels" / "train")

for img, lbl in val_pairs:
    safe_copy(img, BASE / "images" / "val")
    safe_copy(lbl, BASE / "labels" / "val")

print("✅ Done! Split into train and val sets.")
print(f"Train pairs: {len(train_pairs)} | Val pairs: {len(val_pairs)}")
print("images/train:", len(list((BASE / 'images' / 'train').glob('*'))))
print("labels/train:", len(list((BASE / 'labels' / 'train').glob('*'))))
print("images/val:  ", len(list((BASE / 'images' / 'val').glob('*'))))
print("labels/val:  ", len(list((BASE / 'labels' / 'val').glob('*'))))
