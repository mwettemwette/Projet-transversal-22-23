
import cv2
import numpy as np
import time
import os

#chargement YOLO
#net = cv2.dnn.readNet("yolov3.weights","yolov3.cfg") # Original yolov3
net = cv2.dnn.readNet("yolov3-tiny.weights","yolov3-tiny.cfg") #Tiny Yolo

classes = []
with open("coco.names","r") as f:
    classes = [line.strip() for line in f.readlines()]


# Video
cap = cv2.VideoCapture(0)
frameCam = cap.read()
cap.release()


def detection(frameCam,classes,net):
    outputlayers=[]
    layer_names = net.getLayerNames()
    for i in net.getUnconnectedOutLayers():
        outputlayers.append(layer_names[i - 1])
        
    colors= np.random.uniform(0,255,size=(len(classes),3))
    
    
    _,frame = frameCam # lécture vidéo

    
    height,width,channels = frame.shape
    # Detection
    blob = cv2.dnn.blobFromImage(frame,0.00392,(320,320),(0,0,0),True,crop=False) #reduce 416 to 320    

        
    net.setInput(blob)
    outs = net.forward(outputlayers)


    # Boites
    class_ids=[]
    confidences=[]
    boxes=[]
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # confiance detection
                center_x= int(detection[0]*width)
                center_y= int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                #rectangles
                x=int(center_x - w/2)
                y=int(center_y - h/2)

                boxes.append([x,y,w,h]) # rectangles
                confidences.append(float(confidence)) # Text confiance detection
                class_ids.append(class_id) # nom de l'objet

    indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.4,0.6)

    labels = []
    for i in range(len(class_ids)):
        labels.append(str(classes[class_ids[i]]))
        
    print(labels)

    if 'person' in labels:
        os.system("aplay bonjour.wav")
        time.sleep(1)
        cap.release()
        return()
        
    
    for i in range(len(boxes)):
        if i in indexes:
            x,y,w,h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence= confidences[i]
            color = colors[class_ids[i]]
            
            


        

    
    return()

detection(frameCam,classes,net)