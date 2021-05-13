# -*- coding: utf-8 -*-

import os
import json
import sqlite3
import textwrap

CUR_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(CUR_DIR, "data")
PATH_FILE = os.path.join(CUR_DIR, "db_path_viewer.json")

with open(PATH_FILE, "r", encoding='utf8') as f :
    raw_path = json.load(f)
f.close()
path = raw_path["path"]

def get_db_path():
    global path
    with open(PATH_FILE, "r", encoding='utf8') as f :
        raw_path = json.load(f)
    f.close()
    path = raw_path["path"]

## LECTURE DE LA TABLE STOCK :

def _get_all_stock_values() : # Récupere la table "Stock" intégralement
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = "SELECT * FROM Stock"
        c.execute(sql)
        all_stock_values = c.fetchall()
        conn.close()

        return all_stock_values
    except sqlite3.OperationalError :
        pass

def get_stock_item_names() : # Récupere les Item Names de "Stock"
    try :
        stock_item_names = []
        all_stock_values = _get_all_stock_values()
        for value in all_stock_values :
            stock_item_names.append(value[0])

        return stock_item_names
    except TypeError :
        pass

def get_stock_stockCount() : # Récupere les Stock Counts de "Stock"
    try :
        stock_stockCount = []
        all_stock_values = _get_all_stock_values()
        for value in all_stock_values :
            stock_stockCount.append(value[1])

        return stock_stockCount
    except TypeError :
        pass

def get_one_stock_stockCount(name) : # Récupere le Stock Count d'un Item de "Stock"
    try :
        item_row = get_item_row(name)
        item_stockCount = item_row[0][1]

        return item_stockCount
    except TypeError :
        pass

def get_one_stock_atelCount(name) : # Récupere le Atel Count d'un Item de "Stock"
    try :
        item_row = get_item_row(name)
        item_atelCount = item_row[0][3]

        return item_atelCount
    except TypeError :
        pass

def get_stock_pretsCount() : # Récupere les Prets Counts de "Stock"
    try :
        stock_pretsCount = []
        all_stock_values = _get_all_stock_values()
        for value in all_stock_values :
            stock_pretsCount.append(value[2])

        return stock_pretsCount
    except TypeError :
        pass

def get_stock_atelCount() : # Récupere les Atelier Counts de "Stock"
    try :
        stock_atelCount = []
        all_stock_values = _get_all_stock_values()
        for value in all_stock_values :
            stock_atelCount.append(value[3])

        return stock_atelCount
    except TypeError :
        pass

def get_item_row(name) : # Récupere la ligne de la table "Stock" correspondante à "name"
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Stock WHERE Item = ("%s")""" %(name)
        c.execute(sql)
        item_row = c.fetchall()
        conn.close()

        return item_row
    except sqlite3.OperationalError :
        pass

def get_nonull_atelCount_items() : # Récupere la liste des Items de "Stock" dont AtelCount est non-nul
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Stock WHERE AtelCount != 0"""
        c.execute(sql)
        nonull_atel_items = c.fetchall()
        conn.close()

        return nonull_atel_items
    except sqlite3.OperationalError :
        pass

## LECTURE DE LA TABLE STOCK TECHNIQUE :

def _get_all_tech_stock_values() : # Récupere la table "Tech_Stock" intégralement
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = "SELECT * FROM Tech_Stock"
        c.execute(sql)
        all_tech_stock_values = c.fetchall()
        conn.close()

        return all_tech_stock_values
    except sqlite3.OperationalError :
        pass

def get_tech_stock_item_names() : # Récupere les Item Names de "Tech_Stock"
    try :
        tech_stock_item_names = []
        all_tech_stock_values = _get_all_tech_stock_values()
        for value in all_tech_stock_values :
            tech_stock_item_names.append(value[0])

        return tech_stock_item_names
    except TypeError :
        pass

