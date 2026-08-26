from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11s.pt")

# Video
video_path = "data/videos/traffic1.mp4"

# Vehicle classes
vehicle_classes = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}

# Track the video
results = model.track(
    source=video_path,
    conf=0.5,
    tracker="bytetrack.yaml",
    stream=True
)

# Keep track of the maximum vehicles visible
max_cars = 0
max_motorcycles = 0
max_buses = 0
max_trucks = 0

# Process every frame
for result in results:

    cars = 0
    motorcycles = 0
    buses = 0
    trucks = 0

    if result.boxes.id is not None:

        class_ids = result.boxes.cls.int().cpu().tolist()

        for class_id in class_ids:

            if class_id == 2:
                cars += 1

            elif class_id == 3:
                motorcycles += 1

            elif class_id == 5:
                buses += 1

            elif class_id == 7:
                trucks += 1

    # Save the highest number observed
    max_cars = max(max_cars, cars)
    max_motorcycles = max(max_motorcycles, motorcycles)
    max_buses = max(max_buses, buses)
    max_trucks = max(max_trucks, trucks)


# Maximum traffic observed
max_total = (
    max_cars
    + max_motorcycles
    + max_buses
    + max_trucks
)

# Determine traffic level
if max_total <= 5:
    traffic_level = "LOW"

elif max_total <= 10:
    traffic_level = "MEDIUM"

else:
    traffic_level = "HIGH"


# Display result
print()
print("======================================")
print("       TRAFFIC DENSITY RESULT")
print("======================================")
print("Maximum cars        :", max_cars)
print("Maximum motorcycles :", max_motorcycles)
print("Maximum buses       :", max_buses)
print("Maximum trucks      :", max_trucks)
print("--------------------------------------")
print("Maximum vehicles    :", max_total)
print("Traffic level       :", traffic_level)
print("======================================")