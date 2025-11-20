# High Precision Weed Detection in Rose Fields

This repository presents a deep learning–based approach for high-precision weed detection in rose plantations, 
employing both YOLOv8 and YOLOv11 architectures for object detection and instance segmentation. 
The project includes complete training pipelines, dataset-processing utilities, prediction notebooks, 
and augmentation strategies designed to support robust model generalization in challenging agricultural environments.
## Table of Contents
- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Architecture & Approach](#architecture--approach)
- [Installation](#installation)
- [Usage](#usage)
- [Future Improvements](#future-improvements)
- [Official Documentation](#official-documentation)

## Project Overview

This project aims to build a **robust and precise computer vision system** capable of detecting weeds in rose fields — a highly challenging environment due to:

- strong visual similarity between weeds and rose stems  
- heavy occlusion and dense vegetation  
- lighting variability  
- limited annotated segmentation data  

To address this, multiple YOLO-based architectures were trained and compared:

### YOLOv8 Models
- `yolov8n` — detection  
- `yolov8s` — detection  
- `yolov8n-seg` — instance segmentation  
- `yolov8s-seg` — instance segmentation  

### YOLOv11 Models
- `yolov11n` — detection  
- `yolov11n-seg` — instance segmentation  

All training was performed using Jupyter notebooks inside the `configs/` folder.  
A separate technical report contains full metrics, comparisons, and evaluation.

## Dataset

The dataset used in this study was **manually constructed** for weed–rose discrimination tasks and 
is provided in two formats: YOLO bounding-box annotations and YOLO polygon-mask annotations.
### Detection Dataset
- **206** annotated images  
- YOLO bounding-box format  
- Located in:
  `data/weeds_yolo/`

### Segmentation Dataset
- **91** images with instance masks  
- YOLO segmentation format  
- Located in:
  `data/weeds_yolo_mask/`

### Dataset Structure (YOLO Format)
```
dataset/
 ├── images/
 │     ├── train/
 │     └── val/
 └── labels/
       ├── train/
       └── val/
```
### Dataset Tools (tools/ folder)  
- split_yolo.py  
- split_yolo_masks.py  
- move_val_to_train.py  
- rose_oversampling.ipynb  

## Architecture & Approach

### Detection Models  
- YOLOv8n  
- YOLOv8s  
- YOLOv11n  

### Segmentation Models  
- YOLOv8n-seg  
- YOLOv8s-seg  
- YOLOv11n-seg  

### Training Pipelines  
Located in:
```
configs/
 ├── yolov8n_train.ipynb
 ├── yolov8s_train.ipynb
 ├── yolov8n-seg_train.ipynb
 ├── yolov8s-seg_train.ipynb
 ├── yolov11n_train.ipynb
 ├── yolov11n-seg_train.ipynb
 ```

### Augmentation Strategy  
This project uses two augmentation pipelines:
1. YOLO built-in augmentations:
```hsv_h=0.015, hsv_s=0.7, hsv_v=0.4
degrees=5.0, translate=0.1, scale=0.5, shear=2.0
perspective=0.0
flipud=0.0, fliplr=0.5
mosaic=0.5, mixup=0.1, close_mosaic=10
cls=1.0, weight_decay=0.001, lrf=0.0005
```
2. Albumentation augmentations:
```A.MotionBlur(p=0.02, blur_limit=5)
A.MedianBlur(p=0.02, blur_limit=5)
A.RandomBrightnessContrast(brightness_limit=0.15, contrast_limit=0.15, p=0.5)
A.CLAHE(clip_limit=(1.0, 3.0), tile_grid_size=(8, 8), p=0.3)
A.ToGray(p=0.05)
A.ImageCompression(quality_range=(70, 100), p=0.2)
A.GaussNoise(
    std_range=(math.sqrt(10)/255, math.sqrt(40)/255),
    mean_range=(0, 0),
    p=0.15
)
```
## Installation
### 1. Download the Project

1. Go to the GitHub repository page in your browser.  
2. Click on **Code → Download ZIP**.  
3. Extract the ZIP archive to a folder of your choice, for example:
   - `D:/Ai Systems Project/high-precision-weed-detection`
4. Open a terminal (or Anaconda Prompt) and navigate into the project folder, e.g.:

```bash
cd "D:/Ai Systems Project/high-precision-weed-detection"
```
### 2. Create a virtual environment
1. Using conda (See below install guide):
```bash
conda create -n weeds python=3.10
conda activate weeds
```
2. Using Python venv:
```bash
python -m venv weeds
weeds\Scripts\activate
```

### 3. Install Python Dependencies
1. Core dependencies:
```bash
pip install numpy==2.2.6
pip install pandas==2.3.3
pip install scipy==1.15.3
pip install matplotlib==3.10.7
pip install tqdm==4.67.1
pip install pillow==11.3.0
pip install pyyaml==6.0.3
```
2. Computer vision & augmentations:
```bash
pip install opencv-python==4.11.0.86
pip install albucore==0.0.24
pip install albumentations==2.0.8
```
3. Jupyter environment:
```bash
pip install jupyterlab==4.4.10
pip install notebook==7.4.7
pip install ipykernel==7.0.1
```
4. Pytorch (Adjust based on your CUDA version if needed):
```bash
pip install torch==2.5.1+cu121 torchvision==0.20.1+cu121 --index-url https://download.pytorch.org/whl/cu121
```
5. Ultralytics YOLO model:
```bash
pip install ultralytics==8.3.227
```


## Usage

### 1. Training  
Use notebooks inside `configs/`.  
Results are saved to:
`work_dirs/<model-name>/`

### 2. Image Prediction  
`model_predictions/prediction_notebooks/image_prediction.ipynb` <br>
Outputs saved to:
`model_predictions/weeds-unlabeled-pred-<modelname>/`

### 3. Video Prediction  
`model_predictions/prediction_notebooks/video_prediction.ipynb`  
Output saved to:
`model_predictions/video_prediction/`

## Future Improvements
- Expand segmentation dataset  
- Expand bounding boxes dataset
- Train larger YOLO models on expanded datasets  
- ONNX/TensorRT deployment  
- Integrate real-time robotics pipeline  

## Official Documentation
- Ultralytics: https://docs.ultralytics.com  
- Albumentations: https://albumentations.ai  
- Label Studio: https://labelstud.io  
- OpenCV: https://opencv.org
- Conda: https://docs.conda.io/projects/conda/en/stable/user-guide/install/windows.html
