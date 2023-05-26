import multiprocessing as mp
import time

def humain():
    while True :
        detection_humain.acquire()
        if detection_humain.value :
            # print("je suis entrain de detecter des humain")
            pass
        detection_humain.release()

def lecture_stm32():
    while True :
        time.sleep(2)
        recu = "qr"
        if recu=="qr":
            detection_humain.acquire()
            detection_humain.value = False
            detection_humain.release()
            type.acquire()
            type.value = 1
            type.release()
            envoie.acquire()
            envoie.value = True
            envoie.release()
            
        time.sleep(2)

        recu = "destination"
        if recu=="destination":
            type.acquire()
            type.value = 2
            type.release()
            envoie.acquire()
            envoie.value = True
            envoie.release()

        time.sleep(2)

        recu = "stop_qr"
        if recu=="stop_qr":
            detection_humain.acquire()
            detection_humain.value = True
            detection_humain.release()



def lecture_qr():
    while True:
        detection_humain.acquire()
        if detection_humain.value==False:
            qr.acquire()
            distance.acquire()
            qr.value+=1
            distance.value+=0.5
            new_qr.acquire()
            new_qr.value = True
            new_qr.release()
            # print("je suis entrain de detecter des qr codes")
            qr.release()
            distance.release()
        detection_humain.release()

def envoie_stm32():
    while True:
        envoie.acquire()
        if envoie.value :
            type.acquire()
            if type.value == 1:
                test = False
                while test==False:
                    new_qr.acquire()
                    test = new_qr.value
                    new_qr.release()
                new_qr.acquire()
                new_qr.value = False
                new_qr.release()
        
                print("j'envoie donne qr code + distance a stm32 ")

            if type.value == 2 :
                livraison.acquire()
                if livraison.value == 1 :
                    print('recupere corrdonee du livreur')
                    livraison.value = 2
                    'on rearrange la base de donnée'
                else :
                    print('recupere coordonne du destinataire')
                    livraison.value = 1
                livraison.release()
                print("j'envoie les données")
            type.release()

        envoie.value = False
        envoie.release()
                


if __name__ == "__main__" :

    detection_humain = mp.Value('b',True)
    envoie = mp.Value('b',False)
    qr = mp.Value('i',0)
    distance = mp.Value('f',1.0)
    new_qr = mp.Value('b',False)
    type = mp.Value('i',0)
    livraison = mp.Value('i',1)

    p1 = mp.Process(target=lecture_qr,args=())
    p2 = mp.Process(target=humain,args=())
    p3 = mp.Process(target=lecture_stm32,args=())
    p4 = mp.Process(target=envoie_stm32,args=())

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()