def get_tech_stock_stockCount() : # Récupere les Stock Counts de "Tech_Stock"
    try :
        tech_stock_stockCount = []
        all_tech_stock_values = _get_all_tech_stock_values()
        for value in all_tech_stock_values :
            tech_stock_stockCount.append(value[1])

        return tech_stock_stockCount
    except TypeError :
        pass

def get_one_tech_stock_stockCount(name) : # Récupere le Stock Count d'un Item de "Tech_Stock"
    try :
        tech_item_row = get_tech_item_row(name)
        tech_item_stockCount = tech_item_row[0][1]

        return tech_item_stockCount
    except TypeError :
        pass

def get_tech_stock_pretsCount() : # Récupere les Prets Counts de "Tech_Stock"
    try :
        tech_stock_pretsCount = []
        all_tech_stock_values = _get_all_tech_stock_values()
        for value in all_tech_stock_values :
            tech_stock_pretsCount.append(value[2])

        return tech_stock_pretsCount
    except TypeError :
        pass

def get_tech_stock_atelCount() : # Récupere les Atelier Counts de "Tech_Stock"
    try :
        tech_stock_atelCount = []
        all_tech_stock_values = _get_all_tech_stock_values()
        for value in all_tech_stock_values :
            tech_stock_atelCount.append(value[3])

        return tech_stock_atelCount
    except TypeError :
        pass

def get_one_tech_stock_atelCount(name) : # Récupere le Atel Count d'un Item de "Tech_Stock"
    try :
        tech_item_row = get_tech_item_row(name)
        tech_item_atelCount = tech_item_row[0][3]

        return tech_item_atelCount
    except TypeError :
        pass

def get_tech_item_row(name) : # Récupere la ligne de la table "Tech_Stock" correspondante à "name"
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Tech_Stock WHERE Item = ("%s")""" %(name)
        c.execute(sql)
        tech_item_row = c.fetchall()
        conn.close()

        return tech_item_row
    except sqlite3.OperationalError :
        pass

def get_nonull_tech_atelCount_items() : # Récupere la liste des Items de "Stock" dont AtelCount est non-nul
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Tech_Stock WHERE AtelCount != 0"""
        c.execute(sql)
        nonull_tech_atel_items = c.fetchall()
        conn.close()

        return nonull_tech_atel_items
    except sqlite3.OperationalError :
        pass

## LECTURE DE LA TABLE PRETS :

def _get_all_prets_values() : # Récupere la table "Prets" intégralement
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = "SELECT * FROM Prets"
        c.execute(sql)
        all_prets_values = c.fetchall()
        conn.close()

        return all_prets_values
    except sqlite3.OperationalError :
        pass

def get_prets_localisations() : # Récupere les Localisations de "Prets"
    try :
        prets_localisations = []
        all_prets_values = _get_all_prets_values()
        for value in all_prets_values :
            prets_localisations.append(value[0])

        return prets_localisations
    except TypeError :
        pass

def get_prets_types() : # Récupere les Types de "Prets"
    try :
        prets_types = []
        all_prets_values = _get_all_prets_values()
        for value in all_prets_values :
            prets_types.append(value[1])

        return prets_types
    except TypeError :
        pass

