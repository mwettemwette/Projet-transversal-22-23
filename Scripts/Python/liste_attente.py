import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gdown
import datetime

def trouver_nom(nom,sheet):
    try :
        cell = sheet.find(nom)
        return cell.row,cell.col
    except :
        print("Le nom n'est pas dans la base de donnee")
        return None,None

def trouver_nmb(nmb,sheet):
    try :
        cell = sheet.find(str(nmb))
        return cell.row,cell.col
    except :
        print("Le nombre n'est pas dans la base de donnee")
        return None,None

def get_x(row,col,nmb,sheet):
    return sheet.cell(row, col+nmb).value

def get_y(row,col,nmb,sheet):
    return sheet.cell(row, col+nmb).value


# Connect to Google Sheets
def connect_bdd(nom):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("robot\projet.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open("BDD_nom_id_projet").worksheet(nom)
    return sheet


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
    
   


    

def recup_livraison():
    sheet = connect_bdd("Requete")
    cell = sheet.cell(2, 2).value
    if cell == "":
        return None
    else :
        sheet = connect_bdd("Sheet1")
        li,col = trouver_nmb(cell,sheet)
        pos_x = get_x(li,col,2,sheet)
        pos_y = get_y(li,col,3,sheet)
        print(pos_x,pos_y)






# Instruction test

organisation_bdd()

# sheet = connect_bdd("Sheet2")
# x,y = trouver_nom("Julien",sheet)
# if (x!=None and y!=None):
#     print(get_x(x,y,0,sheet))
#     print(get_y(x,y,0,sheet))

# print("oui")
# x,y = trouver_nmb(2,sheet)
# if (x!=None and y!=None):
#     print(get_x(x,y,1,sheet))
#     print(get_y(x,y,1,sheet))






