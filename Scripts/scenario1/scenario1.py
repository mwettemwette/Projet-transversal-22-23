import multiprocessing as mp
import Distance as dist
import serial
import cv2
import detection2 as detec
import time

def humain(cap,classes,net):
    while True :
        detection_humain.acquire()
        if detection_humain.value :
            cap = cv2.VideoCapture(0)
            frameCam = cap.read()
            detec.detection(frameCam,classes,net)
            cap.release()
        detection_humain.release()
        time.sleep(0.5)

def lecture_stm32():
    ser = serial.Serial('/dev/ttyS0', baudrate=19200, timeout=1)
    cmd = "START_AUTONOMOUS"
    ser.write(cmd.encode())
    while True :
        # Lecture du message reçu
        message = ser.readline().decode().strip()
        
        # Vérification si le message n'est pas vide
        if message:
            if message == "START_CAM":
                detection_humain.acquire()
                detection_humain.value = False
                detection_humain.release()
                start_qr.acquire()
                start_qr.value = True
                start_qr.release()
                while True :
                    new_qr.acquire()
                    if new_qr.value :
                        qr.acquire()
                        distance.acquire()
                        cycle.acquire()
                        if qr.value!=0 :
                            cmd = 'DIST_QR:['+str(distance.value*10)+"]"
                            ser.write(cmd.encode())
                            cycle.value = 0
                            break
                        elif cycle.value==4 :
                            cycle.value=0
                            cmd = 'ERROR_QR'
                            ser.write(cmd.encode())
                            cycle.value = 0
                            break
                        else :
                            cmd = 'ERROR_QR'
                            ser.write(cmd.encode())
                            break
                    new_qr.release()
                    time.sleep(0.5)
                new_qr.value = False
                new_qr.release()
                qr.release()
                distance.release()
                cycle.release()
                        



            if message == "ASK_INIT":
                cmd = "DIR_INTI:[45]:[1000]"
                ser.write(cmd.encode())

            if message == "STOP_CAM" :
                detection_humain.acquire()
                detection_humain.value = True
                detection_humain.release()
                

            
        # Arrêt du programme "q"
        if message == "q":
            stop.acquire()
            stop.value = True
            stop.release()
            break
    # Fermeture du port série
    ser.close()
        



def lecture_qr(cap,detector,focalLength,KNOWN_WIDTH):
    while True:
        detection_humain.acquire()
        start_qr.acquire()
        if not detection_humain.value and start_qr.value:
            time.sleep(1.5)
            qr.acquire()
            distance.acquire()
            cap = cv2.VideoCapture(0)
            qr.value,distance.value = dist.admmin_qr(cap,10,detector,focalLength,KNOWN_WIDTH)
            cap.release()
            new_qr.acquire()
            new_qr.value = True
            new_qr.release()
            qr.release()
            distance.release()
            cycle.acquire()
            cycle.value+=1
            cycle.release()
        start_qr.value = False
        start_qr.release()
        detection_humain.release()
        time.sleep(0.5)

def envoie_stm32(ser):
    while True:
        new_qr.acquire()
        if new_qr.value :
            qr.acquire()
            distance.acquire()
            cycle.acquire()
            if qr.value !=0 and distance.value!=0:
                cmd = 'DIST_QR:['+str(distance.value*10)+"]"
                ser.write(cmd.encode())
            elif cycle.value==4 :
                cycle.value=0
                cmd = 'ERROR_QR'
                ser.write(cmd.encode())

            new_qr.value = False
            qr.release()
            distance.release()
            new_qr.release()
            cycle.release()

        type.acquire()
        if type.value==1:
            cmd = "DIR_INTI:[45]:[1000]"
            ser.write(cmd.encode())
            type.value = 0
        type.release()

        


if __name__ == "__main__" :

    detection_humain = mp.Value('b',True)
    start_qr = mp.Value('b',False)
    qr = mp.Value('i',0)
    distance = mp.Value('f',0.0)
    new_qr = mp.Value('b',False)
    type = mp.Value('i',0)
    cycle = mp.Value('i',0)
    stop = mp.Value('b',False)

    # ser = serial.Serial('/dev/ttyS0', baudrate=19200, timeout=1)

    cap,detector,Rwidth,KNOW_DISTANCE,KNOW_WIDTH,focalLength = dist.init()
    cap.release()
    net = cv2.dnn.readNet("yolov3-tiny.weights","yolov3-tiny.cfg") #Tiny Yolo
    classes = []
    with open("coco.names","r") as f:
        classes = [line.strip() for line in f.readlines()]

    cmd = "START_AUTONOMOUS"
    # ser.write(cmd.encode())

    p1 = mp.Process(target=lecture_qr,args=(cap,detector,focalLength,KNOW_WIDTH))
    p2 = mp.Process(target=humain,args=(cap,classes,net))
    p3 = mp.Process(target=lecture_stm32,args=())
    # p4 = mp.Process(target=envoie_stm32,args=(ser,))

    p1.start()
    p2.start()
    p3.start()
    # p4.start()

    p1.join()
    p2.join()
    p3.join()
    # p4.join()
