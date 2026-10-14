# Vehicle Detection Fairness and Robustness Audit

This project implements a fairness and adversarial robustness audit for a vehicle detection system using synthetic CCTV image fixtures.

## Overview of Implementation

### 1. Fairness Audit (`src/fairness_audit.py`)
* **`compute_iou(box_a, box_b)`**: Calculates the Intersection-over-Union (IoU) between two bounding boxes formatted as `[x, y, w, h]`. It converts the box coordinates to corners, computes the overlapping area (clamping non-overlapping boxes to zero area), and divides it by the total union area.
* **`match_ground_truth(gt_boxes, detections, iou_threshold)`**: Compares a list of ground-truth bounding boxes against model detections. Returns a list of booleans indicating whether each ground-truth box was successfully matched with an IoU greater than or equal to the threshold (0.3).
* **`audit_by_category(coco_path, fixtures_dir, iou_threshold, transform)`**: Reads COCO image annotations, runs the mock detector on each image, and evaluates detections using `match_ground_truth`. It calculates total ground-truth count, total detected count, and recall score per category. It also supports an optional image `transform` function to evaluate perturbed images.
* **`find_underperforming_categories(category_stats, recall_threshold)`**: Identifies vehicle classes that fall strictly below the required recall threshold (0.90) and sorts them worst-first.

### 2. Adversarial Robustness Audit (`src/adversarial.py`)
* **`perturb_image(img, eps)`**: Applies an $L_\infty$ FGSM-style perturbation on RGB PIL images based on the detector's color rule. It lowers the Red channel by `eps` while increasing the Green and Blue channels by `eps`, clamping values between 0 and 255.
* **`audit_under_attack(coco_path, fixtures_dir, eps_values, iou_threshold)`**: Re-runs `audit_by_category` across various perturbation values to measure model performance decay under attack.
* **`find_most_fragile(attack_stats, eps, top_k)`**: Computes the drop in recall between clean images (eps = 0) and perturbed images ($\varepsilon$) for each category, returning the top `k` classes with the largest drop.