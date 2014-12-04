import cv2
import numpy as np

def apply_hist_mask(frame, hist):
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	dst = cv2.calcBackProject([hsv], [0,1], hist, [0,180,0,256], 1)

	disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
	cv2.filter2D(dst, -1, disc, dst)
		
	ret, thresh = cv2.threshold(dst, 100, 255, 0)
	thresh = cv2.merge((thresh,thresh, thresh))
	
	cv2.GaussianBlur(dst, (3,3), 0, dst)
	
	res = cv2.bitwise_and(frame, thresh)
	return res

def contours(frame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(gray, 0, 255, 0)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)	
	return contours

def max_contour(contours):
	max_i = 0
	max_area = 0
	
	for i in range(len(contours)):
		cnt = contours[i]
		area = cv2.contourArea(cnt)
		if area > max_area:
			max_area = area
			max_i = i

	contour = contours[max_i]
	return contour

def hull(contour):
	hull = cv2.convexHull(contour)
	return hull

def defects(contour):
	hull = cv2.convexHull(contour, returnPoints=False)
	defects = cv2.convexityDefects(contour, hull)	
	return defects

def centroid(contour):
	moments = cv2.moments(contour)
	cx = int(moments['m10']/moments['m00'])
	cy = int(moments['m01']/moments['m00'])
	return (cx,cy)	

def contour_interior(frame, contour):
	rect = cv2.minAreaRect(contour)
	box = cv2.cv.BoxPoints(rect)
	box = np.int0(box)

	rows,cols,_ = frame.shape
	mask = np.zeros((rows,cols), dtype=np.float)
	for i in xrange(rows):
		for j in xrange(cols):
			mask.itemset((i,j), cv2.pointPolygonTest(box, (j,i), False))

	mask = np.int0(mask)
	mask[mask < 0] = 0
	mask[mask > 0] = 255
	mask = np.array(mask, dtype=frame.dtype)
	mask = cv2.merge((mask, mask, mask))
	
	contour_interior = cv2.bitwise_and(frame, mask)
	return contour_interior			

def gray_threshold(frame, threshold_value):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray, threshold_value, 255, 0)
	return thresh