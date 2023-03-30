import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("Scripts\API_key\projet.json", scope)
client = gspread.authorize(credentials)

sheet = client.open("BDD_nom_id_projet").sheet1

sheet.update('B8',"Emma")
lst = sheet.get_all_values()
print(lst)
