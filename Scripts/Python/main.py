import multiprocessing as mp
import time

'A remettre pour utiliser les code de lecture de QR code'
import Distance as dist
import liste_attente as la

def humain():
    while True:
        detection_humain.acquire()
        if detection_humain.value :
            #detection(detection_humain)
            pass
        detection_humain.release()
        

def lecture_stm32():
    while True :
        'Lecture de ce que veut la stm32'
        'Décryptage de ce quelle veut'
        send_stm32.acquire()
        type_send.acquire()
        send_stm32.value = True
        'Si on passe en mode lecture de QR code : mode 1'
        type_send.value = 1
        'Si on passe en mode envoie de coordonné : mode 2'
        'Si on doit passer en mode lecture de QR code : on change la valeur de detection humain' 
        #
        type_send.value = 2
        detection_humain.acquire()
        detection_humain = False
        detection_humain.release()
        #
        'Si on recoit juste un message de fin de livraison'
        #
        la.organisation_bdd()
        #
        send_stm32.release()
        type_send.release()
        time.sleep(2)

def envoie_stm32():
    while True :
        send_stm32.acquire()
        if send_stm32.value:
            type_send.acquire()
            if type_send.value == 1: # mode envoie cherche qr code et envoie distance
                #envoie a stm32 des infos
                test = False
                while test==False :
                    new_qr.acquire()
                    test = new_qr.value
                    new_qr.release()
                Distance_QR.acquire()
                QR_code.acquire()
                print("Distance envoyé : "+ str(Distance_QR.value)+" nombre qr envoye : "+str(QR_code.value))
                new_qr.acquire()
                new_qr = False
                new_qr.release()
                Distance_QR.release()
                QR_code.release()

            if type_send==2 : # mode envoie prochaine position + position actuelle (dernier qr code lu + distance)
                livraison.acquire()
                new_posx,new_posy = la.get_new_coord(livraison.value)
                if livraison.value == 1:
                    livraison.value = 2
                else :
                    livraison.value = 1
                livraison.release()
                # envoie des infos à la stm32

            else :
                pass
                #autre if de truc qu'on peut envoyer
            type_send.release()
        send_stm32.value = False
        send_stm32.release()

def process_principal():
    N = 10
    nb = 0
    while nb<N:
        nb+=1
        pass

def lecture_qr(cap,detector,Rwidth,KNOWN_DISTANCE,KNOWN_WIDTH,focalLength):
    while True:
        detection_humain.acquire()
        if detection_humain.value==False:
            'a mettre dans le code + rajouter dans le lecture_qr les arguments voulue'
            nmb_frame = 0
            nmb,distance = dist.admmin_qr(cap,nmb_frame,detector,focalLength,KNOWN_WIDTH)
            QR_code.acquire()
            Distance_QR.acquire()
            new_qr.acquire()
            QR_code.value = nmb
            Distance_QR.value = distance
            new_qr.value = True
            QR_code.release()
            Distance_QR.release()
            new_qr.release()
        detection_humain.release()


if __name__ == "__main__" :
    posx = mp.Value('i',1)
    posy = mp.Value('i',1)
    livraison = mp.Value('i',1) # si =1 on doit commencer une livraison // si =2 on est en cours de livraison
    QR_code = mp.Value('i',1)
    Distance_QR = mp.Value('f',1)
    new_qr = mp.Value('b',False)
    detection_humain = mp.Value('b',False)
    send_stm32 = mp.Value('b',False)
    type_send = mp.Value('i',0)
    
    'A mettre pour le faire fonctionner avec le programme des distances'
    cap,detector,Rwidth,KNOWN_DISTANCE,KNOWN_WIDTH,focalLength = dist.init()
    p1 = mp.Process(target=process_principal,args=())
    p2 = mp.Process(target=lecture_stm32,args=())
    p3 = mp.Process(target=lecture_qr,args=(cap,detector,Rwidth,KNOWN_DISTANCE,KNOWN_WIDTH,focalLength))
    p4 = mp.Process(target=envoie_stm32,args=())
    p5 = mp.Process(target=lecture_stm32,args=())

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()



