import Distance as dist




cap,detector,Rwidth,KNOWN_DISTANCE,KNOWN_WIDTH,focalLength = dist.init()

lecture = 0
while(lecture<10):
    lecture+=1
    nmb_frame = 0
    nmb,distance = dist.admmin_qr(cap,nmb_frame,detector,focalLength,KNOWN_WIDTH)

    print("nombre : "+str(nmb))
    print("distance : "+str(distance))

print("fin")