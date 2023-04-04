import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gdown

# Connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

#credentials = ServiceAccountCredentials.from_json_keyfile_name("Scripts\API_key\projet.json", scope)
#client = gspread.authorize(credentials)

#sheet = client.open("BDD_nom_id_projet").sheet1

#sheet.update('B8',"Emma")
#lst = sheet.get_all_values()
#print(lst)
f = open('Scripts\Python\drive_api.txt','r')
link = f.read()
print(link)
gdown.download(link,'Scripts\Python\projet.json')
