import multiprocessing as mp


def oui():
    nmb.acquire()
    print(nmb)
    nmb+=1
    print(nmb)
    nmb.release()

if __name__ == "__main__" :
    nmb = mp.Value('i',5)


    p1 = mp.Process(target=oui,args=())

    p1.start()
    p1.join()

