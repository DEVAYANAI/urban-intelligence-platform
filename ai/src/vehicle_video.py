from ultralytics import YOLO

# Load the pretrained YOLO model
model = YOLO("yolo11n.pt")

# Run YOLO on the video
results = model.predict(
    source="data/videos/traffic1.mp4",
    conf=0.5,
    save=True
)

print("Video detection completed!")