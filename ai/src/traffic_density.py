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

    # YOLO COCO classes:
    # 0 = person
    # 2 = car
    # 3 = motorcycle
    # 5 = bus
    # 7 = truck

    results = model.track(
        source=video_path,
        conf=0.5,
        tracker="bytetrack.yaml",
        stream=True,
        save=True,
        classes=[0, 2, 3, 5, 7]
    )


    # ==========================================
    # CROWD SETTINGS
    # ==========================================

    CROWD_THRESHOLD = 10
    MIN_CROWDED_FRAMES = 10


    # ==========================================
    # MAXIMUM COUNTS
    # ==========================================

    max_people = 0
    max_cars = 0
    max_motorcycles = 0
    max_buses = 0
    max_trucks = 0


    # ==========================================
    # INTERNAL FRAME STATISTICS
    # ==========================================

    total_frames = 0
    crowded_frames = 0


    # ==========================================
    # PROCESS EVERY FRAME
    # ==========================================

    for result in results:

        total_frames += 1

        people = 0
        cars = 0
        motorcycles = 0
        buses = 0
        trucks = 0


        # Read detected object classes

        if result.boxes is not None:

            class_ids = (
                result.boxes.cls
                .int()
                .cpu()
                .tolist()
            )

            for class_id in class_ids:

                if class_id == 0:
                    people += 1

                elif class_id == 2:
                    cars += 1

                elif class_id == 3:
                    motorcycles += 1

                elif class_id == 5:
                    buses += 1

                elif class_id == 7:
                    trucks += 1


        # ==========================================
        # CROWD DETECTION
        # ==========================================

        max_people = max(max_people, people)

        if people >= CROWD_THRESHOLD:
            crowded_frames += 1


        # ==========================================
        # VEHICLE COUNTS
        # ==========================================

        max_cars = max(max_cars, cars)

        max_motorcycles = max(
            max_motorcycles,
            motorcycles
        )

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
    # INTERNAL CROWD CONSISTENCY CALCULATION
    # ==========================================

    crowd_percentage = 0.0

    if total_frames > 0:

        crowd_percentage = (
            crowded_frames / total_frames
        ) * 100


    # ==========================================
    # ROAD EVENT DETECTION
    # ==========================================

    if crowded_frames >= MIN_CROWDED_FRAMES:

        road_event_detected = True

        road_event_type = "LARGE GATHERING"

        # Used internally only
        road_event_confidence = round(
            crowd_percentage / 100,
            2
        )

        alert_message = (
            "Large gathering detected. "
            "Consider an alternative route."
        )

    else:

        road_event_detected = False

        road_event_type = None

        road_event_confidence = 0.0

        alert_message = (
            "No consistent large gathering detected. "
            "Route is currently clear."
        )


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

        "traffic_level": traffic_level,

        # Road event data

        "road_event_detected": road_event_detected,

        "road_event_type": road_event_type,

        "road_event_confidence": road_event_confidence,

        "alert_message": alert_message
    }


    # ==========================================
    # SAVE JSON
    # ==========================================

   # ==========================================
# SAVE JSON
# ==========================================

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    output_path = os.path.join(
        BASE_DIR,
        "traffic_event.json"
    )

    with open(output_path, "w") as file:
        json.dump(
            event,
            file,
            indent=4
        )
    # ==========================================
    # FINAL OUTPUT
    # ==========================================

    print()
    print("AI Status : COMPLETED")
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

    print("ROAD EVENT ANALYSIS")
    print("--------------------------------------")

    print("Road event detected :", road_event_detected)
    print("Road event type     :", road_event_type)
    print("Alert message       :", alert_message)

    print("--------------------------------------")

    print("JSON saved to:")
    print(output_path)

    print()

    print("Annotated video saved under:")
    print("runs/detect/")

    print("======================================")


    # ==========================================
    # RETURN RESULT TO BACKEND
    # ==========================================

    return event


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    analyze_video(
        "data/videos/traffic1.mp4"
    )