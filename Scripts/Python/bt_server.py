import socket 
import bluetooth

from getmac import get_mac_address as gma

# we get the mac address of our raspberry
interface_mac_add =gma()
#print(interface_mac_add)

# creating a bluetooth socket, the tipe of socket , ....., and the protocol
server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

server.bind( (interface_mac_add, 1028) )
server.listen(1)

client, addr = server.accetp()
run=True
try:
    while run:
        msg = client.recv(1024)
        print(f"Message : {msg.decode('utf-8')}")
        if not msg :
            break
        else :
            run = False
        

except OSError as e :
    pass

client.close()