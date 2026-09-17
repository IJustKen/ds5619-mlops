# NOTES.md — Week 6: Containerize and Serve a Detector

**Student ID used with `generate_for_student.py`:**
142301038


## Built image size
166MB


## Swapping in a real checkpoint

<!-- What's the single biggest thing you'd change about this Dockerfile if
     src/mock_detector.py were swapped for a real torch-based checkpoint?
     (Think about what that does to build time and image size.) -->
### Image Size Increase: 
By default, the usual 'pip install torch' downloads PyTorch along with complete NVIDIA GPU libraries (CUDA) so that it works on graphics cards out of the box. 
Including all those extra GPU libraries increases the final Docker image size from ~166 MB to around 5-6 GBs.

### Effect:
Downloading GBs of extra software every time the container builds makes docker build and deployment extremely slow over the network.

### Option 1: 
Download a CPU-only version of torch so that it does not spend time downloading the GPU libraries which will never be used. This is assuming that the container is being used in CPU environment.

### Option 2: (assuming environment is GPU enabled)
While a GPU-enabled container will ultimately be large (5-6 GBs) using an official PyTorch base image (using 'FROM pytorch/pytorch' instead of 'FROM python:3.11-slim' and then 'RUN pip install torch') makes it like a cached base layer. 
This prevents re-downloading GBs of dependencies (requirements.txt) during application updates (like if we modify requirements.txt and torch was listed there)