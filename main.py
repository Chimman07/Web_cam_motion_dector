import glob
import os
import cv2
import time
import Emailing


camera = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None

count = 0

status_list = []


def cleaner():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("cleaning images finished")


while True:
    status = 0
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

        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)  # to get the images of object in images folder
            count = count + 1

            all_images = glob.glob("images/*.png")  # making the list of all images
            index = int(len(all_images) / 2)  # to get the most middlest image from the folder
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        Emailing.send_email(image_with_object)

    print(status_list)

    cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cleaner()

camera.release()
