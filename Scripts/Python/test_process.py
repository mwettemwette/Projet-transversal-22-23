import multiprocessing as mp


def oui():
    a.acquire()
    print("oui : "+str(a.value))
    a.value+=1
    print("oui : "+str(a.value))
    a.release()


def non():
    a.acquire()
    print("non : "+str(a.value))
    a.value+=1
    print("non : "+str(a.value))
    a.release()

if __name__ == "__main__" :
    a = mp.Value('i',5)


    p1 = mp.Process(target=oui,args=())
    p2 = mp.Process(target=non,args=())

    p1.start()
    p2.start()
    p1.join()
    p2.join()