def get_prets_row(localisation) : # Récupere la ligne de la table "Prets" correspondante à "localisation"
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Prets WHERE Localisation = ("%s")""" %(localisation)
        c.execute(sql)
        prets_row = c.fetchall()
        conn.close()

        return prets_row
    except sqlite3.OperationalError :
        pass

def get_one_prets_type(localisation) :  # Récupere le Type d'une Localisation de "Prets"
    try :
        prets_row = get_prets_row(localisation)
        prets_type = prets_row[0][1]

        return prets_type
    except TypeError :
        pass

def get_prets_lists() : # Récupere les Listes de "Prets"
    try :
        prets_lists = []
        all_prets_values = _get_all_prets_values()
        for value in all_prets_values :
            prets_lists.append(value[2])

        return prets_lists
    except TypeError :
        pass

def get_one_prets_list(localisation) :  # Récupere la Liste d'une Localisation de "Prets"
    try :
        prets_row = get_prets_row(localisation)
        prets_list = prets_row[0][2]

        return prets_list
    except TypeError :
        pass

## LECTURE DE LA TABLE MISSION :

def _get_all_mission_values() : # Récupere la table "Mission" intégralement
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = "SELECT * FROM Mission"
        c.execute(sql)
        all_mission_values = c.fetchall()
        conn.close()

        return all_mission_values
    except sqlite3.OperationalError :
        pass

def get_mission_titles() : # Récupere les Titles de "Mission"
    try :
        mission_titles = []
        all_mission_values = _get_all_mission_values()
        for value in all_mission_values :
            mission_titles.append(value[1])

        return mission_titles
    except TypeError :
        pass

def get_mission_types() : # Récupere les Types de "Mission"
    try :
        mission_types = []
        all_mission_values = _get_all_mission_values()
        for value in all_mission_values :
            mission_types.append(value[2])

        return mission_types
    except TypeError :
        pass

def get_mission_dates() : # Récupere les Dates de "Mission"
    try :
        mission_dates = []
        all_mission_values = _get_all_mission_values()
        for value in all_mission_values :
            mission_dates.append(value[3])

        return mission_dates
    except TypeError :
        pass

def get_mission_times() : # Récupere les Times de "Mission"
    try :
        mission_times = []
        all_mission_values = _get_all_mission_values()
        for value in all_mission_values :
            mission_times.append(value[4])

        return mission_times
    except TypeError :
        pass

def get_mission_return_dates() : # Récupere les Return Dates de "Mission"
    try :
        mission_return_dates = []
        all_mission_values = _get_all_mission_values()
        for value in all_mission_values :
            mission_return_dates.append(value[5])

        return mission_return_dates
    except TypeError :
        pass

def get_mission_return_times() : # Récupere les Return Times de "Mission"
    try :
        mission_return_times = []
        all_mission_values = _get_all_mission_values()
        for value in all_mission_values :
            mission_return_times.append(value[6])

        return mission_return_times
    except TypeError :
        pass

def get_mission_descriptions() : # Récupere les Desriptions de "Mission"
    try :
        mission_descriptions = []
        all_mission_values = _get_all_mission_values()
        for value in all_mission_values :
            mission_descriptions.append(value[7])

        return mission_descriptions
    except TypeError :
        pass

def get_mission_matos() : # Récupere les Materiels de "Mission"
    try :
        mission_matos = []
        all_mission_values = _get_all_mission_values()
        for value in all_mission_values :
            mission_matos.append(value[8])

        return mission_matos
    except TypeError :
        pass

def _get_missions_from_date(date) : # Récupere les Rows correspondants a "date"
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Mission WHERE MissionDate = ("%s")""" %(date)
        c.execute(sql)
        mission_rows = c.fetchall()
        conn.close()

        return mission_rows
    except sqlite3.OperationalError :
        pass

def get_ids_from_date(date) : # Récupere les IDS des Missions correspondants a "date"
    try :
        mission_rows = _get_missions_from_date(date)
        missions_ids = []

        for mission in mission_rows :
            missions_ids.append(mission[0])

        return missions_ids
    except TypeError :
        pass

def get_date_from_id(id) : # Récupere la "date" correspondant à "id"
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Mission WHERE MissionID = ("%s")""" %(id)
        c.execute(sql)
        mission_row = c.fetchall()
        mission_date = mission_row[0][3]
        conn.close()

        return mission_date
    except sqlite3.OperationalError :
        pass

def get_time_from_id(id) : # Récupere la "time" correspondant à "id"
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Mission WHERE MissionID = ("%s")""" %(id)
        c.execute(sql)
        mission_row = c.fetchall()
        mission_time = mission_row[0][4]
        conn.close()

        return mission_time
    except sqlite3.OperationalError :
        pass

