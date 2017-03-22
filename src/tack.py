import numpy as np
import cv2
import os
import time
import multiprocessing

from BeeUnique import FileVideoStream

data_dir = os.environ.get('DATA_DIR', None)
raw_dir = os.path.join(data_dir, 'beeunique/raw')
output_dir = os.path.join(data_dir, 'beeunique/output')

input_video_file = os.path.join(raw_dir, '2017-02-14_22-22-15.mp4')

cap = cv2.VideoCapture(input_video_file)
frame_counter = 0

rect_dims = 14

def segment_frame(counter_frame):
    gray_frame = cv2.cvtColor(counter_frame, cv2.COLOR_BGR2GRAY)
    smoothed_frame = cv2.GaussianBlur(gray_frame, (9, 9), 0)

    grad_x = cv2.Sobel(smoothed_frame, cv2.CV_16S, 1, 0, ksize=3, scale=1.5, delta=0, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(smoothed_frame, cv2.CV_16S, 0, 1, ksize=3, scale=1.5, delta=0, borderType=cv2.BORDER_DEFAULT)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    scharr = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    ret, thresh = cv2.threshold(scharr, 70, 255, 0)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13, 13))
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 100:
            centre, width_height, rotation = cv2.minAreaRect(cnt)
            x, y = int(centre[0]), int(centre[1])
            #print(x, y)
            if width_height[0] > 27 and abs(width_height[0] - width_height[1]) < 4:
                cv2.rectangle(frame, (int(centre[0]-width_height[0]), int(centre[1]-width_height[1])), (int(centre[0]+width_height[0]), int(centre[1]+width_height[1])), (0,255,0), 2)
                extract = smoothed_frame[y-rect_dims:y+rect_dims, x-rect_dims:x+rect_dims]

            else:
                cv2.rectangle(frame, (int(centre[0]-width_height[0]), int(centre[1]-width_height[1])), (int(centre[0]+width_height[0]), int(centre[1]+width_height[1])), (0,0,255), 2)

    return frame



while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break

    frame_contours = segment_frame(frame)
    frame_contours = cv2.resize(frame_contours, (1200, 720));

    cv2.imshow('frame', frame_contours)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
