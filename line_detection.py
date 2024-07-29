import cv2 as cv
import numpy as np
import math

def apply_thresholds(gray, thresholds, adaptiveSettings):
    mask1 = cv.bitwise_not(cv.threshold(gray, thresholds[0], thresholds[1], cv.THRESH_OTSU)[1])
    mask = cv.bitwise_not(cv.adaptiveThreshold(gray, thresholds[0], cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, adaptiveSettings[0], adaptiveSettings[1]))
    mask = cv.bitwise_and(mask, mask1)
    mask = cv.inRange(mask, 200, 255)
    return mask


def apply_canny(mask):
    return cv.Canny(mask, 100, 125, apertureSize=7, L2gradient=True)


def get_lines(can):
    return cv.HoughLinesP(
        can,
        1,
        np.pi/90,
        100,
        minLineLength=10,
        maxLineGap=10
    )

def draw_line(img_lines, line):
    x1, y1, x2, y2, angle = line
    cv.line(img_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv.putText(img_lines, " Line "+str(lines_.index(line)), (int((x2+x1)/2), int((y2+y1)/2)), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv.LINE_AA)
    cv.circle(img_lines, (x1, y1), 5, (255, 0, 0), -1)
    cv.putText(img_lines, str(x1)+", "+str(y1), (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv.LINE_AA)
    cv.circle(img_lines, (x2, y2), 5, (255, 255, 0), -1)
    cv.putText(img_lines, str(x2) + ", " + str(y2), (x2, y2), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv.LINE_AA)


img = cv.imread("technical_drawing_sample0.png")
thr = apply_canny(img)

lines = get_lines(thr)
lines_ = []


if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        lines_.append([x1, y1, x2, y2, -90+(math.atan2(y2 - y1, x2 - x1) * 180 / np.pi)])

for line in lines_:
        draw_line(img, line)

cv.imshow("threshold", img)
cv.waitKey(0)