def get_title_from_id(id) : # Récupere le "title" correspondant à "id"
    try :

        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Mission WHERE MissionID = ("%s")""" %(id)
        c.execute(sql)
        mission_row = c.fetchall()
        mission_title = mission_row[0][1]
        conn.close()

        return mission_title
    except sqlite3.OperationalError :
        pass

def get_type_from_id(id) : # Récupere le "type" correspondant à "id"
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Mission WHERE MissionID = ("%s")""" %(id)
        c.execute(sql)
        mission_row = c.fetchall()
        mission_type = mission_row[0][2]
        conn.close()

        return mission_type
    except sqlite3.OperationalError :
        pass

def get_description_from_id(id) : # Récupere le "description" correspondant à "id"
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Mission WHERE MissionID = ("%s")""" %(id)
        c.execute(sql)
        mission_row = c.fetchall()
        mission_description = mission_row[0][7]
        conn.close()

        return mission_description
    except sqlite3.OperationalError :
        pass

def get_matos_from_id(id) : # Récupere le "matos" correspondant à "id"
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Mission WHERE MissionID = ("%s")""" %(id)
        c.execute(sql)
        mission_row = c.fetchall()
        mission_matos = mission_row[0][8]
        conn.close()

        return mission_matos
    except sqlite3.OperationalError :
        pass

def get_return_status_from_id(id) : # Récupere le "return status" correspondant à "id"
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Mission WHERE MissionID = ("%s")""" %(id)
        c.execute(sql)
        mission_row = c.fetchall()
        mission_return = mission_row[0][9]
        conn.close()

        return mission_return
    except sqlite3.OperationalError :
        pass

def get_return_date_from_id(id) : # Récupere le "return date" correspondant à "id"
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Mission WHERE MissionID = ("%s")""" %(id)
        c.execute(sql)
        mission_row = c.fetchall()
        mission_return_date = mission_row[0][5]
        conn.close()

        return mission_return_date
    except sqlite3.OperationalError :
        pass

def get_return_time_from_id(id) : # Récupere le "return time" correspondant à "id"
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Mission WHERE MissionID = ("%s")""" %(id)
        c.execute(sql)
        mission_row = c.fetchall()
        mission_return_time = mission_row[0][6]
        conn.close()

        return mission_return_time
    except sqlite3.OperationalError :
        pass

def get_localisation_from_id(id) : # Récupere la "localisation" correspondante à "id"
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Mission WHERE MissionID = ("%s")""" %(id)
        c.execute(sql)
        mission_row = c.fetchall()
        mission_localisation = mission_row[0][10]
        conn.close()

        return mission_localisation
    except sqlite3.OperationalError :
        pass

def get_mission_ids() : # Récupere les Ids de la Table "Mission"
    try :
        mission_ids = []
    
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("SELECT rowid,* FROM Mission")
        missions = c.fetchall()
        conn.close()

        for i in missions :
            mission_ids.append(i[0])

        return mission_ids
    except sqlite3.OperationalError :
        pass

