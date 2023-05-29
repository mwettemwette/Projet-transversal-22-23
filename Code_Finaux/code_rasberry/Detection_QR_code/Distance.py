'''
But du programme : détecter un QR code, retourner le nombre que celui contient, et la distance avec la caméra.
Auteurs : LEROUX Gaëlle 
'''

import cv2
from pyzbar import pyzbar
import math
import numpy as np

'Permet de retourner le nombre que contient le QR code présentée devant la caméra'
def fin(data):
    nmb1 = ""
    a = True
    for i in range(len(data)):
        if data[i]!=" " and data[i]!="\n":
            if a:
                nmb1 = nmb1 + str(data[i])
        else :
            a = False

    nmb1 = int(nmb1)
    return nmb1


def calculate_slope(p1, p2):
    if p2.x - p1.x == 0 or p2.y - p1.y == 0:
               slope = 0
    else: 
        slope = -1 * (p2.y - p1.y)/(p2.x - p1.x)
    return slope

def distanceFinder(focalLength, knownWidth, widthInImage):
    '''
    Cette fonction permet d'estimer la distance, elle prend les trois arguments suivants : focalLength, knownwidth, widthInImage.
    param1 focalLength : longueur focale trouvée par une autre fonction.
    param2 knownWidth : c'est la largeur de l'objet dans le monde réel.
    param3 width of object : la largeur de l'objet dans l'image .
    :renvoie la distance : '''
    distance = ((knownWidth * focalLength) / widthInImage)
    return distance

def focalLengthFinder(knowDistance, knownWidth, widthInImage):
    '''Cette fonction calcule la longueur focale, qui est utilisée pour déterminer la distance entre l'objet et l'appareil photo. 
    :param1 knownDistance(int/float) : c'est la distance entre l'objet et la caméra, mesurée dans le monde réel.
    :param2 knownWidth(float) : c'est la largeur réelle de l'objet, dans le monde réel.
    :param3 widthInImage(float) : la largeur de l'objet dans l'image, en pixels.
    return FocalLength(float) : '''

    focalLength = ((widthInImage * knowDistance) / knownWidth)
    return focalLength

def eucaldainDistance(x, y, x1, y1):
    '''Cette fonction permet de calculer la distance euclidienne entre deux points, elle prend en entrée les coordonnées de ces 2 points
    Elle renvoie la distance'''

    eucaldainDist = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)

    return eucaldainDist


def DetectQRcode(image):
    '''
    Cette fonction permet de calculer de détecter un QR code et d'en calculersa largeur sur l'image
    Elle prend en entrée une image.
    Elle renvoie la largeur.
    '''
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


def init() :
    ''' 
    Cette fonction permet d'initialiser les données nécessaires au bon fonctionnement du code.
    Elle renvoie : cap,detector,Rwidth,KNOWN_DISTANCE,KNOWN_WIDTH,focalLength 
    '''
    # initalize the cam
    cap = cv2.VideoCapture(0)
    # initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()

    referenceImage = cv2.imread("./Scripts/Python/QR_base_papier.jpg")
    Rwidth= DetectQRcode(referenceImage)

    KNOWN_DISTANCE = 22.5*2.4  # inches
    KNOWN_WIDTH = 10.5*2.4  # inches
    focalLength = focalLengthFinder(KNOWN_DISTANCE, KNOWN_WIDTH, Rwidth)
    return cap,detector,Rwidth,KNOWN_DISTANCE,KNOWN_WIDTH,focalLength


def admmin_qr(cap,nmb_frame,detector,focalLength,KNOWN_WIDTH):
    ''' Cette fonction permet de détecter si il y a un QR code sur N frames et de renvoyé son contenu et la distance avec la caméra.
    Elle prend en entrée la caméra, le nombre N de frames, detector,focalLength,KNOWN_WIDTH.
    Si un QR code et une distance ont été trouvé elle les renvoies, sinon elle renvoie 0.
    '''
    Distance = None
    nmb = None
    while True :
        _, img = cap.read()
        nmb_frame = nmb_frame-1
        # detect and decode
        data, bbox, _ = detector.detectAndDecode(img)
        barcodes = pyzbar.decode(img)

        # finding width of QR code width in the frame 
        codeWidth= DetectQRcode(img)
        if codeWidth is not None and data:
            Distance = distanceFinder(focalLength, KNOWN_WIDTH, codeWidth)
            Distance = round(Distance/(2.54),2)
            nmb = fin(data)
            data = None

        if nmb_frame == 0 :
            if Distance!=None and nmb!=None:
                return nmb,Distance 
            else :
                return 0,0
        
        


