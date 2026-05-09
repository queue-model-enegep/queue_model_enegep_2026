"""
In order to save the region of interest for it ot base the video analysis,
call the function "serialize_roi_coordinates" in the if __name__ == '__main__' block.
"""



import pickle
from typing import Any

import cv2



VIDEO_PATH = 'data/service_area_video.mp4'
DISPLAY_WIDTH = 1280 

region_of_interest: list[tuple[int, int]] = []

# Function for 
def click_event(event: int, x: int, y: int, flags: int, param: Any) -> None:
    if event == cv2.EVENT_LBUTTONDOWN:
        real_x = int(x / scale_factor)
        real_y = int(y / scale_factor)

        coordinates: tuple[int, int] = (real_x, real_y)

        print(f'Point selected: {coordinates}')
        
        region_of_interest.append(coordinates)
        
        # Marking the Region of Interest while selecting it.
        cv2.circle(img_display, (x, y), 5, (0, 255, 255), -1)
        if len(display_points) > 0:
            cv2.line(img_display, display_points[-1], (x, y), (0, 255, 255), 2)
        
        image_points: tuple[int, int] = (x, y)

        display_points.append(image_points)

        # Message to leave the ROI selection.
        cv2.imshow('Image - Press Q to Quit', img_display)


cap = cv2.VideoCapture(VIDEO_PATH)
ret, frame = cap.read()
cap.release()

if ret:
    # Adjusting the image.
    height, width = frame.shape[:2]
    scale_factor = DISPLAY_WIDTH / width
    new_height = int(height * scale_factor)
    img_display = cv2.resize(frame, (DISPLAY_WIDTH, new_height))
    
    display_points: list[tuple[int, int]] = []

    cv2.imshow('Image - Press Q to Quit', img_display)
    cv2.setMouseCallback('Image - Press Q to Quit', click_event)

    # Executing the exit from the ROI selection.
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
else:
    print("Error reading video file.")


# Only call this function if you are absolutely certain about the region you selected!
def serialize_roi_coordinates() -> None:
    with open('data/serialized_data.pckl', 'wb') as stream:
        pickle.dump(region_of_interest, stream)



if __name__ == '__main__':
    ...