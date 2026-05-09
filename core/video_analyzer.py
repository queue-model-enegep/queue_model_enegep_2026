"""
Executing this script will collect the data for both the
heatmap coordinates and for the occupancy tracker of the 
service zone.

Only call "save_data()" if you are certain about the results.
"""



import random
import shelve

import cv2
from ultralytics import YOLO
import numpy as np
import pandas as pd



# Instantiating the model.
model = YOLO('yolov8x.pt')
# Defining the video to analyze.
cap = cv2.VideoCapture('data/service_area_video.mp4')


# Initializing the data storage.
occupancy_list: list[int] = []
heatmap_positions_list: list[dict[str, int]] = [] 

# Loading the region of interest.
with shelve.open('data/serialized_data') as db:
    region_of_interest = db['region_of_interest']

# Formatting the region of interest.
region_array = np.array(region_of_interest, np.int32).reshape((-1, 1, 2))

fps = cap.get(cv2.CAP_PROP_FPS)
total_frames_of_the_video = cap.get(cv2.CAP_PROP_FRAME_COUNT)
T = total_frames_of_the_video / fps

# Determining the period for collecting data.
snapshot_interval = 15
total_counts = int(T / snapshot_interval) 
sampling_frames = sorted(random.sample(
    range(total_counts),
    min(10, total_counts)
))  

for snapshot in range(total_counts):
    frame_index = int(snapshot * snapshot_interval * fps)

    # Set the video capture property to jump to the exact frame index.
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    
    rectangle, frame = cap.read()
    if not rectangle:
        break

    results = model(
        frame, 
        imgsz=1920,      
        conf=0.15,       
        iou=0.7,         
        augment=True,    
        classes=[0],     
        verbose=False
    )
    people_count: int = 0
    show_debugging = snapshot in sampling_frames
    
    if show_debugging:
        # Draw the ROI polygon. 'True' closes the shape, drawing a line from 
        # the last to the first vertex.
        cv2.polylines(frame, [region_array], True, (255, 255, 0), 2)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2) 
            # Perform a point-in-polygon test. 'False' returns +1 (inside), -1 (outside), 
            # or 0 (on edge), rather than the exact distance.
            if cv2.pointPolygonTest(region_array, (cx, cy), False) >= 0:
                people_count += 1
                
                heatmap_positions_list.append({
                    'Snapshot': snapshot,
                    'x': cx,
                    'y': cy
                })

                if show_debugging:
                    # Draw a rectangle using the top-left (x1, y1) and 
                    # bottom-right (x2, y2) coordinates.
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    print(f"Snapshot {snapshot}: {people_count} people")
    occupancy_list.append(people_count)


    if show_debugging:
        cv2.putText(frame, f"Snapshot: {snapshot} | Count: {people_count}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        window_name = f"Debug Snapshot {snapshot}"
        # The WINDOW_NORMAL flag allows the OS GUI window to be freely resized, 
        # overriding the default WINDOW_AUTOSIZE.
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL) 
        cv2.resizeWindow(window_name, 1280, 720)
        cv2.imshow(window_name, frame)
        # Halts the current thread indefinitely until a keyboard interrupt event is detected in the active window.
        cv2.waitKey(0)
        cv2.destroyWindow(window_name)

# Finishing execution.
cap.release()
cv2.destroyAllWindows()

# Formatting the data.
df_occupancy = pd.DataFrame(
    data={'C_i': occupancy_list},
    index=range(len(occupancy_list))
)
df_occupancy.index.name = 'Snapshot'

df_heatmap_positions = pd.DataFrame(data=heatmap_positions_list)


# Caution!
def save_data() -> None:
    df_occupancy.to_csv('data/occupancy.csv')
    df_heatmap_positions.to_csv('data/heatmap_positions.csv', index=False)


if __name__ == '__main__':
    ...