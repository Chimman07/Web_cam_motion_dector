import cv2
import time

camera = cv2.VideoCapture(0)
time.sleep(1)
first_frame = None
while True:
    check, frame = camera.read()
    # cv2.imshow("my video", frame)  # shows the frame as it is
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grey_frame_gau = cv2.GaussianBlur(grey_frame, (15, 15), 0)
    # cv2.imshow("my video", grey_frame_gau)  # made the frame in black and white and blured it

    if first_frame is None:
        first_frame = grey_frame_gau  # saved the first frame

    delta_frame = cv2.absdiff(first_frame, grey_frame_gau)  # comparing the first_frame with blured to get difference
    # cv2.imshow("my video", delta_frame)
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]  # now its just b/w
    # cv2.imshow("my video", thresh_frame)

    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)  # even more detailed b/w
    # cv2.imshow("video", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # drawing contours
    for contour in contours:
        if cv2.contourArea(contour) < 5000:  # if object size in frame is less than 5000 then it won't show rectangle
            continue
        x, y, w, h = cv2.boundingRect(contour)  # if it's larger than 5000 then giving the rectangle to the object
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    cv2.imshow("video", frame)


    key = cv2.waitKey(1)
    if key == ord("q"):
        break

camera.release()