def get_mission_id_from_title_and_date(title, date) : # Récupere l'Id de la Mission fonction de "title" et "date"
    try :
        mission_id = 0

        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Mission WHERE MissionTitle = ("%s") AND MissionDate = ("%s")""" %(title, date)
        c.execute(sql)
        mission = c.fetchall()
        conn.close()

        mission_id = mission[0][0]

        return mission_id
    except sqlite3.OperationalError :
        pass

def create_printable_mission(id) : # Créé un fichier .txt imprimable contenant toutes les informations correspondantes à "id"
    printable_file_name = f"mission{id}.txt"
    PRINT_FILE = os.path.join(DATA_DIR, printable_file_name)

    with open(PRINT_FILE, "w", encoding='utf8') as f :
        f.write("*****************    RECAPITULATIF DE LA MISSION    *****************\n\n")
        f.write("- Titre de la Mission : ")
        f.write(get_title_from_id(id))
        f.write("\n- Type : ")
        if get_type_from_id(id) == 1 :
            f.write("Prêt de Matériel")
        if get_type_from_id(id) == 2 :
            f.write("Montage / Démontage")
        if get_type_from_id(id) == 3 :
            f.write("Technique")
        f.write("\n- Lieu : ")
        f.write(get_localisation_from_id(id))
        f.write("\n\n- Date : ")
        f.write(get_date_from_id(id))
        f.write("                    - Heure : ")
        f.write(get_time_from_id(id))
        if get_return_status_from_id(id) == 1 :
            f.write("\n- Date de Retour : ")
            f.write(get_return_date_from_id(id))
            f.write("          - Heure : ")
            f.write(get_return_time_from_id(id))
        f.write("\n\n- Description de la Mission :\n")
        mission_description = get_description_from_id(id).capitalize()
        f.write('\n'.join(textwrap.wrap(mission_description, 69, break_long_words=False)))
        f.write("\n\n - Matériel Nécessaire :\n")

        mission_matos = get_matos_from_id(id)
        if mission_matos != [""] :
            mission_items = mission_matos.split("\n")
            for item in mission_items :
                f.write(item)
                f.write("\n")
        else :
            f.write("Aucun")
                
        f.close()

## MODIFICATIONS DE LA TABLE MISSION :

def create_new_mission(mission_title, mission_type, mission_date, mission_time, mission_return_date, mission_return_time, mission_description, mission_matos, mission_return, mission_localisation) : # Création d'une nouvelle Row de "Mission"
    try :
        mission_ids = []

        mission_ids = get_mission_ids()
        mission_id = len(mission_ids) + 1

        new_mission = {"MissionID" : mission_id, "MissionTitle" : mission_title, "MissionType" : mission_type, "MissionDate" : mission_date, "MissionTime" : mission_time, "MissionReturnDate" : mission_return_date, "MissionReturnTime" : mission_return_time, "MissionDescription" : mission_description, "MissionMatos" : mission_matos, "MissionReturn" : mission_return, "MissionLocalisation" : mission_localisation}

        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("INSERT INTO Mission VALUES (:MissionID, :MissionTitle, :MissionType, :MissionDate, :MissionTime, :MissionReturnDate, :MissionReturnTime, :MissionDescription, :MissionMatos, :MissionReturn, :MissionLocalisation)", new_mission)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError :
        pass

def cancel_mission_from_id(id) : # Supprime la Row correspondante à "id"
    try :
        sql = """DELETE FROM Mission WHERE MissionID = %s""" %(id)
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError :
        pass

## MODIFICATIONS DE LA TABLE STOCK :

def create_new_stock_item(item, stockCount) : # Création d'une nouvelle Row de "Stock"
    try :
        new_stock_item = {"Item" : item, "StockCount" : stockCount, "PretsCount" : 0}

        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("INSERT INTO Stock VALUES (:Item, :StockCount, :PretsCount)", new_stock_item)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError :
        pass

def modify_stock_item(item, stockCount) : # Modification d'une Row de "Stock"
    try :
        sql = """UPDATE Stock SET StockCount = ("%s") WHERE Item = ("%s")""" %(stockCount, item)
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError :
        pass

def remove_stock_item(item) : # Suppression d'une Row de "Stock"
    try :
        sql = """DELETE FROM Stock WHERE Item = ("%s")""" %(item)
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError :
        pass

## MODIFICATIONS DE LA TABLE STOCK TECHNIQUE :

def create_new_tech_stock_item(item, stockCount) : # Création d'une nouvelle Row de "Tech_Stock"
    try :
        new_tech_stock_item = {"Item" : item, "StockCount" : stockCount, "PretsCount" : 0}

        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("INSERT INTO Tech_Stock VALUES (:Item, :StockCount, :PretsCount)", new_tech_stock_item)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError :
        pass

def modify_tech_stock_item(item, stockCount) : # Modification d'une Row de "Tech_Stock"
    try :
        sql = """UPDATE Tech_Stock SET StockCount = ("%s") WHERE Item = ("%s")""" %(stockCount, item)
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError :
        pass

def remove_tech_stock_item(item) : # Suppression d'une Row de "Tech_Stock"
    try :
        sql = """DELETE FROM Tech_Stock WHERE Item = ("%s")""" %(item)
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError :
        pass

## MODIFICATIONS DE LA TABLE PRETS DE MATERIEL :

def create_prets(localisation, prets_type) : # Création d'une nouvelle Row de "Prets"
    try :
        new_prets = {"Localisation" : localisation, "Type" : prets_type, "ItemLists" : None}

        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("INSERT INTO Prets VALUES (:Localisation, :Type, :ItemLists)", new_prets)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError :
        pass

def update_pret_list(localisation, item_list) : # Modification de ItemList de Row de "Prets"
    try :
        sql = """UPDATE Prets SET ItemLists = ("%s") WHERE Localisation = ("%s")""" %(item_list, localisation)
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError :
        pass

def remove_prets(localisation) : # Suppression d'une Row de "Prets"
    try :
        sql = """DELETE FROM Prets WHERE Localisation = ("%s")""" %(localisation)
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError :
        pass

def empty_total_prets() : # RAZ du total des prets pour nouveau calcul
    try :
        item_names = get_stock_item_names()
        item_tech_names = get_tech_stock_item_names()

        for name in item_names :
            conn = sqlite3.connect(path)
            sql = """UPDATE Stock SET PretsCount = ("%s") WHERE Item = ("%s")""" %(0, name)
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
            conn.close()

        for name in item_tech_names :
            conn = sqlite3.connect(path)
            sql = """UPDATE Tech_Stock SET PretsCount = ("%s") WHERE Item = ("%s")""" %(0, name)
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
            conn.close()
    except sqlite3.OperationalError :
        pass
    except TypeError :
        pass

def calculate_total_prets() : # Calcule de la quantité totale de chaque Item prété
    try :
        empty_total_prets()
        set_to_none()

        stock_items = get_stock_item_names()
        tech_stock_items = get_tech_stock_item_names()

        total_lists = get_prets_lists()
        total_lists_unformated = []
        total_list_separated = []
        items_list = []

        for liste in total_lists :
            if liste != None :
                total_lists_unformated.append(liste)

        for liste in total_lists_unformated :
            total_list_separated.append(liste.split("\n"))

        for i in range(len(total_list_separated)) :
            for item in total_list_separated[i] :
                items_list.append(item)

        for item in items_list :
            item_name = (item.split(" : ")[0])
            item_qty = (item.split(" : ")[1])

            if item_name in stock_items :
                conn = sqlite3.connect(path)
                c = conn.cursor()
                sql = """SELECT * FROM Stock WHERE Item = ("%s")""" %(item_name)
                c.execute(sql)
                item_data = c.fetchall()
                item_old_qty = item_data[0][2]

                item_qty = int(item_qty) + int(item_old_qty)
                sql = """UPDATE Stock SET PretsCount = ("%s") WHERE Item = ("%s")""" %(item_qty, item_name)
                c = conn.cursor()
                c.execute(sql)
                conn.commit()
                conn.close()

            elif item_name in tech_stock_items :
                conn = sqlite3.connect(path)
                c = conn.cursor()
                sql = """SELECT * FROM Tech_Stock WHERE Item = ("%s")""" %(item_name)
                c.execute(sql)
                item_data = c.fetchall()
                item_old_qty = item_data[0][2]

                item_qty = int(item_qty) + int(item_old_qty)
                sql = """UPDATE Tech_Stock SET PretsCount = ("%s") WHERE Item = ("%s")""" %(item_qty, item_name)
                c = conn.cursor()
                c.execute(sql)
                conn.commit()
                conn.close()
    except sqlite3.OperationalError :
        pass
    except TypeError :
        pass

def set_to_none() : # Transforme une liste vide en élément nul
    try :
        conn = sqlite3.connect(path)
        sql = """UPDATE Prets SET ItemLists = NULL WHERE ItemLists = ("%s")""" %("")
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError :
        pass
