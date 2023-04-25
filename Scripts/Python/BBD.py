import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gdown


def trouver_nom(nom):
    try :
        cell = sheet.find(nom)
        return cell.row,cell.col
    except :
        print("Le nom n'est pas dans la base de donnee")
        return None,None

def trouver_nmb(nmb):
    try :
        cell = sheet.find(str(nmb))
        return cell.row,cell.col
    except :
        print("Le nombre n'est pas dans la base de donnee")
        return None,None

def get_x(row,col,nmb):
    return sheet.cell(row, col+nmb+1).value

def get_y(row,col,nmb):
    return sheet.cell(row, col+nmb+2).value


# Connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("Scripts\Python\projet.json", scope)
client = gspread.authorize(credentials)
sheet = client.open("BDD_nom_id_projet").sheet1


# Instruction test
x,y = trouver_nom("Julien")
if (x!=None and y!=None):
    print(get_x(x,y,0))
    print(get_y(x,y,0))

x,y = trouver_nmb(2)
if (x!=None and y!=None):
    print(get_x(x,y,1))
    print(get_y(x,y,1))






