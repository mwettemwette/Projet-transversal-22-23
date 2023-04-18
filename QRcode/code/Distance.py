# le code de base est trouvable à l'adresse https://github.com/akpythonyt/AKpythoncodes
import cv2
from pyzbar import pyzbar
import math
import numpy as np

def fin(data):
    nmb1 = ""
    nmb2 = ""
    a = True
    for i in range(len(data)):
        if data[i]!=" " and data[i]!="\n":
            if a:
                nmb1 = nmb1 + str(data[i])
        else :
            a = False

    nmb1 = int(nmb1)
    print("Le nombre que contient le QR code est : " + str(nmb1))


def calculate_slope(p1, p2):
    if p2.x - p1.x == 0 or p2.y - p1.y == 0:
               slope = 0
    else: 
        slope = -1 * (p2.y - p1.y)/(p2.x - p1.x)
    return slope

def distanceFinder(focalLength, knownWidth, widthInImage):
    '''
    This function basically estimate the distance, it takes the three arguments: focallength, knownwidth, widthInImage
    :param1 focalLength: focal length found through another function .
    param2 knownWidth : it is the width of object in the real world.
    param3 width of object: the width of object in the image .
    :returns the distance:
    '''
    distance = ((knownWidth * focalLength) / widthInImage)
    return distance

def focalLengthFinder(knowDistance, knownWidth, widthInImage):
    '''This function calculates the focal length. which is used to find the distance between  object and camera 
    :param1 knownDistance(int/float) : it is Distance form object to camera measured in real world.
    :param2 knownWidth(float): it is the real width of object, in real world
    :param3 widthInImage(float): the width of object in the image, it will be in pixels.
    return FocalLength(float): '''
    
    focalLength = ((widthInImage * knowDistance) / knownWidth)
    return focalLength

def eucaldainDistance(x, y, x1, y1):

    eucaldainDist = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)

    return eucaldainDist

def DetectQRcode(image):
    codeWidth = 0
    x, y = 0, 0
    euclaDistance = 0
    global Pos 
    # convert the color image to gray scale image
    Gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # create QR code object
    objectQRcode = pyzbar.decode(Gray)
    for obDecoded in objectQRcode:

        points = obDecoded.polygon
        if len(points) > 4:
            hull = cv2.convexHull(
                np.array([points for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        n = len(hull)
        # finding width of QR code in the image 
        x, x1 = hull[0][0], hull[1][0]
        y, y1 = hull[0][1], hull[1][1]
        
        Pos = hull[3]
        # using Eucaldain distance finder function to find the width 
        euclaDistance = eucaldainDistance(x, y, x1, y1)

        # retruing the Eucaldain distance/ QR code width other words  
        return euclaDistance

# initalize the cam
cap = cv2.VideoCapture(0)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()

referenceImage = cv2.imread("ab.jpg")
print("ok")
Rwidth= DetectQRcode(referenceImage)

KNOWN_DISTANCE = 30.1  # inches
KNOWN_WIDTH = 5.0  # inches
focalLength = focalLengthFinder(KNOWN_DISTANCE, KNOWN_WIDTH, Rwidth)
while True:
    _, img = cap.read()
    # detect and decode
    data, bbox, _ = detector.detectAndDecode(img)
    barcodes = pyzbar.decode(img)

    # finding width of QR code width in the frame 
    codeWidth= DetectQRcode(img)
    if codeWidth is not None and data:
        
        # print("not none")
        Distance = distanceFinder(focalLength, KNOWN_WIDTH, codeWidth)
        print ("Distance : " + str(round(10+Distance/(2.54),2)))
        # cv.putText(frame, f"Distance: {Distance}", (50,50), fonts, 0.6, (GOLD), 2)
        fin(data)
        data = None
    cv2.imshow("QRCODEscanner", img)    
    if cv2.waitKey(1) == ord("q"):
        break



cap.release()
cv2.destroyAllWindows()