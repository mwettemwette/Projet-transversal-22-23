import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gdown


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
    return sheet.cell(row, col+nmb+1).value

def get_y(row,col,nmb,sheet):
    return sheet.cell(row, col+nmb+2).value


# Connect to Google Sheets
def connect_bdd():
    scope = ['https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("Scripts\Python\projet.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open("BDD_nom_id_projet").sheet1
    return sheet



# Instruction test
sheet = connect_bdd()
x,y = trouver_nom("Julien",sheet)
if (x!=None and y!=None):
    print(get_x(x,y,0,sheet))
    print(get_y(x,y,0,sheet))

x,y = trouver_nmb(2,sheet)
if (x!=None and y!=None):
    print(get_x(x,y,1,sheet))
    print(get_y(x,y,1,sheet))






