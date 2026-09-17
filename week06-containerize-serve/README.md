# Part 1: Flask Application (src/app.py)
Implemented three core functions/routes:

load_image_from_upload(file_storage): Reads incoming uploaded bytes from Werkzeug FileStorage, wraps them in an io.BytesIO buffer, opens the image using PIL and converts it to standard RGB format.

run_detection(image): Runs det.detect(image) using the mock detector and serializes the resulting object detections into a COCO-style JSON dictionary containing detection bounding boxes and confidence counts.

@app.post("/detect"): Endpoint that processes file uploads. Checks for the "image" key in request.files, returns a 400 Bad Request JSON error if missing and returns a 200 OK JSON detection response on success.

# Part 2: Containerization (Dockerfile)
Containerized the application using a lightweight base setup:

Base Image: python:3.11-slim (keeps build size small).

Dependencies: Installed requirements.txt using --no-cache-dir to prevent cached wheel bloating.

App Execution: Copies src/ directory into /app and executes CMD ["python", "src/app.py"] listening on port 8080.

# Testing Locally

First verified the app works locally by using pytest tests/ -q
and also by running src/app.py, and the given curl commands in README.pdf (in another terminal tab) 

health check: curl http://localhost:8080/health

bad request check: curl -X POST http://localhost:8080/detect

image detection test: curl -F "image=@data/fixtures/camera_A_daylight/000.jpg" http://localhost:8080/detect

# Testing with Docker

docker build -t week6-detector .

docker run --rm -p 8080:8080 week6-detector

curl http://localhost:8080/health

curl -F "image=@data/fixtures/camera_A_daylight/000.jpg" http://localhost:8080/detect

# Checking image size after it has been built in the previous step

docker images week6-detector