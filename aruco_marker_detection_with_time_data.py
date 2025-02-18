import cv2
import cv2.aruco as aruco
import time

# Define the dictionary of markers you are using.
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

# Define the parameters for the ArUco marker detection.
parameters = aruco.DetectorParameters_create()


# Start the webcam feed
cap = cv2.VideoCapture(0)  # 'C:\\Users\\ulubi\\Desktop\\pilot_test_1_data.mp4'

# Variables to keep track of marker visibility times and the current marker ID
marker_detected_at = None
visibility_intervals = []
current_marker_id = None  # Variable to store the marker ID when detected

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the markers in the image
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # If any markers were found, draw them on the frame
    if ids is not None:
        frame = aruco.drawDetectedMarkers(frame, corners, ids)
        if marker_detected_at is None:  # If the marker was not detected before
            marker_detected_at = time.time()
            current_marker_id = ids[0][0]  # Store the marker ID when detected
    else:
        if marker_detected_at is not None:  # If the marker was detected earlier, but not now
            marker_end_time = time.time()
            visibility_intervals.append((marker_detected_at, marker_end_time, current_marker_id))
            marker_detected_at = None
            current_marker_id = None

    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.moveWindow('frame', 100, 100)  # This moves the window to (100, 100) coordinates

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Handle the case when the marker is still visible when the video feed ends
if marker_detected_at is not None:
    marker_end_time = time.time()
    visibility_intervals.append((marker_detected_at, marker_end_time, current_marker_id))

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# Write the visibility intervals to a file
with open('marker_time_data_pilot_test_10.txt', 'w') as file:
    for start, end, marker_id in visibility_intervals:
        duration = round(end - start, 3)
        file.write(f"ID {marker_id} Duration: {duration} seconds {time.ctime(start)} to {time.ctime(end)} \n\n")
