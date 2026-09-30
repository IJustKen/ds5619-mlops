# README

In production CV pipelines, ground-truth labels are rarely available in real time. Therefore, we monitor the detector's **confidence scores** at inference time as a proxy for detecting domain shift (e.g., transitioning from clear daylight footage to low-light CCTV conditions).

## Background

This project monitors confidence score distributions across two simulated camera conditions:
* `data/fixtures/camera_A_daylight/` (Reference distribution)
* `data/fixtures/camera_B_lowlight/` (Live inference distribution)

## Code

Four key functions:

### 1. Feature Extraction (`extract_confidence_scores`)
Runs the detector model over all *.jpg images in a given directory and collects a flat list of confidence scores ([0.0, 1.0]).

### 2. Population Stability Index (`compute_psi`)
Discretizes reference and live score distributions into N equal-width bins (default: 10) and computes the Population Stability Index:

* Bins are clamped to a minimum proportion (1e-4) to prevent division-by-zero or logarithmic errors.
* Boundary edge cases (scores of exactly 1.0) are automatically assigned to the last bin.

### 3. Drift Classification (`classify_drift`)
Categorizes calculated PSI values into actionable operational bands:
* **`psi < 0.10`**: `"none"` (Distribution stable)
* **`0.10 <= psi < 0.25`**: `"moderate"` (Slight shift; warrants investigation)
* **`psi >= 0.25`**: `"significant"` (Action required; trigger retrain/alert)

### 4. Summary Statistics (`summarize_scores`)
Generates descriptive statistics (`count`, `mean`, `std`, `min`, `max`) rounded to 4 decimal places. Handles low-sample edge cases safely where $N < 2$.