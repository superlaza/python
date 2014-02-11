import cv2
import cv
import math
import numpy as np
from scipy.cluster.vq import kmeans

def acceptLinePair(line1, line2):
    minTheta = (cv2.cv.CV_PI)/32
    minThetaDiff = 3*(cv2.cv.CV_PI)/8
    maxThetaDiff = 5*(cv2.cv.CV_PI)/8
    theta1 = line1[1]
    theta2 = line2[1]

    if (theta1 < minTheta):
        theta1 += cv2.cv.CV_PI #deals with 0 and 180 ambiguity
    if (theta2 < minTheta):
        theta2 += cv2.cv.CV_PI #deals with 0 and 180 ambiguity

    thetaDiff = abs(theta1-theta2)
    return thetaDiff > minThetaDiff and thetaDiff < maxThetaDiff

def computeIntersect(line1, line2):
    [l1p1, l1p2] = lineToPointPair(line1)
    [l2p1, l2p2] = lineToPointPair(line2)
    [x1,y1] = l1p1
    [x2,y2] = l1p2
    [x3,y3] = l2p1
    [x4,y4] = l2p2

    denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    intersect = [((x1*y2-y1*x2)*(x3-x4)
               -(x1-x2)*(x3*y4-y3*x4))/denom,
               ((x1*y2-y1*x2)*(y3-y4)
                -(y1-y2)*(x3*y4-y3*x4))/denom]

    return intersect

def lineToPointPair(line):

    r = line[0]
    t = line[1]
    cost = math.cos(t)
    sint = math.sin(t)
    x0 = r*cost
    y0 = r*sint
    alpha = 1000

    points = []
    
    points.append([x0+alpha*(-sint), y0+alpha*cost])
    points.append([x0-alpha*(-sint), y0-alpha*cost])

    return points

def drawIntersection(detectedLines, image):
    #compute the intersection from the lines detected...
        intersections = []
        for i in range(0,detectedLines.size/2):
            for j in range(i,detectedLines.size/2):
                line1 = detectedLines[i]
                line2 = detectedLines[j]
                if(acceptLinePair(line1, line2)):
                    intersection = computeIntersect(line1,line2)
                    intersections.append(intersection)
        '''
        print intersections[0]
        max_x = 0
        min_x = intersections[0][0]
        max_y = 0
        min_y = intersections[0][1]
        sumx = 0
        sumy = 0
        '''
        if len(intersections)>0:
            for i in range(0,len(intersections)):
                #print "Intersection is "+str(intersections[i][0])+", "+str(intersections[i][1])
                p_i = (int(round(intersections[i][0])),int(round(intersections[i][1])))
                '''
                sumx += p_i[0]
                sumy += p_i[1]
                if(i%1000==0):
                    print i
                if p_i[0] > max_x:
                    max_x=p_i[0]
                if p_i[1] > max_y:
                    max_y=p_i[1]
                if p_i[0] < min_x:
                    min_x=p_i[0]
                if p_i[1] < min_y:
                    min_y=p_i[1]
                '''
                #cv2.circle(image, p_i , 1, (0,255,0), 3)
        '''
        intersections2 = []
        res = kmeans(detectedLines,4)[0]
        for i in range(0,res.size/2):
            for j in range(i,res.size/2):
                line1 = res[i]
                line2 = res[j]
                if(acceptLinePair(line1, line2)):
                    intersection = computeIntersect(line1,line2)
                    intersections2.append(intersection)
        for i in range(0,len(intersections2)):
            p_i = (int(round(intersections2[i][0])),int(round(intersections2[i][1])))
            cv2.circle(image, p_i , 1, (0,255,0), 3)
        '''
            
        '''
        print max_x, min_x, max_y, min_y
        print sumx/len(intersections)
        print sumy/len(intersections)
        '''
    

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
for i in xrange(ramp_frames):
 temp = get_image()
 print temp == None
 print type(temp)
print("Adjusting...")

while True:
    #im = cv2.imread("test.jpg")
    im = get_image()
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    reval, thresh = cv2.threshold(gray, 200.0, 255.0, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    edges = cv2.Canny(thresh, 140.0, 240.0,2)
    cv2.imshow("ooreners", edges);
    corners = cv2.goodFeaturesToTrack(edges,25,0.01,10)
    corners = np.int0(corners)

    for i in corners:
        x,y = i.ravel()
        cv2.circle(im,(x,y),3,255,-1)
    
        
    cv2.imshow("oorners", im);
    #cv2.imwrite("corners.png", im)
    if cv2.cv.WaitKey(10) == 27:
        break
cv2.cv.DestroyAllWindows()
#cv2.cv.WaitKey();
