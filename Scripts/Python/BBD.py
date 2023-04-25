import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gdown


def trouver_nom(nom):
    try :
        cell = sheet.find(nom)
        print(cell.row,cell.col)
    except :
        print("Le nom n'est pas dans la base de donnee")

def trouver_nmb(nmb):
    try :
        cell = sheet.find(nmb)
        print(cell.row,cell.col)
        return cell
    except :
        print("Le nom n'est pas dans la base de donnee")
        return None

def get_x(row,col):
    return 1


# Connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("Scripts\Python\projet.json", scope)
client = gspread.authorize(credentials)

sheet = client.open("BDD_nom_id_projet").sheet1

#sheet.update('B8',"Emma")
lst = sheet.get_all_values()
trouver_nom("a")
ligne = sheet.row_values(3)
print(ligne)
print(lst)
# f = open('Scripts\drive_api.txt','r')
# link = f.read()
# print(link)
# gdown.download(link,'Scripts\Python\projet.json')



