import cv2
import numpy as np


# we're using BGR format
class Channel():
    RED = 2
    GREEN = 1
    BLUE = 0

# indices for image arrays
ROW = 1
COL = 0
# indices for points
PT_X = 0
PT_Y = 1


img = cv2.imread('ball.jpg')

# create mask for orange pixels
# indices are img[row, col, channel]
# TODO find better definition of orange?
mask1 = img[:, :, Channel.RED] > 1.5 * img[:, :, Channel.GREEN]
mask2 = img[:, :, Channel.RED] < 3.0 * img[:, :, Channel.GREEN]
mask3 = img[:, :, Channel.GREEN] > 1.5 * img[:, :, Channel.BLUE]
mask = mask1 & mask2 & mask3

orange = np.asarray(mask, dtype='uint8')

# remove stray pixels
# see https://docs.opencv.org/3.4/db/df6/tutorial_erosion_dilatation.html
kernel = np.ones((5, 5), dtype='uint8')
orange = cv2.erode(orange, kernel=kernel)
orange = cv2.dilate(orange, kernel=kernel)

# find contours of connected areas
_, contours, _ = cv2.findContours(orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# contours is a list where each contour is a numpy array of points
# points are in the form [[x, y]]

# lists of parameters of bounding boxes for the contours
x = [] # lowest x value
y = [] # lowest y value
w = [] # width
h = [] # height
for contour in contours:
    x1 = np.min(contour[:, 0, PT_X])
    y1 = np.min(contour[:, 0, PT_Y])
    x2 = np.max(contour[:, 0, PT_X])
    y2 = np.max(contour[:, 0, PT_Y])
    x.append(x1)
    y.append(y1)
    w.append(x2 - x1)
    h.append(y2 - y1)

if len(contours) > 0:
    # choose contour with largest bounding box
    area = np.multiply(w, h)
    i_max = np.argmax(area)
    width = w[i_max]
    height = h[i_max]

    # draw bounding box (blue)
    cv2.rectangle(
        img,
        (x[i_max], y[i_max]),
        (x[i_max] + width, y[i_max] + height),
        color=(255, 0, 0),
        thickness=1)

    # determine radius and centre range of ball and ensure that the circle is completely 
    # contained in the image
    r = int(max(width, height)/2)
    xmin = max(x[i_max] + min(r, width-r), r)
    xmax = min(x[i_max] + max(r, width-r), orange.shape[ROW] - r)
    ymin = max(y[i_max] + min(r, height-r), r)
    ymax = min(y[i_max] + max(r, height-r), orange.shape[COL] - r)

    # find circle containing largest number of orange pixels
    # simplified method: look in rectangle, not circular mask
    # TODO change if needed (draw filled circle, & with orange, then as before)
    area_max = 0
    centre = (0, 0)
    for xmid in np.arange(xmin, xmax+1):
        for ymid in np.arange(ymin, ymax+1):
            # in orange: 1 = pixel is orange, 0 = pixel is not orange
            area = cv2.countNonZero(orange[ymid-r:ymid+r, xmid-r:xmid+r])
            if area > area_max:
                area_max = area
                centre = (xmid, ymid)

    # draw circle (green)
    cv2.circle(
        img,
        centre,
        radius=r,
        color=(0, 255, 0),
        thickness=1)
    # draw centre (black)
    cv2.circle(
        img,
        centre,
        radius=1,
        color=(0, 0, 0),
        thickness=2)

cv2.imshow('orange ball', img)
cv2.waitKey(0)
