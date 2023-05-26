import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gdown






def get_x(row,col,nmb):
    return sheet.cell(row, col+nmb+1).value

def get_y(row,col,nmb):
    return sheet.cell(row, col+nmb+2).value

def trouver_nom(sheet, nom):
    try :
        cell = sheet.find(nom)
        return cell.row,cell.col
    except :
        print("user not in the data base")
        return None,None


"""****************************** TO LOG IN THE APP ****************************"""
def get_BDD_log():
    # Connect to Google Sheets
    scope = ['https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("Appli_BDD/projet.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open("BDD_nom_id_projet").worksheet("Sheet2")
    return sheet

def trouver_nmb(nmb):
    try :
        cell = sheet.find(str(nmb))
        return cell.row,cell.col
    except :
        #print("Le nombre n'est pas dans la base de donnee")
        return None,None


def get_user_pwd(sheet, row, col):
    return sheet.cell(row, col+1).value

def check_utilisateur(name, pwd):
    # We get our Data Base
    print("getting the user from the data base ")
    sheet = get_BDD_log()
    row, col =trouver_nom(sheet, name)
    #print(row, col)
    #if we got a result
    if ( row !=None and col!=None ):
        print('user found !')
        # checking for the password
        if ( pwd == get_user_pwd(sheet,row, col) ):
            print(" password foung")
            return True
        return False 
    else :
        print("user not found ...")
        return False

"""**********************************************TO CALL THE ROBOT***************************************"""
def get_BDD_ID_CALL():
    # Connect to Google Sheets
    scope = ['https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("Appli_BDD/projet.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open("BDD_nom_id_projet").worksheet("Sheet2")
    return sheet

def find_ID(sheet, nmb):
    """ This function returns the line and row if the data base of the str nmb"""
    try :
        cell = sheet.find(str(nmb))
        return cell.row,cell.col
    except :
        #print("Le nombre n'est pas dans la base de donnee")
        return None,None

def get_ID(sheet, row, col):
    """ This function returns the id matchin th user's name (a raw and a column) """
    return sheet.cell(row, col+2).value# a column before the user's name

def find_ID_people(name):
    # We get our Data Base containg the ids
    sheet = get_BDD_ID_CALL()

    # we try to find the position of the adresse in our data base
    row, col = find_ID(sheet, name)

    return get_ID(sheet, row, col)

"""*************************************WRITING THE USER'S CALL **********************************"""
def get_queue():
    """ We get the data base that upadets the queue for the robot's calls"""
     # Connect to Google Sheets
    scope = ['https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("Appli_BDD/projet.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open("BDD_nom_id_projet").worksheet("Requete")
    return sheet

def write_call(sender, adresse):
    
    adresse_ID = find_ID_people(adresse)
    print("adresse found")
    sender_ID = find_ID_people(sender)
    print("sender found")

    sheet = get_queue()
    print(" got the id bdd")
    empty_row = len( sheet.col_values(1))+1
    print("empty row found")
    #sheet.update_cell(2,1,'Emma')
    row = [sender_ID, adresse_ID]
    print(row)
    sheet.insert_row(row, empty_row )
    print("wrote in sheet")
    return True


""" ******************************** SOME TESTS **************************************"""


#check_utilisateur("gaellou", "azer")
#print(find_ID_adresse("gaellou"))
#write_call()