import serial

ser= serial.Serial('/dev/ttyS0', baudrate=19200, timeout=1)

while True:
  with open('/var/www/html/Commandes.txt', 'r+') as f:
    cmd=f.readline()
    
    if cmd!="":
      print(cmd)
      f.seek(0)
      f.write("")
      f.truncate()
      ser.write(cmd.encode())
    else:
      pass
