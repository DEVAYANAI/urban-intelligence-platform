from ultralytics import YOLO

# Load the pretrained YOLO model
model = YOLO("yolo11s.pt")

# Store unique vehicle IDs
vehicle_ids = set()

# Track vehicles in the video
results = model.track(
    source="data/videos/traffic1.mp4",
    conf=0.5,
    tracker="bytetrack.yaml",
    save=True,
    show=False,
    stream=True
)

# Process every frame
for result in results:

    # Check whether tracking IDs exist
    if result.boxes.id is not None:

        # Get the tracking IDs
        ids = result.boxes.id.int().cpu().tolist()

        # Add IDs to our set
        for vehicle_id in ids:
            vehicle_ids.add(vehicle_id)

# Display unique vehicle count
print()
print("========== VEHICLE TRACKING ==========")
print("Unique vehicles:", len(vehicle_ids))
print("======================================")