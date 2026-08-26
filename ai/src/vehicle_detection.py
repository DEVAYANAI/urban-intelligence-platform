from ultralytics import YOLO

# Load the pretrained YOLO model
model = YOLO("yolo11n.pt")

# Run YOLO on our image
results = model("data/images/road.jpg", save=True)

# Vehicle counters
car_count = 0
motorcycle_count = 0
bus_count = 0
truck_count = 0

# Process the detection results
for result in results:

    # Go through every detected object
    for box in result.boxes:

        # Get the detected object's class ID
        class_id = int(box.cls[0])

        # Count the vehicles
        if class_id == 2:
            car_count += 1

        elif class_id == 3:
            motorcycle_count += 1

        elif class_id == 5:
            bus_count += 1

        elif class_id == 7:
            truck_count += 1


# Display the result
print()
print("========== TRAFFIC ANALYSIS ==========")
print("Cars        :", car_count)
print("Motorcycles :", motorcycle_count)
print("Buses       :", bus_count)
print("Trucks      :", truck_count)
print("======================================")