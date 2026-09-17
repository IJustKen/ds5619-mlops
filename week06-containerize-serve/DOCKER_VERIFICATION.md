# Docker verification

Fill this in after you build and run your container (see README.md,
"Part 2 — Dockerfile"). This is how we confirm your container actually works, since an
automated grader running in a sandbox may not always have Docker-in-Docker
available.

## Build

Paste the command you ran and its final output line (the one showing the
built image ID/tag):

docker build -t week6-detector .
[+] Building 17.7s (10/10) FINISHED                              docker:default
 => [internal] load build definition from Dockerfile                       0.0s
 => => transferring dockerfile: 1.28kB                                     0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim        4.5s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => [1/5] FROM docker.io/library/python:3.11-slim@sha256:9534e5a8e315485d  3.6s
 => => resolve docker.io/library/python:3.11-slim@sha256:9534e5a8e315485d  0.0s
 => => sha256:9534e5a8e315485d4061ed659af0fd78a284c015f 10.37kB / 10.37kB  0.0s
 => => sha256:d1053354624536b044162aaab1e418bd000ea35184f 1.75kB / 1.75kB  0.0s
 => => sha256:b8fe4ce3655e95f7f22c2a87d8e03a2f1f0cedc488a 5.49kB / 5.49kB  0.0s
 => => sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657 29.79MB / 29.79MB  2.4s
 => => sha256:3678bb828654fcc3752f7a5eb63c5accfa00c970472 4.27MB / 4.27MB  1.9s
 => => sha256:db840d086b65cf73e0feea3bd0cf11063818114e4 14.45MB / 14.45MB  3.0s
 => => sha256:f9efa1b83d065a7c5a3041582875b75d63c4ab3d4413514 249B / 249B  2.5s
 => => extracting sha256:6310eb16bf4251731feab01e8f633bf5e2d75a657ccad97f  0.5s
 => => extracting sha256:3678bb828654fcc3752f7a5eb63c5accfa00c97047252f25  0.1s
 => => extracting sha256:db840d086b65cf73e0feea3bd0cf11063818114e466846ae  0.3s
 => => extracting sha256:f9efa1b83d065a7c5a3041582875b75d63c4ab3d4413514d  0.0s
 => [internal] load build context                                          0.0s
 => => transferring context: 14.90kB                                       0.0s
 => [2/5] WORKDIR /app                                                     0.0s
 => [3/5] COPY requirements.txt .                                          0.0s
 => [4/5] RUN pip install --no-cache-dir -r requirements.txt               9.2s
 => [5/5] COPY src/ ./src/                                                 0.0s
 => exporting to image                                                     0.4s
 => => exporting layers                                                    0.4s
 => => writing image sha256:0ec84c4e4726990677ce582e1e2e9e1eb35dd5b315b49  0.0s
 => => naming to docker.io/library/week6-detector                          0.0s

## Run

Paste the command you used to start the container (should map a host port to the container's 8080):

docker run --rm -p 8080:8080 week6-detector

## Verify

Paste the exact `curl` commands and their JSON output for both endpoints,
run against the running container (not against `python src/app.py` directly
— the point is to prove the *container* works):

curl http://localhost:8080/health
{"status":"ok"}

curl -F "image=@data/fixtures/camera_A_daylight/000.jpg" http://localhost:8080/detect
{"count":5,"detections":[{"bbox":[124,4,41,25],"category_id":3,"id":0,"image_id":0,"score":0.98},{"bbox":[190,39,29,24],"category_id":10,"id":1,"image_id":0,"score":0.98},{"bbox":[67,80,28,14],"category_id":0,"id":2,"image_id":0,"score":0.98},{"bbox":[99,96,39,21],"category_id":7,"id":3,"image_id":0,"score":0.98},{"bbox":[139,96,3,11],"category_id":5,"id":4,"image_id":0,"score":0.98}]}
