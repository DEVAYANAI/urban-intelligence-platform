from ultralytics import YOLO
import json
from datetime import datetime
import os


# ==========================================
# LOAD MODEL
# ==========================================

model = YOLO("yolo11s.pt")


# ==========================================
# ANALYZE VIDEO
# ==========================================

def analyze_video(video_path):

    print()
    print("======================================")
    print("       AI TRAFFIC ANALYSIS")
    print("======================================")
    print("Input video :", video_path)
    print("AI Status   : RUNNING...")
    print()

    results = model.track(
        source=video_path,
        conf=0.5,
        tracker="bytetrack.yaml",
        stream=True,
        save=True,
        classes=[2, 3, 5, 7]
    )

    # ==========================================
    # MAXIMUM VEHICLES
    # ==========================================

    max_cars = 0
    max_motorcycles = 0
    max_buses = 0
    max_trucks = 0

    # ==========================================
    # PROCESS EVERY FRAME
    # ==========================================

    for result in results:

        cars = 0
        motorcycles = 0
        buses = 0
        trucks = 0

        if result.boxes.id is not None:

            class_ids = (
                result.boxes.cls
                .int()
                .cpu()
                .tolist()
            )

            for class_id in class_ids:

                if class_id == 2:
                    cars += 1

                elif class_id == 3:
                    motorcycles += 1

                elif class_id == 5:
                    buses += 1

                elif class_id == 7:
                    trucks += 1

        # Store maximum number seen in any frame

        max_cars = max(max_cars, cars)
        max_motorcycles = max(max_motorcycles, motorcycles)
        max_buses = max(max_buses, buses)
        max_trucks = max(max_trucks, trucks)

    # ==========================================
    # TOTAL VEHICLES
    # ==========================================

    max_total = (
        max_cars
        + max_motorcycles
        + max_buses
        + max_trucks
    )

    # ==========================================
    # TRAFFIC LEVEL
    # ==========================================

    if max_total <= 5:
        traffic_level = "LOW"

    elif max_total <= 10:
        traffic_level = "MEDIUM"

    else:
        traffic_level = "HIGH"

    # ==========================================
    # CREATE JSON
    # ==========================================

    event = {
        "event_type": "traffic_density",
        "timestamp": datetime.now().isoformat(),
        "cars": max_cars,
        "motorcycles": max_motorcycles,
        "buses": max_buses,
        "trucks": max_trucks,
        "total_vehicles": max_total,
        "traffic_level": traffic_level
    }

    # ==========================================
    # SAVE JSON
    # ==========================================

    output_path = "ai/src/traffic_event.json"

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    with open(output_path, "w") as file:
        json.dump(
            event,
            file,
            indent=4
        )

    # ==========================================
    # FINAL RESULT
    # ==========================================

    print()
    print("AI Status   : COMPLETED")
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
    print("--------------------------------------")
    print("JSON saved to:")
    print(output_path)
    print()
    print("Annotated video saved under:")
    print("runs/detect/")
    print("======================================")

    return event

if __name__ == "__main__":
    analyze_video("data/videos/traffic1.mp4")