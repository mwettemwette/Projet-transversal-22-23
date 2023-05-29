import serial

# Configuration du port série
ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)

while True:
    # Lecture du message reçu
    message = ser.readline().decode().strip()
    
    # Vérification si le message n'est pas vide
    if message:
        print("Message reçu:", message)

        
    # Arrêt du programme "q"
    if message == "q":
        break

# Fermeture du port série
ser.close()
