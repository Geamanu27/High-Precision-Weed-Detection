# YOLOv8s vs YOLOv8s-seg Evaluation Report

## **Dataset Overview**

- **Domain:** Detection and segmentation of *weeds* and *roses* in natural agricultural environments  
- **Objective:** Compare bounding-box detection and mask-based segmentation performance using the YOLOv8s architecture  
- **Classes:**  
  - `0 – weed`  
  - `1 – rose`

> **Note:** The segmentation dataset is **much smaller**, which naturally reduces mAP performance. 

---

## **1️. Dataset Splits**

| Model           | Task Type                         | Train Images | Validation Images | Total |
|-----------------|-----------------------------------|--------------|-------------------|-------|
| **YOLOv8s**     | Object Detection (Bounding Boxes) | 180          | 26                | 206   |
| **YOLOv8s-seg** | Instance Segmentation (Masks)     | 71           | 20                | 91    |

Both datasets share the same domain and scene variety, differing only in annotation format —  
the segmentation dataset uses polygon-based masks converted into YOLO segmentation format.

---

## **2️. Training Configuration**

| Parameter     | YOLOv8s (Detection) | YOLOv8s-seg (Segmentation) |
|---------------|----------------------|-----------------------------|
| Base Model    | `yolov8s.pt`         | `yolov8s-seg.pt`            |
| Epochs        | 120                  | 120                         |
| Image Size    | 1280×1280            | 1280×1280                   |
| Batch Size    | 6                    | 4                           |
| Device        | GPU (CUDA 0)         | GPU (CUDA 0)                |
| Seed          | 42                   | 42                          |
| Patience      | 25                   | 25                          |
| Augmentations | MotionBlur, MedianBlur, RandomBrightnessContrast, CLAHE, ToGray, ImageCompression, GaussNoise + YOLO built-ins (HSV, rotation, scaling, flipping, mosaic, mixup) | Same |
| Optimizer Settings | `cls=1.0`, `weight_decay=0.001`, `lrf=0.0005` | Same |

Both trainings were run with the same augmentations and hyperparameters for a fair performance comparison.

---

## **3️. Quantitative Results**

### **Training Metrics Evolution**

#### YOLOv8s (Detection)
![YOLOv8s](../work_dirs/yolov8s-weeds/results.png)

#### YOLOv8s-seg (Segmentation)
![YOLOv8s-seg](../work_dirs/yolov8s-seg-weeds/results.png)

### **Observations**

#### **Loss Convergence**
- Both models show **steady and smooth convergence** across all losses.  
- The segmentation model includes an additional `seg_loss` term which decreases consistently.  
- No overfitting is present.

#### **Precision & Recall**
- **YOLOv8s (Detection):**  
  Precision stabilizes around **0.70–0.75**, recall around **0.60–0.70**. 
- **YOLOv8s-seg (Segmentation):**  
  Precision is **less stable**, not necessarily lower.   
  Recall remains around **0.30–0.35**, as segmentation is harder with fewer images.

#### **Mean Average Precision (mAP)**  

| Metric | YOLOv8s | YOLOv8s-seg |
|--------|----------|-------------|
| **mAP@50 (B/M)** | **≈ 0.80–0.82**  | **≈ 0.30–0.33**  |
| **mAP@50–95 (B/M)** | **≈ 0.32–0.34**  | **≈ 0.21–0.23**  |

> Detection achieves higher mAP across IoU thresholds, as expected with a larger dataset.

---

## **4️. Qualitative Evaluation on Unseen Images**

Both models were evaluated on unseen agricultural images to assess generalization.

| YOLOv8s Predictions                     | YOLOv8s-seg Predictions                      |
|-----------------------------------------|----------------------------------------------|
| ![pred-bb](Images/yolov8s-IMG_4283.jpg) | ![pred-seg](Images/yolov8s-seg-IMG_4283.jpg) |

### **Analysis**

- **Detection Model:**  
  - Produces accurate bounding boxes for most plants.  
  - Sometimes merges dense clusters.

- **Segmentation Model:**  
  - Produces clearer shape boundaries.  
  - Struggles with very thin stems and overlapping leaves.  
  - Visually far more informative for agricultural analysis.

---

## **5. Comparative Summary**


| Aspect | YOLOv8s (Detection) | YOLOv8s-seg (Segmentation) | Verdict |
|--------|--------------------|-----------------------------|----------|
| Training Set Size | 180 | 71 | – |
| Validation Set Size | 26 | 20 | – |
| Localization Type | Bounding Boxes | Pixel-level Masks | 🟢 Segmentation more detailed |
| Precision / Recall | 0.72 / 0.65  | 0.65 / 0.32 | 🔵 Detection more stable |
| mAP@50–95 | **≈ 0.33**  | **≈ 0.22**  | 🔵 Detection higher |
| Qualitative Boundary Detail | Moderate | High | 🟢 Segmentation superior |
| Generalization | Strong | Moderate | 🔵 Detection more robust |

---

## **6️. Conclusions**

- **YOLOv8s** achieves significantly higher mAP and better precision/recall due to a larger dataset and easier task formulation.  
- **YOLOv8s-seg** provides **much better region-level detail**, despite lower recall and mAP.  
- Both models train stably without overfitting.  
- For **large-scale field inference**, detection is recommended.  
- For **botanical analysis, crop diagnostics, or robotics requiring exact plant shapes**, segmentation is superior.

---

## **Summary**

> **YOLOv8s-seg** provides deeper pixel-wise plant understanding, while **YOLOv8s** offers stronger numerical accuracy and robustness.  
> Choose segmentation for **precision agriculture analytics**, and detection for **broad, high-speed field detection** workloads.
