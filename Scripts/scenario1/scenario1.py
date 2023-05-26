import multiprocessing as mp
import envoit as env
import uart as rece
import Distance as dist
import serial

def humain():
    while True :
        detection_humain.acquire()
        if detection_humain.value :
            # print("je suis entrain de detecter des humain")
            pass
        detection_humain.release()

def lecture_stm32(ser):
    while True :
        # Lecture du message reçu
        message = ser.readline().decode().strip()
        
        # Vérification si le message n'est pas vide
        if message:
            print("Message reçu:", message)
            if message == "qr":
                type.acquire()
                type.value = 1
                type.release()
                detection_humain.acquire()
                detection_humain.value = False
                detection_humain.release()

            
        # Arrêt du programme "q"
        if message == "q":
            break
    # Fermeture du port série
    ser.close()
        



def lecture_qr(cap,nmb_frame,detector,focalLength,KNOWN_WIDTH):
    while True:
        detection_humain.acquire()
        if detection_humain.value==False:
            qr.acquire()
            distance.acquire()
            qr.value,distance.value = dist.admmin_qr(cap,nmb_frame,detector,focalLength,KNOWN_WIDTH)
            new_qr.acquire()
            new_qr.value = True
            new_qr.release()
            qr.release()
            distance.release()
        detection_humain.value = True
        detection_humain.release()

def envoie_stm32():
    while True:
        new_qr.acquire()
        if new_qr.value :
            qr.acquire()
            distance.acquire()
            cmd = str(qr.value)+" "+str() 
            ser.write(cmd.encode())


if __name__ == "__main__" :

    detection_humain = mp.Value('b',True)
    envoie = mp.Value('b',False)
    qr = mp.Value('i',0)
    distance = mp.Value('f',1.0)
    new_qr = mp.Value('b',False)
    type = mp.Value('i',0)
    livraison = mp.Value('i',1)

    ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)

    cap,nmb_frame,detector,focalLength,KNOWN_WIDTH = dist.init()

    p1 = mp.Process(target=lecture_qr,args=(cap,nmb_frame,detector,focalLength,KNOWN_WIDTH))
    p2 = mp.Process(target=humain,args=())
    p3 = mp.Process(target=lecture_stm32,args=(ser))
    p4 = mp.Process(target=envoie_stm32,args=())

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()