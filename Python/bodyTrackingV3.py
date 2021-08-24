import cv2
import sys
import math

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

if __name__ == '__main__':

    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD',
                     'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[2]

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()

    # Read video
    video = cv2.VideoCapture(0)
    video.set(3,640)
    video.set(4,480)
    frameHeight = 480
    frameWidth = 640
    center = (640//2,480//2)
    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

    # Define an initial bounding box
    print(frame.shape)
    midHeight = int(frame.shape[1]/2)
    midWidth = int(frame.shape[0]/2)
    # top = (int(midWidth/4),int(midHeight/4))
    # bottom = 3*(int(3*midWidth/4),int(3*midHeight/4))
    x1 = int(3*midWidth/4)
    y1 = int(midHeight/4)
    x2 = int(6*midWidth/4)
    y2 = int(4*midHeight/4)
    bbox = (x1,y1,x2,y2)

    # Uncomment the line below to select a different bounding box
#     bbox = cv2.selectROI(frame, False)

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

    while True:
        # Read a new frame
        timer = cv2.getTickCount()
        ok, frame = video.read()
        if not ok:
            break

        # Start timer
        cv2.circle(frame,center,7,(255,0,255),-1)
        # Update tracker
        ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS)

        # Draw bounding box
        # ok = True
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            selectMid = ((p1[0]+p2[0])//2,(p1[1]+p2[1])//2)
            dist = math.sqrt((center[0]-selectMid[0])**2 + (center[1]-selectMid[1])**2) 
            distX = (center[0]-selectMid[0])
            distY = (center[1]-selectMid[1])
            print('Distance:- ',dist)
            cv2.circle(frame,selectMid,7,(0,255,0),-1)
            cv2.circle(frame,p1,4,(0,255,0),-1)
            cv2.circle(frame,p2,4,(0,255,0),-1)
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
            cv2.line(frame,center,selectMid,(0,0,255),5)
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (20, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

        # Display FPS on frame
        cv2.putText(frame, "Distance X: " + str(int(distX)), (150, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 10, 255), 2)
        cv2.putText(frame, "Distance Y: " + str(int(distY)), (400, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 10, 255), 2)


        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        cv2.putText(frame, "FPS : " + str(int(fps)), (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
        # Display result
        cv2.imshow("Tracking", frame)
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == ord('q'):
            break
video.release()
cv2.destroyAllWindows()
