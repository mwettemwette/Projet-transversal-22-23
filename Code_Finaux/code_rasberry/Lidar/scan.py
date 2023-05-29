#!/usr/bin/env python3
'''Records scans to a given file in the form of numpy array.
Usage example:

$ ./record_scans.py out.npy'''
import serial
import numpy as np
from rplidar import RPLidar


PORT_NAME = '/dev/ttyUSB9'



def near(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def run():
    '''Main'''
    lidar = RPLidar(PORT_NAME)
    lidar.stop_motor()
    lidar.stop()
    lidar.disconnect()
    lidar = RPLidar(PORT_NAME)
    
    ser = serial.Serial ("/dev/ttyS0", 19200) 

    
    try:
        for scan in lidar.iter_scans():
            toSend="LIDAR"
            angle=[]
            dist = []
            
            for i in scan:
                angle.append(i[1])
            indexs=[round(near(angle,90),1), round(near(angle,135),1),round(near(angle,160),1),
                    round(near(angle,180),1),round(near(angle,200),1),round(near(angle,225),1),round(near(angle,270),1)]
            
            for k in scan:
                if round(k[1],1) in indexs:
                    # toSend.append([k[1],k[2]]) # Angle + distance en mm
                    toSend+=":"+(str(round(k[2]))[:-1:])
                    dist.append(1)
                    
                    
            print(toSend)
            if len(dist) == 7:
                ser.write(toSend.encode())
            print("\n")
        
    except KeyboardInterrupt:
        print('Erreur')
        
    lidar.stop()
    lidar.disconnect()
    print(np.array(data))
    

if __name__ == '__main__':
    run()
