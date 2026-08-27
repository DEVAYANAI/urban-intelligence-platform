from ultralytics import YOLO

# -----------------------------
# 1. Load YOLO model
# -----------------------------
model = YOLO("yolo11s.pt")

# -----------------------------
# 2. Video path
# -----------------------------
video_path = "data/videos/traffic1.mp4"

# -----------------------------
# 3. Counting line
# -----------------------------
LINE_Y = 2600

# -----------------------------
# 4. Vehicle classes
# -----------------------------
vehicle_classes = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}

# -----------------------------
# 5. Store vehicles already counted
# -----------------------------
counted_ids = set()

car_count = 0
motorcycle_count = 0
bus_count = 0
truck_count = 0

# -----------------------------
# 6. Start tracking
# -----------------------------
results = model.track(
    source=video_path,
    conf=0.5,
    tracker="bytetrack.yaml",
    stream=True
)

# -----------------------------
# 7. Process every frame
# -----------------------------
for result in results:

    if result.boxes.id is None:
        continue

    boxes = result.boxes

    tracking_ids = boxes.id.int().cpu().tolist()
    class_ids = boxes.cls.int().cpu().tolist()

    for track_id, class_id, box in zip(
        tracking_ids,
        class_ids,
        boxes.xyxy
    ):

        # Ignore objects that aren't vehicles
        if class_id not in vehicle_classes:
            continue

        # Bounding box coordinates
        x1, y1, x2, y2 = box.tolist()

        # Calculate center of vehicle
        center_y = (y1 + y2) / 2

        # Check whether vehicle crossed the line
        if center_y > LINE_Y:

            # Count this vehicle only once
            if track_id not in counted_ids:

                counted_ids.add(track_id)

                vehicle_type = vehicle_classes[class_id]

                if vehicle_type == "car":
                    car_count += 1

                elif vehicle_type == "motorcycle":
                    motorcycle_count += 1

                elif vehicle_type == "bus":
                    bus_count += 1

                elif vehicle_type == "truck":
                    truck_count += 1

# -----------------------------
# 8. Display final result
# -----------------------------
print()
print("====================================")
print("       TRAFFIC COUNT RESULT")
print("====================================")
print("Cars        :", car_count)
print("Motorcycles :", motorcycle_count)
print("Buses       :", bus_count)
print("Trucks      :", truck_count)
print("------------------------------------")
print("Total       :", car_count + motorcycle_count + bus_count + truck_count)
print("====================================")