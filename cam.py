import sys
import cv2
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
import energy

weights = hf_hub_download("Ank0805/waste-classification", "waste classification modle.pt")
model = YOLO(weights)
src = sys.argv[1] if len(sys.argv) > 1 else "0"
cap = cv2.VideoCapture(int(src) if src.isdigit() else src)

while True:
    ok, frame = cap.read()
    if not ok:
        break
    res = model.predict(frame, conf=0.25, imgsz=640, verbose=False)[0]
    img = res.plot()
    for box in res.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        mass, mj = energy.estimate(int(box.cls[0]), x2 - x1, y2 - y1)
        cv2.putText(img, f"{mass * 1000:.0f} g, {mj:.2f} MJ", (int(x1), int(y2) + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.imshow("waste", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
