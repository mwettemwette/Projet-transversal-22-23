'''
But du programme : Fonction permettant la manipulation de la base de donnée
Auteurs : LEROUX Gaëlle / COURBIN Michel
'''

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gdown
import datetime

'''
Cette fonction permet de trouver une string dans le sheet placer en paramètre.
Renvoie la ligne et la colonne si trouvé sinon renvoie None.
'''
def trouver_nom(nom,sheet):
    try :
        cell = sheet.find(nom)
        return cell.row,cell.col
    except :
        return None,None

'''
Cette fonction permet de trouver un nombre dans le sheet placer en paramètre.
Renvoie la ligne et la colonne si trouvé sinon renvoie None.
'''
def trouver_nmb(nmb,sheet):
    try :
        cell = sheet.find(str(nmb))
        return cell.row,cell.col
    except :
        print("Le nombre n'est pas dans la base de donnee")
        return None,None

'''
Cette fonction permet de renvoyer la valeur situé à la colonne col+nmb et à la ligne row du sheet placé en paramètre.
'''
def get_x(row,col,nmb,sheet):
    return sheet.cell(row, col+nmb).value

def get_y(row,col,nmb,sheet):
    return sheet.cell(row, col+nmb).value


'''
Cette fonction permet de se connecter au sheet placer en paramètre.
'''
def connect_bdd(nom):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("Code_Finaux\code_rasberry\Base_de_donnees\projet.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open("BDD_nom_id_projet").worksheet(nom)
    return sheet


'''
Cette fonction permet d'organiser la base de donnée lors de la fin d'une livraison.
'''
def organisation_bdd():
    # Update de la sheet Requete
    sheet = connect_bdd("Requete")
    cell_envoyeur = sheet.cell(2, 1).value
    cell_destinataire = sheet.cell(2, 2).value
    if cell_envoyeur!=None and cell_destinataire!=None:
        sheet.delete_rows(2)

        # Update de la sheet Livrer
        sheet = connect_bdd("Livrer")
        cell_nmb_commande = sheet.cell(2, 5).value
        now = datetime.datetime.now()

        sheet.update_cell(int(cell_nmb_commande)+2,3,now.strftime("%d/%m/%Y"))
        sheet.update_cell(int(cell_nmb_commande)+2,4,now.strftime("%H:%M:%S"))
        sheet.update_cell(int(cell_nmb_commande)+2,1,cell_envoyeur)
        sheet.update_cell(int(cell_nmb_commande)+2,2,cell_destinataire)
        sheet.update_cell(2,5,int(cell_nmb_commande)+1)
    else :
        pass
    

'''
Cette fonction permet de renvoyer les prochaines coordonnées que le robot doit atteindre.
La fonction prend en entrée 1 ou 2 :
1 : renvoie les coordonnée de l'expéditeur de la prochaine livraison
2 : renvoie les coordonnée du destinataire de la prochaine livraison
'''
def get_new_coord(nmb):
    sheet = connect_bdd("Requete")
    cell = sheet.cell(2, nmb).value
    sheet = connect_bdd("Sheet1")
    row,col = trouver_nmb(cell,sheet)
    return (sheet.cell(row, col+2).value,sheet.cell(row, col+3).value)





'''Instruction test'''

# organisation_bdd()

# a,b=get_new_coord(1)
# print(a,b)

# a,b=get_new_coord(2)
# print(a,b)







