import cv2
import numpy as np

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares


 
# Camera 0 is the integrated web cam on my netbook
camera_port = 0
 
#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 4
 
# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
camera = cv2.VideoCapture(camera_port)
 
# Captures a single image from the camera and returns it in PIL format
def get_image():
 # read is the easiest way to get a full image out of a VideoCapture object.
 retval, im = camera.read()
 return im

'''NECESSARY TO THROW AWAY FIRST FEW FRAMES!! OTHERWISE, WON'T WORK.
FIRST FEW QUERIES DON'T ACTUALLY RETURN ANYTHING
'''
# Ramp the camera - these frames will be discarded and are only used to allow v4l2
# to adjust light levels, if necessary
list = []

for i in xrange(ramp_frames):
 temp = get_image()
 print type(temp)
print("Adjusting...")


#operations on the image
#===========================#

edgeThresh = 1;
lowThreshold = 33;
max_lowThreshold = 100;
ratio = 3;
kernel_size = 3;

while True:

    # Take the actual image we want to keep
    camera_capture = get_image()
    gray = cv2.cvtColor( camera_capture, cv2.cv.CV_BGR2GRAY )
    detected_edges = cv2.Canny( gray, lowThreshold, lowThreshold*ratio, kernel_size)

    #out = cv2.flip(camera_capture, -1)

    squares = find_squares(detected_edges)
    cv2.drawContours( detected_edges, squares, -1, (0, 255, 0), 3 )

    #lines = cv2.HoughLines( detected_edges, 1, cv2.cv.CV_PI/180, 50, 0, 0 )
    #print type(lines)
    #print lines

    cv2.imshow('squares', detected_edges)
    
    if cv2.cv.WaitKey(10) == 27:
        break
cv2.cv.DestroyAllWindows()

#===========================#
        
file = "test_image.png"
# A nice feature of the imwrite method is that it will automatically choose the
# correct format based on the file extension you provide. Convenient!
#cv2.imwrite(file, detected_edges)
 
# You'll want to release the camera, otherwise you won't be able to create a new
# capture object until your script exits
del(camera)

