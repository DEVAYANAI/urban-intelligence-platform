from ultralytics import YOLO
from pathlib import Path


# ==========================================
# 1. LOAD MODEL
# ==========================================

model = YOLO("yolo11s.pt")


# ==========================================
# 2. IMAGE PATH
# ==========================================

image_path = "data/images/road2.jpg"


# ==========================================
# 3. RUN YOLO
# ==========================================

print()
print("======================================")
print("       AI VEHICLE DETECTION")
print("======================================")
print("Input image :", image_path)
print("AI Status   : RUNNING...")
print()


results = model(
    image_path,
    conf=0.5,
    classes=[2, 3, 5, 7],
    save=True
)


# ==========================================
# 4. COUNT VEHICLES
# ==========================================

cars = 0
motorcycles = 0
buses = 0
trucks = 0


for result in results:

    if result.boxes is not None:

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


# ==========================================
# 5. TOTAL
# ==========================================

total = cars + motorcycles + buses + trucks


# ==========================================
# 6. DISPLAY RESULT
# ==========================================

print("AI Status   : COMPLETED")
print()
print("======================================")
print("          DETECTION RESULT")
print("======================================")
print("Cars        :", cars)
print("Motorcycles :", motorcycles)
print("Buses       :", buses)
print("Trucks      :", trucks)
print("--------------------------------------")
print("Total       :", total)
print("======================================")


# ==========================================
# 7. OUTPUT LOCATION
# ==========================================

output_folder = Path("runs/detect")

folders = sorted(
    output_folder.glob("predict*"),
    key=lambda x: x.stat().st_mtime,
    reverse=True
)

if folders:
    latest_folder = folders[0]
    print()
    print("Annotated image saved in:")
    print(latest_folder)

print()
print("======================================")
print("       IMAGE TEST FINISHED")
print("======================================")