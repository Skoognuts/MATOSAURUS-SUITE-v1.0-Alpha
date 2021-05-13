# -*- coding: utf-8 -*-

import os
import sys
import json

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import date, datetime
import textwrap

from api_mat_v_2 import *

CUR_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(CUR_DIR, "data")
ICON_FILE = os.path.join(DATA_DIR, "icone.png")
PATH_FILE = os.path.join(CUR_DIR, "db_path_viewer.json")

class App(QtWidgets.QTabWidget):
    def __init__(self, parent = None): # Initialisation de la fenêtre et des fonctions de départ
        super(App, self).__init__(parent)
        self.setWindowTitle("MATOSAURUS REX  |  v.1.2 - Alpha")
        self.setStyleSheet("background-color: rgb(200, 200, 255)")
        self.setWindowIcon(QtGui.QIcon(ICON_FILE))

        self.tab_mission = QtWidgets.QWidget()
        self.tab_stock = QtWidgets.QWidget()
        self.tab_tech_stock = QtWidgets.QWidget()
        self.tab_pret = QtWidgets.QWidget()
        self.tab_atel = QtWidgets.QWidget()
		
        self.addTab(self.tab_mission," MISSION CONTROL ")
        self.addTab(self.tab_stock," STOCK ")
        self.addTab(self.tab_tech_stock," STOCK TECHNIQUE ")
        self.addTab(self.tab_pret," PRETS DE MATERIEL ")
        self.addTab(self.tab_atel," ATELIER ")
        
        self.tabMissionUI()
        self.tabStockUI()
        self.tabTechStockUI()
        self.tabPretUI()
        self.tabAtelUI()
        self.setup_connections()
        self.setup_default()

        calculate_total_prets()

        self.populate_daily_missions_lw()
        self.populate_create_type_cbb()
        self.populate_create_matos_localisation_cbb()
        self.populate_create_matos_prov_cbb()

        self.populate_stock_lw()

        self.populate_tech_stock_lw()
        self.populate_tech_stock_type_cbb()

        self.populate_prets_localisations_lw()

        self.populate_atel_ref_qty_lw()
        self.populate_atel_search_cbb()

    def tabMissionUI(self): # Génération du Tab "MISSION CONTROL"
        self.grid_layout = QtWidgets.QGridLayout(self)

        ## Création des GroupBox pour la mise en forme

        self.groupBox1 = QtWidgets.QGroupBox(self.tab_mission)
        self.groupBox2 = QtWidgets.QGroupBox(self.tab_mission)
        self.groupBox3 = QtWidgets.QGroupBox(self.tab_mission)

        self.grid_layout.addWidget(self.groupBox1, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.groupBox2, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.groupBox3, 0, 2, 1, 1)

        self.gridLayout1 = QtWidgets.QGridLayout(self.groupBox1)
        self.gridLayout2 = QtWidgets.QGridLayout(self.groupBox2)
        self.gridLayout3 = QtWidgets.QGridLayout(self.groupBox3)

        self.groupBox1.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.groupBox2.setStyleSheet("background-color: rgb(85, 85, 255)")
        self.groupBox3.setStyleSheet("background-color: rgb(150, 150, 255)")

        ## Peuplement du GroupBox 1

        self.calendarWidget = QtWidgets.QCalendarWidget(self.groupBox1)
        self.btn_today = QtWidgets.QPushButton("AUJOURD'HUI", self.groupBox1)
        self.btn_tomorow = QtWidgets.QPushButton("DEMAIN", self.groupBox1)
        self.btn_tdatomorow = QtWidgets.QPushButton("APRES-DEMAIN", self.groupBox1)
        self.lbl_missions_du_jour = QtWidgets.QLabel(" 📂 - MISSIONS DU JOUR :", self.groupBox1)
        self.lw_missions_list = QtWidgets.QListWidget(self.groupBox1)
        self.lbl_legend = QtWidgets.QLabel("🟡 Prêt de Matériel | 🟢 Montage / Démontage | 🟣 Technique", self.groupBox1)
        self.btn_view_calendar = QtWidgets.QPushButton("AFFICHER LE CALENDRIER HEBDOMADAIRE", self.groupBox1)

        self.gridLayout1.addWidget(self.calendarWidget, 0, 0, 1, 3)
        self.gridLayout1.addWidget(self.btn_today, 1, 0, 1, 1)
        self.gridLayout1.addWidget(self.btn_tomorow, 1, 1, 1, 1)
        self.gridLayout1.addWidget(self.btn_tdatomorow, 1, 2, 1, 1)
        self.gridLayout1.addWidget(self.lbl_missions_du_jour, 2, 0, 1, 3)
        self.gridLayout1.addWidget(self.lw_missions_list, 3, 0, 1, 3)
        self.gridLayout1.addWidget(self.lbl_legend, 4, 0, 1, 3)
        self.gridLayout1.addWidget(self.btn_view_calendar, 5, 0, 1, 3)

        self.calendarWidget.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self.btn_today.setStyleSheet("background-color: rgb(200, 200, 255)")
        self.btn_tomorow.setStyleSheet("background-color: rgb(200, 200, 255)")
        self.btn_tdatomorow.setStyleSheet("background-color: rgb(200, 200, 255)")
        self.lbl_missions_du_jour.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.lw_missions_list.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.btn_view_calendar.setStyleSheet("background-color: rgb(255, 255, 100)")
        
        ## Peuplement du GroupBox 2

        self.lbl_mission = QtWidgets.QLabel(" -  M  I  S  S  I  O  N  - ", self.groupBox2)
        self.lbl_mission_date = QtWidgets.QLabel(" 📅 - DATE :", self.groupBox2)
        self.le_mission_date = QtWidgets.QLineEdit(self.groupBox2)
        self.lbl_mission_title = QtWidgets.QLabel(" 📌 - TITRE :", self.groupBox2)
        self.le_mission_title = QtWidgets.QLineEdit(self.groupBox2)
        self.lbl_mission_type = QtWidgets.QLabel(" 🏷 - TYPE :", self.groupBox2)
        self.le_mission_type = QtWidgets.QLineEdit(self.groupBox2)
        self.lbl_mission_localisation = QtWidgets.QLabel(" 📥 - LIEU :", self.groupBox2)
        self.le_mission_localisation = QtWidgets.QLineEdit(self.groupBox2)
        self.lbl_mission_description = QtWidgets.QLabel(" 🖋 - DESCRIPTIF DE LA MISSION :", self.groupBox2)
        self.te_mission_description = QtWidgets.QTextEdit(self.groupBox2)
        self.lbl_materiel_necessaire = QtWidgets.QLabel(" 🖋 - MATERIEL NECESSAIRE :", self.groupBox2)
        self.lw_materiel_necessaire = QtWidgets.QListWidget(self.groupBox2)
        self.btn_mission_modify = QtWidgets.QPushButton("MODIFIER", self.groupBox2)
        self.btn_mission_cancel = QtWidgets.QPushButton("ANNULER", self.groupBox2)
        self.btn_mission_complete = QtWidgets.QPushButton("MISSION ACCOMPLIE", self.groupBox2)
        self.btn_print_mission = QtWidgets.QPushButton("IMPRIMER UN RECAPITULATIF", self.groupBox2)

        self.gridLayout2.addWidget(self.lbl_mission, 0, 0, 1, 3)
        self.gridLayout2.addWidget(self.lbl_mission_date, 1, 0, 1, 1)
        self.gridLayout2.addWidget(self.le_mission_date, 1, 1, 1, 2)
        self.gridLayout2.addWidget(self.lbl_mission_title, 2, 0, 1, 1)
        self.gridLayout2.addWidget(self.le_mission_title, 2, 1, 1, 2)
        self.gridLayout2.addWidget(self.lbl_mission_type, 3, 0, 1, 1)
        self.gridLayout2.addWidget(self.le_mission_type, 3, 1, 1, 2)
        self.gridLayout2.addWidget(self.lbl_mission_localisation, 4, 0, 1, 1)
        self.gridLayout2.addWidget(self.le_mission_localisation, 4, 1, 1, 2)
        self.gridLayout2.addWidget(self.lbl_mission_description, 5, 0, 1, 3)
        self.gridLayout2.addWidget(self.te_mission_description, 6, 0, 1, 3)
        self.gridLayout2.addWidget(self.lbl_materiel_necessaire, 7, 0, 1, 3)
        self.gridLayout2.addWidget(self.lw_materiel_necessaire, 8, 0, 1, 3)
        self.gridLayout2.addWidget(self.btn_mission_modify, 9, 0, 1, 1)
        self.gridLayout2.addWidget(self.btn_mission_cancel, 9, 1, 1, 1)
        self.gridLayout2.addWidget(self.btn_mission_complete, 9, 2, 1, 1)
        self.gridLayout2.addWidget(self.btn_print_mission, 10, 0, 1, 3)

        self.lbl_mission.setStyleSheet("background-color: rgb(255, 255, 0); font: 75 12pt; MS Shell Dlg 2")
        self.lbl_mission.setAlignment(Qt.AlignCenter)
        self.lbl_mission_date.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.le_mission_date.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lbl_mission_title.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.le_mission_title.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lbl_mission_type.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.le_mission_type.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lbl_mission_localisation.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.le_mission_localisation.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lbl_mission_description.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.te_mission_description.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lbl_materiel_necessaire.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.lw_materiel_necessaire.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.btn_mission_modify.setStyleSheet("background-color: rgb(200, 200, 255)")
        self.btn_mission_cancel.setStyleSheet("background-color: rgb(242, 242, 95)")
        self.btn_mission_complete.setStyleSheet("background-color: rgb(255, 100, 100)")
        self.btn_print_mission.setStyleSheet("background-color: rgb(255, 255, 100)")
        self.lw_materiel_necessaire.setAlternatingRowColors(True)

        ## Peuplement du GroupBox 3

        self.lbl_create_mission = QtWidgets.QLabel(" 📂 - CREER UNE MISSION :", self.groupBox3)
        self.lbl_create_mission_title = QtWidgets.QLabel(" 📌 - TITRE :", self.groupBox3)
        self.le_create_mission_title = QtWidgets.QLineEdit(self.groupBox3)
        self.lbl_create_mission_type = QtWidgets.QLabel(" 🏷 - TYPE :", self.groupBox3)
        self.cbb_create_mission_type = QtWidgets.QComboBox(self.groupBox3)
        self.lbl_create_mission_localisation = QtWidgets.QLabel(" 📥 - LIEU :", self.groupBox3)
        self.cbb_create_mission_localisation = QtWidgets.QComboBox(self.groupBox3)
        self.lbl_create_mission_date = QtWidgets.QLabel(" 📅 - DATE :", self.groupBox3)
        self.de_create_mission_date = QtWidgets.QDateEdit(self.groupBox3)
        self.lbl_create_mission_time = QtWidgets.QLabel(" 🕔 - HEURE :", self.groupBox3)
        self.tie_create_mission_time = QtWidgets.QTimeEdit(self.groupBox3)
        self.cb_return = QtWidgets.QCheckBox(" Date et heure de retour", self.groupBox3)
        self.lbl_return_mission_date = QtWidgets.QLabel(" 📅 - DATE :", self.groupBox3)
        self.de_return_mission_date = QtWidgets.QDateEdit(self.groupBox3)
        self.lbl_return_mission_time = QtWidgets.QLabel(" 🕔 - HEURE :", self.groupBox3)
        self.tie_return_mission_time = QtWidgets.QTimeEdit(self.groupBox3)
        self.lbl_create_mission_description = QtWidgets.QLabel(" 🖋 - DESCRIPTIF DE LA MISSION :", self.groupBox3)
        self.te_create_mission_description = QtWidgets.QTextEdit(self.groupBox3)
        self.lbl_create_materiel_necessaire = QtWidgets.QLabel(" 🖋 - MATERIEL NECESSAIRE :", self.groupBox3)
        self.lbl_create_mission_prov = QtWidgets.QLabel(" 📤 - PROVENANCE :", self.groupBox3)
        self.cbb_create_mission_prov = QtWidgets.QComboBox(self.groupBox3)
        self.lbl_create_mission_matos = QtWidgets.QLabel(" 🏷 - MATERIEL :", self.groupBox3)
        self.cbb_create_mission_matos = QtWidgets.QComboBox(self.groupBox3)
        self.lbl_create_mission_qty = QtWidgets.QLabel(" 🧮 - QUANTITE :", self.groupBox3)
        self.sb_create_mission_qty = QtWidgets.QSpinBox(self.groupBox3)
        self.btn_create_mission_qty_max = QtWidgets.QPushButton("MAX", self.groupBox3)
        self.btn_create_mission_add = QtWidgets.QPushButton("AJOUTER", self.groupBox3)
        self.btn_create_mission_modify = QtWidgets.QPushButton("MODIFIER", self.groupBox3)
        self.btn_create_mission_remove = QtWidgets.QPushButton("SUPPRIMER", self.groupBox3)
        self.lw_create_mission_matos = QtWidgets.QListWidget(self.groupBox3)
        self.btn_create_mission_save = QtWidgets.QPushButton("ENREGISTRER", self.groupBox3)
        self.btn_create_mission_erase = QtWidgets.QPushButton("R.A.Z", self.groupBox3)

        self.gridLayout3.addWidget(self.lbl_create_mission, 0, 0, 1, 3)
        self.gridLayout3.addWidget(self.lbl_create_mission_title, 1, 0, 1, 1)
        self.gridLayout3.addWidget(self.le_create_mission_title, 1, 1, 1, 2)
        self.gridLayout3.addWidget(self.lbl_create_mission_type, 2, 0, 1, 1)
        self.gridLayout3.addWidget(self.cbb_create_mission_type, 2, 1, 1, 2)
        self.gridLayout3.addWidget(self.lbl_create_mission_localisation, 3, 0, 1, 1)
        self.gridLayout3.addWidget(self.cbb_create_mission_localisation, 3, 1, 1, 2)
        self.gridLayout3.addWidget(self.lbl_create_mission_date, 4, 0, 1, 1)
        self.gridLayout3.addWidget(self.de_create_mission_date, 4, 1, 1, 2)
        self.gridLayout3.addWidget(self.lbl_create_mission_time, 5, 0, 1, 1)
        self.gridLayout3.addWidget(self.tie_create_mission_time, 5, 1, 1, 2)
        self.gridLayout3.addWidget(self.cb_return, 6, 0, 1, 3)
        self.gridLayout3.addWidget(self.lbl_return_mission_date, 7, 0, 1, 1)
        self.gridLayout3.addWidget(self.de_return_mission_date, 7, 1, 1, 2)
        self.gridLayout3.addWidget(self.lbl_return_mission_time, 8, 0, 1, 1)
        self.gridLayout3.addWidget(self.tie_return_mission_time, 8, 1, 1, 2)
        self.gridLayout3.addWidget(self.lbl_create_mission_description, 9, 0, 1, 3)
        self.gridLayout3.addWidget(self.te_create_mission_description, 10, 0, 1, 3)
        self.gridLayout3.addWidget(self.lbl_create_materiel_necessaire, 11, 0, 1, 3)
        self.gridLayout3.addWidget(self.lbl_create_mission_prov, 12, 0, 1, 1)
        self.gridLayout3.addWidget(self.cbb_create_mission_prov, 12, 1, 1, 2)
        self.gridLayout3.addWidget(self.lbl_create_mission_matos, 13, 0, 1, 1)
        self.gridLayout3.addWidget(self.cbb_create_mission_matos, 13, 1, 1, 2)
        self.gridLayout3.addWidget(self.lbl_create_mission_qty, 14, 0, 1, 1)
        self.gridLayout3.addWidget(self.sb_create_mission_qty, 14, 1, 1, 1)
        self.gridLayout3.addWidget(self.btn_create_mission_qty_max, 14, 2, 1, 1)
        self.gridLayout3.addWidget(self.btn_create_mission_add, 16, 0, 1, 1)
        self.gridLayout3.addWidget(self.btn_create_mission_modify, 16, 1, 1, 1)
        self.gridLayout3.addWidget(self.btn_create_mission_remove, 16, 2, 1, 1)
        self.gridLayout3.addWidget(self.lw_create_mission_matos, 15, 0, 1, 3)
        self.gridLayout3.addWidget(self.btn_create_mission_save, 17, 0, 1, 2)
        self.gridLayout3.addWidget(self.btn_create_mission_erase, 17, 2, 1, 1)

        self.lbl_create_mission.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.lbl_create_mission_title.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.le_create_mission_title.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lbl_create_mission_type.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.cbb_create_mission_type.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lbl_create_mission_localisation.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.cbb_create_mission_localisation.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lbl_create_mission_date.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.de_create_mission_date.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lbl_create_mission_time.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.tie_create_mission_time.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.cb_return.setStyleSheet("background-color: rgb(200, 200, 255)")
        self.lbl_return_mission_date.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.de_return_mission_date.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lbl_return_mission_time.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.tie_return_mission_time.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lbl_create_mission_description.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.te_create_mission_description.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lbl_create_materiel_necessaire.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.lbl_create_mission_prov.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.cbb_create_mission_prov.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lbl_create_mission_matos.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.cbb_create_mission_matos.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lbl_create_mission_qty.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.sb_create_mission_qty.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.btn_create_mission_qty_max.setStyleSheet("background-color: rgb(255, 255, 100)")
        self.btn_create_mission_add.setStyleSheet("background-color: rgb(200, 200, 255)")
        self.btn_create_mission_modify.setStyleSheet("background-color: rgb(200, 200, 255)")
        self.btn_create_mission_remove.setStyleSheet("background-color: rgb(255, 100, 100)")
        self.lw_create_mission_matos.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.btn_create_mission_save.setStyleSheet("background-color: rgb(255, 255, 100)")
        self.btn_create_mission_erase.setStyleSheet("background-color: rgb(255, 100, 100)")
        self.lw_create_mission_matos.setAlternatingRowColors(True)

        ## Affichage du Tab

        self.setTabText(0," MISSION CONTROL ")
        self.tab_mission.setLayout(self.grid_layout)

    def tabStockUI(self): # Génération du Tab "STOCK"
        self.grid_layout = QtWidgets.QGridLayout(self)

        self.lw_stock_ref = QtWidgets.QListWidget()
        self.lw_stock_count = QtWidgets.QListWidget()
        self.lbl_stock_ref = QtWidgets.QLabel("Référence :")
        self.le_stock_ref = QtWidgets.QLineEdit() 
        self.lbl_stock_qty = QtWidgets.QLabel("Quantité : ")
        self.sb_stock_qty = QtWidgets.QSpinBox()
        self.btn_addstock = QtWidgets.QPushButton(" Ajouter au stock ")
        self.btn_modifystock = QtWidgets.QPushButton(" Modifier l'élément ")
        self.btn_rmvstock = QtWidgets.QPushButton(" Retirer du stock ")

        self.grid_layout.addWidget(self.lw_stock_ref, 1, 0, 8, 8)
        self.grid_layout.addWidget(self.lw_stock_count, 1, 8, 8, 2)
        self.grid_layout.addWidget(self.lbl_stock_ref, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.le_stock_ref, 0, 1, 1 , 4)
        self.grid_layout.addWidget(self.lbl_stock_qty, 0, 5, 1, 1)
        self.grid_layout.addWidget(self.sb_stock_qty, 0, 6, 1, 1)
        self.grid_layout.addWidget(self.btn_addstock, 0, 7, 1, 1)
        self.grid_layout.addWidget(self.btn_modifystock, 0, 8, 1, 1)
        self.grid_layout.addWidget(self.btn_rmvstock, 0, 9, 1, 1)

        self.lw_stock_ref.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lw_stock_count.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.le_stock_ref.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.sb_stock_qty.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.btn_addstock.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.btn_modifystock.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.btn_rmvstock.setStyleSheet("background-color: rgb(200, 100, 100)")
        self.lw_stock_ref.setAlternatingRowColors(True)
        self.lw_stock_count.setAlternatingRowColors(True)

        ## Affichage du Tab

        self.setTabText(1," STOCK ")
        self.tab_stock.setLayout(self.grid_layout)

        self.sliderBarS1 = self.lw_stock_ref.verticalScrollBar()
        self.sliderBarS2 = self.lw_stock_count.verticalScrollBar()

        self.sliderBarS1.valueChanged.connect(self.move_stock_scrollbar)
        self.sliderBarS2.valueChanged.connect(self.move_stock_scrollbar)

    def move_stock_scrollbar(self, value): # Synchronisation des SliderBars des ListWidgets du Tab "Stock"
        self.sliderBarS1.setValue(value)
        self.sliderBarS2.setValue(value)

    def tabTechStockUI(self): # Génération du Tab "STOCK TECHNIQUE"
        self.grid_layout = QtWidgets.QGridLayout(self)

        self.lw_Tstock_ref = QtWidgets.QListWidget()
        self.lw_Tstock_count = QtWidgets.QListWidget()
        self.lbl_Tstock_ref = QtWidgets.QLabel("Référence :")
        self.le_Tstock_ref = QtWidgets.QLineEdit()
        self.cbb_Tstock_type = QtWidgets.QComboBox()
        self.lbl_Tstock_qty = QtWidgets.QLabel("Quantité : ")
        self.sb_Tstock_qty = QtWidgets.QSpinBox()
        self.btn_addTstock = QtWidgets.QPushButton(" Ajouter au stock ")
        self.btn_modifyTstock = QtWidgets.QPushButton(" Modifier l'élément ")
        self.btn_rmvTstock = QtWidgets.QPushButton(" Retirer du stock ")

        self.grid_layout.addWidget(self.lw_Tstock_ref, 1, 0, 8, 8)
        self.grid_layout.addWidget(self.lw_Tstock_count, 1, 8, 8, 2)
        self.grid_layout.addWidget(self.lbl_Tstock_ref, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.le_Tstock_ref, 0, 1, 1 , 3)
        self.grid_layout.addWidget(self.cbb_Tstock_type, 0, 4, 1, 1)
        self.grid_layout.addWidget(self.lbl_Tstock_qty, 0, 5, 1, 1)
        self.grid_layout.addWidget(self.sb_Tstock_qty, 0, 6, 1, 1)
        self.grid_layout.addWidget(self.btn_addTstock, 0, 7, 1, 1)
        self.grid_layout.addWidget(self.btn_modifyTstock, 0, 8, 1, 1)
        self.grid_layout.addWidget(self.btn_rmvTstock, 0, 9, 1, 1)

        self.lw_Tstock_ref.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lw_Tstock_count.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.le_Tstock_ref.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.cbb_Tstock_type.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.sb_Tstock_qty.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.btn_addTstock.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.btn_modifyTstock.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.btn_rmvTstock.setStyleSheet("background-color: rgb(200, 100, 100)")
        self.lw_Tstock_ref.setAlternatingRowColors(True)
        self.lw_Tstock_count.setAlternatingRowColors(True)

        ## Affichage du Tab

        self.setTabText(2," STOCK TECHNIQUE ")
        self.tab_tech_stock.setLayout(self.grid_layout)

        self.sliderBarT1 = self.lw_Tstock_ref.verticalScrollBar()
        self.sliderBarT2 = self.lw_Tstock_count.verticalScrollBar()

        self.sliderBarT1.valueChanged.connect(self.move_Tstock_scrollbar)
        self.sliderBarT2.valueChanged.connect(self.move_Tstock_scrollbar)

    def move_Tstock_scrollbar(self, value): # Synchronisation des SliderBars des ListWidgets du Tab "Stock Technique"
        self.sliderBarT1.setValue(value)
        self.sliderBarT2.setValue(value)

    def tabPretUI(self): # Génération du Tab "PRETS DE MATERIEL"
        self.grid_layout = QtWidgets.QGridLayout(self)

        self.lbl_prets_local = QtWidgets.QLabel("Localisations :")
        self.lbl_prets_matos = QtWidgets.QLabel("Matériel prêté :")
        self.lbl_prets_add_name = QtWidgets.QLabel("Créer un Destinataire :")
        self.lbl_prets_name = QtWidgets.QLabel("Nom :")
        self.cb_prets_1 = QtWidgets.QCheckBox(" Récurrent")
        self.cb_prets_2 = QtWidgets.QCheckBox(" Salle")
        self.cb_prets_3 = QtWidgets.QCheckBox(" Asso & Particulier")
        self.le_prets_name = QtWidgets.QLineEdit()
        self.lbl_prets_legend = QtWidgets.QLabel("🟨 Prêts récurents - 🟩 Salles - 🟦 Assos & particuliers")
        self.lw_prets_local = QtWidgets.QListWidget()
        self.lw_prets_matos = QtWidgets.QListWidget()
        self.btn_prets_name_add = QtWidgets.QPushButton(" Ajouter ")
        self.btn_prets_name_cancel = QtWidgets.QPushButton(" Annuler ")
        self.btn_prets_name_remove = QtWidgets.QPushButton(" Supprimer ")

        self.grid_layout.addWidget(self.lbl_prets_local, 0, 0, 1, 4)
        self.grid_layout.addWidget(self.lbl_prets_matos, 0, 4, 1, 3)
        self.grid_layout.addWidget(self.lbl_prets_add_name, 1, 7, 1, 3)
        self.grid_layout.addWidget(self.lbl_prets_name, 2, 7, 1, 1)
        self.grid_layout.addWidget(self.lbl_prets_legend, 20, 1, 1, 6)
        self.grid_layout.addWidget(self.le_prets_name, 2, 8, 1, 2)
        self.grid_layout.addWidget(self.cb_prets_1, 3, 7, 1, 3)
        self.grid_layout.addWidget(self.cb_prets_2, 4, 7, 1, 3)
        self.grid_layout.addWidget(self.cb_prets_3, 5, 7, 1, 3)
        self.grid_layout.addWidget(self.lw_prets_local, 1, 0, 19, 4)
        self.grid_layout.addWidget(self.lw_prets_matos, 1, 4, 19, 3)
        self.grid_layout.addWidget(self.btn_prets_name_add, 6, 8, 1, 1)
        self.grid_layout.addWidget(self.btn_prets_name_cancel, 6, 9, 1, 1)
        self.grid_layout.addWidget(self.btn_prets_name_remove, 20, 0, 1, 1)

        self.lw_prets_local.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lw_prets_matos.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.le_prets_name.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.cb_prets_1.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.cb_prets_2.setStyleSheet("background-color: rgb(200, 255, 200)")
        self.cb_prets_3.setStyleSheet("background-color: rgb(160, 160, 255)")
        self.btn_prets_name_add.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.btn_prets_name_cancel.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.btn_prets_name_remove.setStyleSheet("background-color: rgb(200, 100, 100)")
        self.lw_prets_matos.setAlternatingRowColors(True)

        ## Affichage du Tab

        self.setTabText(3," PRETS DE MATERIEL ")
        self.tab_pret.setLayout(self.grid_layout)

    def tabAtelUI(self): # Génération du Tab "ATELIER"
        self.grid_layout = QtWidgets.QGridLayout(self)

        self.lbl_atel_ref = QtWidgets.QLabel("Références :")
        self.lbl_atel_qty = QtWidgets.QLabel("Quantités :")
        self.lbl_atel_search = QtWidgets.QLabel("Rechercher une Réference 🔍")
        self.lw_atel_ref = QtWidgets.QListWidget()
        self.lw_atel_qty = QtWidgets.QListWidget()
        self.lw_atel_search = QtWidgets.QListWidget()
        self.cbb_atel_ref = QtWidgets.QComboBox()
        self.btn_database = QtWidgets.QPushButton("DATABASE")
        self.btn_update = QtWidgets.QPushButton("ACTUALISER")

        self.grid_layout.addWidget(self.lbl_atel_ref, 0, 0, 1, 5)
        self.grid_layout.addWidget(self.lbl_atel_qty, 0, 5, 1, 1)
        self.grid_layout.addWidget(self.lbl_atel_search, 0, 6, 1, 5)
        self.grid_layout.addWidget(self.lw_atel_ref, 1, 0, 9, 5)
        self.grid_layout.addWidget(self.lw_atel_qty, 1, 5, 9, 1)
        self.grid_layout.addWidget(self.lw_atel_search, 2, 6, 8, 5)
        self.grid_layout.addWidget(self.cbb_atel_ref, 1, 6, 1, 3)
        self.grid_layout.addWidget(self.btn_database, 1, 9, 1, 1)
        self.grid_layout.addWidget(self.btn_update, 1, 10, 1, 1)

        for i in range(10) :
            self.grid_layout.setRowStretch(i, 4)
        self.grid_layout.setRowStretch(0, 1)
        self.grid_layout.setRowStretch(9, 1)
        for i in range(11) :
            self.grid_layout.setColumnStretch(i, 2)
        self.grid_layout.setColumnStretch(5, 1)

        self.lw_atel_ref.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lw_atel_qty.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lw_atel_search.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.cbb_atel_ref.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.btn_database.setStyleSheet("background-color: rgb(100, 255, 100)")
        self.btn_update.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.lw_atel_ref.setAlternatingRowColors(True)
        self.lw_atel_qty.setAlternatingRowColors(True)
        self.lw_atel_search.setAlternatingRowColors(True)

        ## Affichage du Tab

        self.setTabText(4," ATELIER ")
        self.tab_atel.setLayout(self.grid_layout)

        self.sliderBarA1 = self.lw_atel_ref.verticalScrollBar()
        self.sliderBarA2 = self.lw_atel_qty.verticalScrollBar()

        self.sliderBarA1.valueChanged.connect(self.move_atel_scrollbar)
        self.sliderBarA2.valueChanged.connect(self.move_atel_scrollbar)

    def move_atel_scrollbar(self, value): # Synchronisation des SliderBars des ListWidgets du Tab "Atelier"
        self.sliderBarA1.setValue(value)
        self.sliderBarA2.setValue(value)

    def setup_connections(self): # Initialisation des connections Widgets - Fonctions
        self.btn_today.clicked.connect(self.mission_today)
        self.btn_tomorow.clicked.connect(self.mission_tomorow)
        self.btn_tdatomorow.clicked.connect(self.mission_tdatomorow)
        self.btn_view_calendar.clicked.connect(self.openCalendarView)
        self.btn_mission_modify.clicked.connect(self.mission_modify)
        self.btn_mission_cancel.clicked.connect(self.mission_cancel)
        self.btn_mission_complete.clicked.connect(self.mission_complete)
        self.btn_print_mission.clicked.connect(self.print_mission)
        self.btn_create_mission_qty_max.clicked.connect(self.create_mission_qty_max)
        self.btn_create_mission_add.clicked.connect(self.create_mission_add)
        self.btn_create_mission_modify.clicked.connect(self.create_mission_modify)
        self.btn_create_mission_remove.clicked.connect(self.create_mission_remove)
        self.btn_create_mission_save.clicked.connect(self.create_mission_save)
        self.btn_create_mission_erase.clicked.connect(self.create_mission_raz)
        self.cb_return.clicked.connect(self.cb_return_enable)
        self.calendarWidget.selectionChanged.connect(self.populate_daily_missions_lw)
        self.lw_missions_list.itemClicked.connect(self.populate_mission_widgets)
        self.cbb_create_mission_prov.activated.connect(self.populate_create_matos_items_cbb)
        self.cbb_create_mission_matos.activated.connect(self.populate_create_matos_qty_sb)

        self.btn_addstock.clicked.connect(self.add_to_stock)
        self.btn_modifystock.clicked.connect(self.modify_stock)
        self.btn_rmvstock.clicked.connect(self.remove_from_stock)

        self.btn_addTstock.clicked.connect(self.add_to_tech_stock)
        self.btn_modifyTstock.clicked.connect(self.modify_tech_stock)
        self.btn_rmvTstock.clicked.connect(self.remove_from_tech_stock)
        
        self.btn_prets_name_add.clicked.connect(self.prets_add)
        self.btn_prets_name_cancel.clicked.connect(self.prets_cancel)
        self.btn_prets_name_remove.clicked.connect(self.prets_remove)
        self.lw_prets_local.itemClicked.connect(self.populate_prets_lists_lw)
        self.cb_prets_1.clicked.connect(self.checkbox1_gestion)
        self.cb_prets_2.clicked.connect(self.checkbox2_gestion)
        self.cb_prets_3.clicked.connect(self.checkbox3_gestion)

        self.cbb_atel_ref.activated.connect(self.populate_atel_search_lw)
        self.btn_database.clicked.connect(self.get_database)
        self.btn_update.clicked.connect(self.update)

    def setup_default(self): # Définition des valeurs de Widget par défaut
        self.le_mission_date.setReadOnly(True)
        self.le_mission_title.setReadOnly(True)
        self.le_mission_type.setReadOnly(True)
        self.le_mission_localisation.setReadOnly(True)
        self.de_create_mission_date.setDate(QDate.currentDate())
        self.tie_create_mission_time.setTime(QTime.fromString("12:00"))
        self.de_return_mission_date.setDate(QDate.currentDate())
        self.tie_return_mission_time.setTime(QTime.fromString("12:00"))
        self.de_return_mission_date.setMinimumDate(QDate.fromString(self.de_create_mission_date.text()))
        self.te_mission_description.setReadOnly(True)
        self.de_return_mission_date.setEnabled(False)
        self.tie_return_mission_time.setEnabled(False)
        self.sb_create_mission_qty.setRange(0, 0)

        self.sb_stock_qty.setRange(1, 1000000)

        self.sb_Tstock_qty.setRange(1, 1000000)

### "MISSION CONTROL" TAB METHODS #####################################################

    def mission_today(self): # BTN "Aujourd'hui" du Tab "Mission Control"
        self.calendarWidget.showToday()
        date = QDate.currentDate()
        self.calendarWidget.setSelectedDate(date)

    def mission_tomorow(self): # BTN "Demain" du Tab "Mission Control"
        date = QDate.currentDate().addDays(1)
        self.calendarWidget.setSelectedDate(date)
        self.calendarWidget.showSelectedDate()

    def mission_tdatomorow(self): # BTN "Apres Demain" du Tab "Mission Control"
        date = QDate.currentDate().addDays(2)
        self.calendarWidget.setSelectedDate(date)
        self.calendarWidget.showSelectedDate()

    def openCalendarView(self): # BTN "Ouverture du Calendrier Hebdomadaire" du Tab "Mission Control"
        self.w = CalendarView()
        self.w.show()

    def mission_modify(self): # BTN "Modifier Mission" du Tab "Mission Control"
        for selected_mission in self.lw_missions_list.selectedItems() :
            selected_mission_unformated = selected_mission.text()

        if self.lw_missions_list.selectedItems() == [] :
            return False
        
        self.cbb_create_mission_type.setCurrentText("")
        self.cbb_create_mission_localisation.setCurrentText("")
        self.de_create_mission_date.clear()
        self.tie_create_mission_time.clear()
        self.te_create_mission_description.clear()
        self.lw_create_mission_matos.clear()
        
        if selected_mission_unformated.startswith("🟡") :
            selected_mission_formated = selected_mission_unformated.lstrip("🟡 ")
        if selected_mission_unformated.startswith("🟢") :
            selected_mission_formated = selected_mission_unformated.lstrip("🟢 ")
        if selected_mission_unformated.startswith("🟣") :
            selected_mission_formated = selected_mission_unformated.lstrip("🟣 ")

        selected_date = self.calendarWidget.selectedDate()
        selected_date_formated = self.translate_date(selected_date)

        missions_ids = get_ids_from_date(selected_date_formated)

        for mission_id in missions_ids :
            mission_title = get_title_from_id(mission_id)
            if mission_title == selected_mission_formated :
                mission_date = get_date_from_id(mission_id)
                mission_time = get_time_from_id(mission_id)
                mission_type = get_type_from_id(mission_id)
                mission_localisation = get_localisation_from_id(mission_id)
                mission_description = get_description_from_id(mission_id)
                mission_matos = get_matos_from_id(mission_id)
                mission_return_status = get_return_status_from_id(mission_id)
                mission_return_date = get_return_date_from_id(mission_id)
                mission_return_time = get_return_time_from_id(mission_id)

                self.le_create_mission_title.setText(mission_title)

                if mission_type == 1 :
                    self.cbb_create_mission_type.setCurrentText("🟡 Prêt de Matériel")
                if mission_type == 2 :
                    self.cbb_create_mission_type.setCurrentText("🟢 Montage / Démontage")
                if mission_type == 3 :
                    self.cbb_create_mission_type.setCurrentText("🟣 Technique")

                self.cbb_create_mission_localisation.setCurrentText(mission_localisation)

                self.de_create_mission_date.setDate(selected_date)

                time = QTime.fromString(mission_time)
                self.tie_create_mission_time.setTime(time)

                if mission_return_status == 0 :
                    self.cb_return.setChecked(False)
                elif mission_return_status == 1 :
                    self.cb_return.setChecked(True)
                self.cb_return_enable()
                
                return_date = QDate.fromString(mission_return_date)
                self.de_return_mission_date.setDate(return_date)

                return_time = QTime.fromString(mission_return_time)
                self.tie_return_mission_time.setTime(return_time)

                self.te_create_mission_description.setText(mission_description)

                if mission_matos != None :
                    mission_matos_formated = mission_matos.split("\n")
                else :
                    mission_matos_formated = []
                for matos in mission_matos_formated :
                    self.lw_create_mission_matos.addItem(matos)

    def mission_cancel(self): # BTN "Annuler Mission" du Tab "Mission Control"
        if not self.lw_missions_list.selectedItems() :
            return False

        for selected_mission in self.lw_missions_list.selectedItems() :
            selected_mission_unformated = selected_mission.text()

        if selected_mission_unformated.startswith("🟡") :
            selected_mission_formated = selected_mission_unformated.lstrip("🟡 ")
        if selected_mission_unformated.startswith("🟢") :
            selected_mission_formated = selected_mission_unformated.lstrip("🟢 ")
        if selected_mission_unformated.startswith("🟣") :
            selected_mission_formated = selected_mission_unformated.lstrip("🟣 ")

        selected_date_unformated = self.calendarWidget.selectedDate()
        selected_date = self.translate_date(selected_date_unformated)
        missions_ids = get_ids_from_date(selected_date)

        for mission_id in missions_ids :
            mission_title = get_title_from_id(mission_id)
            if mission_title == selected_mission_formated :
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText("Le matériel ne sera pas déplacé.       \nAnnuler quand même ?")
                msgBox.setWindowTitle("ANNULER LA MISSION")
                msgBox.setWindowIcon(QtGui.QIcon(ICON_FILE))
                msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

                returnValue = msgBox.exec()
                if returnValue == QMessageBox.Ok:
                    cancel_mission_from_id(mission_id)

                self.populate_daily_missions_lw()
                self.raz_mission_widgets()

    def mission_complete(self): # BTN "Mission Accomplie" du Tab "Mission Control"
        for selected_mission in self.lw_missions_list.selectedItems() :
            selected_mission_unformated = selected_mission.text()

        if self.lw_missions_list.selectedItems() == [] :
            return False

        if selected_mission_unformated.startswith("🟡") :
            selected_mission_formated = selected_mission_unformated.lstrip("🟡 ")
        if selected_mission_unformated.startswith("🟢") :
            selected_mission_formated = selected_mission_unformated.lstrip("🟢 ")
        if selected_mission_unformated.startswith("🟣") :
            selected_mission_formated = selected_mission_unformated.lstrip("🟣 ")

        selected_date = self.calendarWidget.selectedDate()
        selected_date_formated = self.translate_date(selected_date)

        mission_id = get_mission_id_from_title_and_date(selected_mission_formated, selected_date_formated)
        mission_title = get_title_from_id(mission_id)

        if mission_title == selected_mission_formated :
            mission_localisation = get_localisation_from_id(mission_id)
            mission_matos_unformated = get_matos_from_id(mission_id)
            mission_matos = mission_matos_unformated.split("\n")

            if mission_matos != False :
                for item in mission_matos :
                    prov = item.split(" --> ")[0]
                    ref_and_count = item.split(" --> ")[1]
                    ref = ref_and_count.split(" : ")[1]
                    count = ref_and_count.split(" : ")[0]
            
                    if mission_localisation == "Atelier" :
                        self.rmv_from_elsewhere(prov, ref, count)
                    elif mission_localisation != prov :
                        if prov == "Atelier" :
                            self.add_from_atel(ref, count, mission_localisation)
                        else :
                            self.add_from_elsewhere(prov, ref, count, mission_localisation)

            cancel_mission_from_id(mission_id)
            calculate_total_prets()
            self.populate_daily_missions_lw()
            self.raz_mission_widgets()
            self.create_mission_raz()
            self.populate_prets_localisations_lw()
            self.populate_prets_lists_lw()
            self.populate_atel_ref_qty_lw()
            self.populate_atel_search_cbb()
            self.lw_atel_search.clear()

    def add_from_atel(self, ref, count, mission_localisation): # Ajoute les items à la nouvelle localisation en provenance de l'Atelier
        dest_list_unformated = get_one_prets_list(mission_localisation)
        print(dest_list_unformated)
        dest_list = []

        if dest_list_unformated != None :
            dest_list = dest_list_unformated.split("\n")

            for item in dest_list :
                if ref == (item.split(" : ")[0]) :
                    item_qty = int(item.split(" : ")[1])
                    add_qty = item_qty + int(count)
                    dest_list.remove(item)
                    new_item = """%s : %s""" %(ref, add_qty)
                elif ref != (item.split(" : ")[0]) :
                    add_qty = int(count)
                    new_item = """%s : %s""" %(ref, add_qty)
        else :
            add_qty = int(count)
            new_item = """%s : %s""" %(ref, add_qty)

        dest_list.append(new_item)
        dest_list_formated = "\n".join(dest_list)
        update_pret_list(mission_localisation, dest_list_formated)

    def add_from_elsewhere(self, prov, ref, count, mission_localisation): # Ajoute les items à la nouvelle localisation en provenance d'ailleur
        dest_list_unformated = get_one_prets_list(mission_localisation)
        dest_list = []

        prov_list_unformated = get_one_prets_list(prov)
        prov_list = []

        prov_list = prov_list_unformated.split("\n")
        new_qty = 0

        for item in prov_list :
            if ref == (item.split(" : ")[0]) :
                item_qty = int(item.split(" : ")[1])
                new_qty = item_qty - int(count)
                prov_list.remove(item)
                new_item = """%s : %s""" %(ref, new_qty)
        
        if new_qty != 0 :
            prov_list.append(new_item)

        if dest_list_unformated != None :
            dest_list = dest_list_unformated.split("\n")

            for item in dest_list :
                if ref == (item.split(" : ")[0]) :
                    item_qty = int(item.split(" : ")[1])
                    add_qty = item_qty + int(count)
                    dest_list.remove(item)
                    new_item = """%s : %s""" %(ref, add_qty)
                elif ref != (item.split(" : ")[0]) :
                    add_qty = int(count)
                    new_item = """%s : %s""" %(ref, add_qty)
        else :
            add_qty = int(count)
            new_item = """%s : %s""" %(ref, add_qty)
        
        dest_list.append(new_item)
        prov_list_formated = "\n".join(prov_list)
        dest_list_formated = "\n".join(dest_list)

        update_pret_list(prov, prov_list_formated)
        update_pret_list(mission_localisation, dest_list_formated)

    def rmv_from_elsewhere(self, prov, ref, count):
        prov_list_unformated = get_one_prets_list(prov)
        prov_list = []

        prov_list = prov_list_unformated.split("\n")
        new_qty = 0

        for item in prov_list :
            if ref == (item.split(" : ")[0]) :
                item_qty = int(item.split(" : ")[1])
                new_qty = item_qty - int(count)
                prov_list.remove(item)
                new_item = """%s : %s""" %(ref, new_qty)

        if new_qty != 0 :
            prov_list.append(new_item)

        prov_list_formated = "\n".join(prov_list)
        update_pret_list(prov, prov_list_formated)

    def print_mission(self, id): # BTN "Imprimer Recapitulatif" du Tab "Mission Control"
        if not self.lw_missions_list.selectedItems() :
            return False
        
        for selected_mission in self.lw_missions_list.selectedItems() :
            selected_mission_unformated = selected_mission.text()

        if selected_mission_unformated.startswith("🟡") :
            selected_mission_formated = selected_mission_unformated.lstrip("🟡 ")
        if selected_mission_unformated.startswith("🟢") :
            selected_mission_formated = selected_mission_unformated.lstrip("🟢 ")
        if selected_mission_unformated.startswith("🟣") :
            selected_mission_formated = selected_mission_unformated.lstrip("🟣 ")

        selected_date_unformated = self.calendarWidget.selectedDate()
        selected_date = self.translate_date(selected_date_unformated)
        missions_ids = get_ids_from_date(selected_date)

        for mission_id in missions_ids :
            mission_title = get_title_from_id(mission_id)
            if mission_title == selected_mission_formated :
                create_printable_mission(mission_id)

                printable_file_name = f"mission{mission_id}.txt"
                PRINT_FILE = os.path.join(DATA_DIR, printable_file_name)
                os.startfile(PRINT_FILE)

                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText("Le document est il imprimé avec succés ?")
                msgBox.setWindowTitle("IMPRIMER UN RECAPITULATIF")
                msgBox.setWindowIcon(QtGui.QIcon(ICON_FILE))
                msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

                returnValue = msgBox.exec()
                if returnValue == QMessageBox.Ok:
                    os.remove(PRINT_FILE)

    def create_mission_qty_max(self): # BTN "MAX" du Tab "Mission Control" pour "prov" != "Atelier"
        prov = self.cbb_create_mission_prov.currentText()
        matos = self.cbb_create_mission_matos.currentText()

        if matos == "" :
            return False
        if prov == "" :
            return False
        elif prov == "- Atelier -" :
            self.create_mission_qty_max_atelier()
        else :
            pret_list = get_one_prets_list(prov)
            item_list = pret_list.split("\n")

            for item in item_list :
                if (item.split(" : "))[0] == matos :
                    item_qty = (item.split(" : "))[1]
            
                    self.sb_create_mission_qty.setValue(int(item_qty))

    def create_mission_qty_max_atelier(self): # BTN "MAX" du Tab "Mission Control" pour "prov" = "Atelier"
        matos = self.cbb_create_mission_matos.currentText()
        if matos == "" :
            return False

        stock_items_list = get_stock_item_names()
        tech_stock_items_list = get_tech_stock_item_names()
        for i in stock_items_list :
            if matos == i :
                item_qty = get_one_stock_atelCount(matos)
        for i in tech_stock_items_list :
            if matos == i :
                item_qty = get_one_tech_stock_atelCount(matos)
        
        self.sb_create_mission_qty.setValue(item_qty)

    def create_mission_add(self): # BTN "Ajouter Materiel" du Tab "Mission Control"
        add_from = self.cbb_create_mission_prov.currentText()
        add_what = self.cbb_create_mission_matos.currentText()
        add_qty = self.sb_create_mission_qty.value()
        dest = self.cbb_create_mission_localisation.currentText()

        if add_from == "" :
            return False
        elif add_what == "" :
            return False
        elif add_from == dest :
            return False
        
        if self.le_create_mission_title.text() == "" :
            return False
        if self.cbb_create_mission_type.currentText() == "" :
            return False
        if self.cbb_create_mission_localisation.currentText() == "" :
            return False

        if add_from == "- Atelier -" :
            add_from = "Atelier"

        new_lw_item = """%s --> %s : %s""" %(add_from, add_qty, add_what)

        self.lw_create_mission_matos.addItem(new_lw_item)

    def create_mission_modify(self): # BTN "Modifier Materiel" du Tab "Mission Control"
        if not self.lw_create_mission_matos.selectedItems() :
            return False

        self.cbb_create_mission_matos.clear()
        self.sb_create_mission_qty.clear()

        for selected_item in self.lw_create_mission_matos.selectedItems() :
            selected_ref = selected_item.text()

        selected_ref_prov_unformated = selected_ref.split(" --> ")[0]
        if selected_ref_prov_unformated == "Atelier" :
            selected_ref_prov = "- Atelier -"
        else :
            selected_ref_prov = selected_ref_prov_unformated

        selected_ref_qty_and_ref = selected_ref.split(" --> ")[1]

        selected_ref_qty = selected_ref_qty_and_ref.split(" : ")[0]

        selected_ref_matos = selected_ref_qty_and_ref.split(" : ")[1]

        self.cbb_create_mission_prov.setCurrentText(selected_ref_prov)
        self.populate_create_matos_items_cbb()
        self.cbb_create_mission_matos.setCurrentText(selected_ref_matos)
        self.populate_create_matos_qty_sb()
        self.sb_create_mission_qty.setValue(int(selected_ref_qty))
        
        self.lw_create_mission_matos.takeItem(self.lw_create_mission_matos.row(selected_item))

    def create_mission_remove(self): # BTN "Supprimer Materiel" du Tab "Mission Control"
        if not self.lw_create_mission_matos.selectedItems() :
            return False
        
        for selected_item in self.lw_create_mission_matos.selectedItems() :
            selected_ref = selected_item.text()

        self.lw_create_mission_matos.takeItem(self.lw_create_mission_matos.row(selected_item))

    def create_mission_save(self): # BTN "Enregistrer" du Tab "Mission Control"
        mission_title = self.le_create_mission_title.text()
        mission_type = self.cbb_create_mission_type.currentText()
        mission_localisation = self.cbb_create_mission_localisation.currentText()
        mission_date = self.de_create_mission_date.text()
        mission_time = self.tie_create_mission_time.text()
        mission_description = self.te_create_mission_description.toPlainText().capitalize()
        mission_matos = []
        mission_ids = []
        mission_matos_formated = ""
        for i in range(self.lw_create_mission_matos.count()):
            mission_matos.append(self.lw_create_mission_matos.item(i).text())
        mission_matos_formated = "\n".join(mission_matos)

        if mission_title == "" :
            return False
        if mission_type == "" :
            return False
        if mission_type.startswith("🟡") :
            mission_type_formated = 1
        if mission_type.startswith("🟢") :
            mission_type_formated = 2
        if mission_type.startswith("🟣") :
            mission_type_formated = 3
        if mission_localisation == "" :
            return False
        if mission_localisation == "- Atelier -" :
            mission_localisation = "Atelier"
        if self.cb_return.isChecked() == False:
            mission_return = 0
            mission_return_date = None
            mission_return_time = None
        else :
            mission_return = 1
            mission_return_date = self.de_return_mission_date.text()
            mission_return_time = self.tie_return_mission_time.text()
        
        mission_ids = get_mission_ids()

        try :
            mission_id = get_mission_id_from_title_and_date(mission_title, mission_date)
            cancel_mission_from_id(mission_id)
            create_new_mission(mission_title.title(), mission_type_formated, mission_date, mission_time, mission_return_date, mission_return_time, mission_description, mission_matos_formated, mission_return, mission_localisation)
        except IndexError :
            try :
                self.lw_missions_list.clear()
                selected_date = self.calendarWidget.selectedDate()
                selected_date_formated = self.translate_date(selected_date)

                mission_id = get_mission_id_from_title_and_date(mission_title, selected_date_formated)
                cancel_mission_from_id(mission_id)
                create_new_mission(mission_title.title(), mission_type_formated, mission_date, mission_time, mission_return_date, mission_return_time, mission_description, mission_matos_formated, mission_return, mission_localisation)
            except :
                create_new_mission(mission_title.title(), mission_type_formated, mission_date, mission_time, mission_return_date, mission_return_time, mission_description, mission_matos_formated, mission_return, mission_localisation)

        self.populate_daily_missions_lw()
        self.raz_mission_widgets()
        self.create_mission_raz()

    def create_mission_raz(self): # BTN "RAZ" du Tab "Mission Control"
        self.le_create_mission_title.clear()
        self.cbb_create_mission_type.setCurrentText("")
        self.cbb_create_mission_localisation.setCurrentText("")
        self.de_create_mission_date.setDate(QDate.currentDate())
        self.tie_create_mission_time.setTime(QTime.fromString("12:00"))
        self.de_return_mission_date.setDate(QDate.currentDate())
        self.tie_return_mission_time.setTime(QTime.fromString("12:00"))
        self.cb_return.setChecked(False)
        self.cb_return_enable()
        self.te_create_mission_description.clear()
        self.cbb_create_mission_prov.setCurrentText("")
        self.cbb_create_mission_matos.setCurrentText("")
        self.sb_create_mission_qty.setRange(0, 0)
        self.lw_create_mission_matos.clear()

    def translate_date(self, date): # Conversion du format de date
        year = date.toString().split(" ")[3]
        month = date.toString().split(" ")[1]
        day = date.toString().split(" ")[2]
        if month == "janv." :
            f_month = "01"
        if month == "févr." :
            f_month = "02"
        if month == "mars" :
            f_month = "03"
        if month == "avr." :
            f_month = "04"
        if month == "mai" :
            f_month = "05"
        if month == "juin." :
            f_month = "06"
        if month == "juil." :
            f_month = "07"
        if month == "août" :
            f_month = "08"
        if month == "sept." :
            f_month = "09"
        if month == "oct." :
            f_month = "10"
        if month == "nov." :
            f_month = "11"
        if month == "déc." :
            f_month = "12"
        selected_date_formated = """%s/%s/%s""" %(day, f_month, year)

        return selected_date_formated

    def populate_daily_missions_lw(self): # Peuplement du ListWidget des Missions du Jour du Tab "Mission Control"
        try :
            self.lw_missions_list.clear()
            selected_date = self.calendarWidget.selectedDate()

            selected_date_formated = self.translate_date(selected_date)

            missions_ids = get_ids_from_date(selected_date_formated)
            missions = []

            for mission_id in missions_ids :
                mission_title = get_title_from_id(mission_id)
                mission_type = get_type_from_id(mission_id)
                if mission_type == 1 :
                    mission_formated_title = """🟡 %s""" %(mission_title)
                if mission_type == 2 :
                    mission_formated_title = """🟢 %s""" %(mission_title)
                if mission_type == 3 :
                    mission_formated_title = """🟣 %s""" %(mission_title)
                missions.append(mission_formated_title)

            self.lw_missions_list.addItems(missions)
        except TypeError :
            pass

    def populate_mission_widgets(self): # Peuplement des Widgets de description de la Mission selectionnée du Tab "Mission Control"
        self.raz_mission_widgets()

        for selected_mission in self.lw_missions_list.selectedItems() :
            selected_mission_unformated = selected_mission.text()

        if selected_mission_unformated.startswith("🟡") :
            selected_mission_formated = selected_mission_unformated.lstrip("🟡 ")
        if selected_mission_unformated.startswith("🟢") :
            selected_mission_formated = selected_mission_unformated.lstrip("🟢 ")
        if selected_mission_unformated.startswith("🟣") :
            selected_mission_formated = selected_mission_unformated.lstrip("🟣 ")

        selected_date = self.calendarWidget.selectedDate()
        selected_date_formated = self.translate_date(selected_date)

        missions_ids = get_ids_from_date(selected_date_formated)

        for mission_id in missions_ids :
            mission_title = get_title_from_id(mission_id)
            if mission_title == selected_mission_formated :
                mission_type_unformated = get_type_from_id(mission_id)
                mission_localisation = get_localisation_from_id(mission_id)

                if mission_type_unformated == 1 :
                    mission_type = "🟡 Prêt de Matériel"
                if mission_type_unformated == 2 :
                    mission_type = "🟢 Montage / Démontage"
                if mission_type_unformated == 3 :
                    mission_type = "🟣 Technique"

                mission_description_text = get_description_from_id(mission_id)
                mission_time = get_time_from_id(mission_id)
                mission_description = []
                mission_description.append(mission_time)
                mission_description.append(mission_description_text)

                mission_return_status = get_return_status_from_id(mission_id)
                if mission_return_status != 0 :
                    mission_return_date = get_return_date_from_id(mission_id)
                    mission_return_time = get_return_time_from_id(mission_id)
                    mission_description.append("""Retour le %s""" %(mission_return_date))
                    mission_description.append("""A %s""" %(mission_return_time))

                mission_matos = get_matos_from_id(mission_id)
                if mission_matos != None :
                    mission_matos_formated = mission_matos.split("\n")
                else :
                    mission_matos_formated = []

                self.le_mission_date.setText(selected_date_formated)
                self.le_mission_title.setText(mission_title)
                self.le_mission_type.setText(mission_type)
                self.le_mission_localisation.setText(mission_localisation)
                mission_description_formated = "\n".join(mission_description)
                self.te_mission_description.setText(mission_description_formated)

                for matos in mission_matos_formated :
                    self.lw_materiel_necessaire.addItem(matos)

    def raz_mission_widgets(self): # Remise à zero des Widgets de description de la Mission du Tab "Mission Control"
        self.le_mission_date.clear()
        self.le_mission_title.clear()
        self.le_mission_type.clear()
        self.le_mission_localisation.clear()
        self.te_mission_description.clear()
        self.lw_materiel_necessaire.clear()

    def populate_create_type_cbb(self): # Peuplement du ComboBox de Création de Type de Mission du Tab "Mission Control"
        self.cbb_create_mission_type.clear()
        mission_types = ["", "🟡 Prêt de Matériel", "🟢 Montage / Démontage", "🟣 Technique"]

        self.cbb_create_mission_type.addItems(mission_types)

    def populate_create_matos_localisation_cbb(self): # Peuplement du ComboBox Localisation de Mission du Tab "Mission Control"
        try :
            self.cbb_create_mission_localisation.clear()
            matos_localisation = ["", "- Atelier -"]

            prets_localisations = get_prets_localisations()
            for localisation in prets_localisations :
                matos_localisation.append(localisation)

            self.cbb_create_mission_localisation.addItems(sorted(matos_localisation))
        except TypeError :
            pass

    def populate_create_matos_prov_cbb(self): # Peuplement du ComboBox de Création de Provenance de Matériel du Tab "Mission Control"
        try :
            self.cbb_create_mission_prov.clear()
            matos_prov = ["", "- Atelier -"]

            prets_localisations = get_prets_localisations()
            for localisation in prets_localisations :
                matos_prov.append(localisation)

            self.cbb_create_mission_prov.addItems(sorted(matos_prov))
        except TypeError :
            pass

    def populate_create_matos_items_cbb(self): # Peuplement du ComboBox de liste Matériel si "prov" != "Atelier" du Tab "Mission Control"
        self.cbb_create_mission_matos.clear()
        pret_list = [""]
        
        pret_prov = self.cbb_create_mission_prov.currentText()
        if not pret_prov :
            return False
        if pret_prov == "- Atelier -" :
            self.populate_create_matos_atelier_items_cbb()
            return False
        if (get_one_prets_list(pret_prov)) == None :
            return False
        else :
            pret_total_list = (get_one_prets_list(pret_prov)).split("\n")
            for item in pret_total_list :
                pret_list.append(item.split(" : ")[0])
            for i in sorted(pret_list) :
                self.cbb_create_mission_matos.addItem(i)

    def populate_create_matos_atelier_items_cbb(self): # Peuplement du ComboBox de liste Matériel si "prov" = "Atelier" du Tab "Mission Control"
        self.cbb_create_mission_matos.clear()
        matos_list = [""]
        tech_matos_list = []
        
        atel_items_list = get_nonull_atelCount_items()
        for i in range(len(atel_items_list)) :
            matos_list.append(atel_items_list[i][0])
        for matos in sorted(matos_list) :
            self.cbb_create_mission_matos.addItem(matos)

        tech_atel_items_list = get_nonull_tech_atelCount_items()
        for i in range(len(tech_atel_items_list)) :
            tech_matos_list.append(tech_atel_items_list[i][0])
        for matos in sorted(tech_matos_list) :
            self.cbb_create_mission_matos.addItem(matos)

    def populate_create_matos_qty_sb(self): # Peuplement du SpinBox de Quantité de Matériel fonction de "prov" si "prov" != "Atelier" du Tab "Mission Control"
        self.sb_create_mission_qty.setRange(0,0)
        
        prov = self.cbb_create_mission_prov.currentText()
        matos = self.cbb_create_mission_matos.currentText()

        if prov == "" :
            return False
        elif prov == "- Atelier -" :
            self.populate_create_matos_atelier_qty_sb()
        else :
            pret_list = get_one_prets_list(prov)

            item_list = pret_list.split("\n")
            for item in item_list :
                if (item.split(" : "))[0] == matos :
                    item_upRange = (item.split(" : "))[1]
            
                    self.sb_create_mission_qty.setRange(1, int(item_upRange))

    def populate_create_matos_atelier_qty_sb(self): # Peuplement du SpinBox de Quantité de Matériel fonction de "prov" si "prov" = "Atelier" du Tab "Mission Control"
        self.sb_create_mission_qty.setRange(0,0)
        
        matos = self.cbb_create_mission_matos.currentText()
        if matos == "" :
            return False

        stock_items_list = get_stock_item_names()
        tech_stock_items_list = get_tech_stock_item_names()
        for i in stock_items_list :
            if matos == i :
                item_upRange = get_one_stock_atelCount(matos)
        for i in tech_stock_items_list :
            if matos == i :
                item_upRange = get_one_tech_stock_atelCount(matos)

        self.sb_create_mission_qty.setRange(1, item_upRange)

    def cb_return_enable(self): # Activation des Inputs de Date et Heure de Retour si CheckBox est activée
        if self.cb_return.isChecked() :
            self.de_return_mission_date.setEnabled(True)
            self.tie_return_mission_time.setEnabled(True)
        else :
            self.de_return_mission_date.setEnabled(False)
            self.tie_return_mission_time.setEnabled(False)

### "STOCK" TAB METHODS ###############################################################

    def populate_stock_lw(self): # Peuplement des ListWidgets du Tab "Stock"
        try :
            self.lw_stock_ref.clear()
            self.lw_stock_count.clear()

            stock_item_names = get_stock_item_names()
            for item_name in sorted(stock_item_names) :
                self.lw_stock_ref.addItem(item_name)
                item_stockCount = get_one_stock_stockCount(item_name)
                self.lw_stock_count.addItem(str(item_stockCount))
        except TypeError :
            pass

    def add_to_stock(self): # BTN "Ajouter" du Tab "Stock"
        new_stock_item = (self.le_stock_ref.text()).title()
        if not new_stock_item :
            return False

        new_stock_item_count = self.sb_stock_qty.value()

        create_new_stock_item(new_stock_item, new_stock_item_count)
        self.raz_stock_widgets()
        self.refresh_all()

    def modify_stock(self): # BTN "Modifier" du Tab "Stock"
        if not self.lw_stock_ref.selectedItems() :
            return False

        for selected_item in self.lw_stock_ref.selectedItems() :
            selected_stock_ref = selected_item.text()
            selected_stock_item_index = self.lw_stock_ref.row(selected_item)

        num, ok = QtWidgets.QInputDialog.getInt(self, f"MODIFIER : {selected_stock_ref.upper()}","Nouvelle Quantité :                                                             ")

        if ok :
            if num == 0:
                QtWidgets.QMessageBox.warning(self, "ATTENTION", "La quantité ne peut être égale à 0 !          ")
                self.modify_stock()
            else :
                stock_item_newCount = str(num)
                modify_stock_item(selected_stock_ref, stock_item_newCount)

                self.refresh_all()
                self.lw_stock_ref.setCurrentItem(self.lw_stock_ref.item(selected_stock_item_index))

    def remove_from_stock(self): # BTN "Supprimer" du Tab "Stock"
        if not self.lw_stock_ref.selectedItems() :
            return False

        for selected_item in self.lw_stock_ref.selectedItems() :
            selected_stock_ref = selected_item.text()

        remove_stock_item(selected_stock_ref)
        self.raz_stock_widgets()
        self.refresh_all()

    def raz_stock_widgets(self): # Remise à zero des Input Widgets du Tab "Stock"
        self.le_stock_ref.setText("")
        self.sb_stock_qty.setValue(1)

### "STOCK TECHNIQUE" TAB METHODS #####################################################

    def populate_tech_stock_lw(self): # Peuplement des ListWidgets du Tab "Stock Technique"
        try :
            self.lw_Tstock_ref.clear()
            self.lw_Tstock_count.clear()

            tech_stock_item_names = get_tech_stock_item_names()
            for item_name in sorted(tech_stock_item_names) :
                self.lw_Tstock_ref.addItem(item_name)
                tech_item_stockCount = get_one_tech_stock_stockCount(item_name)
                self.lw_Tstock_count.addItem(str(tech_item_stockCount))
        except TypeError :
            pass

    def populate_tech_stock_type_cbb(self): # Peuplement du ComboBox de Types du Tab "Stock Technique"
        tech_stock_types = [" Type", "ELEC", "LUM", "SON", "STR", "VID", "DIV"]

        self.cbb_Tstock_type.addItems(sorted(tech_stock_types))

    def add_to_tech_stock(self): # BTN "Ajouter" du Tab "Stock Technique"
        new_tech_stock_ref = (self.le_Tstock_ref.text()).title()
        if not new_tech_stock_ref :
            return False
        
        new_tech_stock_type = self.cbb_Tstock_type.currentText()
        if new_tech_stock_type == " Type" :
            return False

        new_tech_stock_item = """%s - %s""" %(new_tech_stock_type, new_tech_stock_ref)

        new_tech_stock_item_count = self.sb_Tstock_qty.value()

        create_new_tech_stock_item(new_tech_stock_item, new_tech_stock_item_count)
        self.raz_tech_stock_widgets()
        self.refresh_all()

    def modify_tech_stock(self): # BTN "Modifier" du Tab "Stock Technique"
        if not self.lw_Tstock_ref.selectedItems() :
            return False

        for selected_item in self.lw_Tstock_ref.selectedItems() :
            selected_tech_stock_ref = selected_item.text()
            selected_tech_stock_item_index = self.lw_Tstock_ref.row(selected_item)

        num, ok = QtWidgets.QInputDialog.getInt(self,f"MODIFIER : {selected_tech_stock_ref.upper()}","Nouvelle Quantité :                                                             ")

        if ok :
            if num == 0:
                QtWidgets.QMessageBox.warning(self, "ATTENTION", "La quantité ne peut être égale à 0 !          ")
                self.modify_tech_stock()
            else :
                tech_stock_item_newCount = str(num)
                modify_tech_stock_item(selected_tech_stock_ref, tech_stock_item_newCount)

                self.refresh_all()
                self.lw_Tstock_ref.setCurrentItem(self.lw_Tstock_ref.item(selected_tech_stock_item_index))

    def remove_from_tech_stock(self): # BTN "Supprimer" du Tab "Stock Technique"
        if not self.lw_Tstock_ref.selectedItems() :
            return False

        for selected_item in self.lw_Tstock_ref.selectedItems() :
            selected_tech_stock_ref = selected_item.text()

        remove_tech_stock_item(selected_tech_stock_ref)
        self.raz_stock_widgets()
        self.refresh_all()

    def raz_tech_stock_widgets(self): # Remise à zero des Input Widgets du Tab "Stock Technique"
        self.le_Tstock_ref.setText("")
        self.sb_Tstock_qty.setValue(1)

### "PRETS DE MATERIEL" TAB METHODS ###################################################

    def populate_prets_localisations_lw(self): # Peuplement du ListWidget de Localisations du Tab "Prets de Matériel"
        try :
            self.lw_prets_local.clear()
            prets_localisations = get_prets_localisations()

            for localisation in sorted(prets_localisations) :
                localisation_type = get_one_prets_type(localisation)

                if localisation_type == 1 :
                    localisation = """🟡 %s""" %(localisation)
                    item = QtWidgets.QListWidgetItem(localisation)
                    self.lw_prets_local.addItem(item)

            for localisation in sorted(prets_localisations) :
                localisation_type = get_one_prets_type(localisation)

                if localisation_type == 2 :
                    localisation = """🟢 %s""" %(localisation)
                    item = QtWidgets.QListWidgetItem(localisation)
                    self.lw_prets_local.addItem(item)

            for localisation in sorted(prets_localisations) :
                localisation_type = get_one_prets_type(localisation)

                if localisation_type == 3 :
                    localisation = """🟣 %s""" %(localisation)
                    item = QtWidgets.QListWidgetItem(localisation)
                    self.lw_prets_local.addItem(item)
        except TypeError :
            pass

    def populate_prets_lists_lw(self): # Peuplement du ListWidget de Listes du Tab "Prets de Matériel"
        self.lw_prets_matos.clear()
        
        if not self.lw_prets_local.selectedItems() :
            return False

        for selected_name in self.lw_prets_local.selectedItems() :
            selected_local_name = selected_name.text()

        if selected_local_name.startswith("🟡") :
            selected_localisation = selected_local_name.lstrip("🟡 ")
        if selected_local_name.startswith("🟢") :
            selected_localisation = selected_local_name.lstrip("🟢 ")
        if selected_local_name.startswith("🟣") :
            selected_localisation = selected_local_name.lstrip("🟣 ")

        local_total_list = get_one_prets_list(selected_localisation)
        if local_total_list == None :
            return False
        else :
            local_list = local_total_list.split("\n")
        
            for item in local_list :
                self.lw_prets_matos.addItem(item)

    def checkbox1_gestion(self): # Gestion de la checkBox 1
        if self.cb_prets_1.isChecked() :
            self.cb_prets_2.setChecked(False)
            self.cb_prets_3.setChecked(False)

    def checkbox2_gestion(self): # Gestion de la checkBox 2
        if self.cb_prets_2.isChecked() :
            self.cb_prets_1.setChecked(False)
            self.cb_prets_3.setChecked(False)

    def checkbox3_gestion(self): # Gestion de la checkBox 3
        if self.cb_prets_3.isChecked() :
            self.cb_prets_1.setChecked(False)
            self.cb_prets_2.setChecked(False)

    def prets_remove(self): # BTN "Supprimer" du Tab "Prets de Matériel"
        if not self.lw_prets_local.selectedItems() :
            return False

        for selected_name in self.lw_prets_local.selectedItems() :
            selected_pret_name = selected_name.text()

        if selected_pret_name.startswith("🟡") :
            selected_localisation = selected_pret_name.lstrip("🟡 ")
        if selected_pret_name.startswith("🟢") :
            selected_localisation = selected_pret_name.lstrip("🟢 ")
        if selected_pret_name.startswith("🟣") :
            selected_localisation = selected_pret_name.lstrip("🟣 ")

        pret_values = get_one_prets_list(selected_localisation)
        if pret_values == None :
            self.prets_remove_empty_popup(selected_localisation)
        else :
            self.prets_remove_popup(selected_localisation)

    def prets_remove_popup(self, localisation): # Demande confirmation de supprimer la Localisation si PretList n'est pas vide
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Tout le matériel sera retourné à l'Atelier.\nSupprimer quand même ?")
        msgBox.setWindowTitle("SUPPRIMER UN DESTINATAIRE")
        msgBox.setWindowIcon(QtGui.QIcon(ICON_FILE))
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            remove_prets(localisation)

            calculate_total_prets()
            self.refresh_all()

    def prets_remove_empty_popup(self, localisation): # Demande confirmation de supprimer la Localisation si PretList est vide
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Ce destinataire ne dispose d'aucun materiel.\nSupprimer quand même ?")
        msgBox.setWindowTitle("SUPPRIMER UN DESTINATAIRE")
        msgBox.setWindowIcon(QtGui.QIcon(ICON_FILE))
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            remove_prets(localisation)

            self.refresh_all()

    def prets_add(self): # BTN "Ajouter" du Tab "Prets de Matériel"
        new_pret_name = (self.le_prets_name.text()).title()
        if not new_pret_name :
            return False
        prets_list = get_prets_localisations()
        if new_pret_name in prets_list :
            QtWidgets.QMessageBox.warning(self, "ATTENTION", "Ce destinataire existe déjà !         ")
            return False

        type_list = [1, 2, 3]
        pret_type = 0
        if self.cb_prets_1.isChecked() :
            pret_type = 1
        elif self.cb_prets_2.isChecked() :
            pret_type = 2
        elif self.cb_prets_3.isChecked() :
            pret_type = 3
        
        if pret_type not in type_list :
            return False

        create_prets(new_pret_name, pret_type)

        self.refresh_all()
        self.raz_prets_widgets()

    def prets_cancel(self): # BTN "Annuler" du Tab "Prets de Matériel"
        self.raz_prets_widgets()

    def raz_prets_widgets(self): # Remise à zero des Input Widgets du Tab "Stock Technique"
        self.le_prets_name.setText("")
        self.cb_prets_1.setChecked(False)
        self.cb_prets_2.setChecked(False)
        self.cb_prets_3.setChecked(False)

### "ATELIER" TAB METHODS #############################################################

    def populate_atel_ref_qty_lw(self): # Peuplement des ListWidgets "Références" et "Quantité" du Tab "Atelier"
        try :
            self.lw_atel_ref.clear()
            self.lw_atel_qty.clear()

            atel_stock_item_names = get_stock_item_names()
            for item_name in sorted(atel_stock_item_names) :
                self.lw_atel_ref.addItem(item_name)
                item_atelCount = get_one_stock_atelCount(item_name)
                self.lw_atel_qty.addItem(str(item_atelCount))

            atel_tech_stock_item_names = get_tech_stock_item_names()
            for item_name in sorted(atel_tech_stock_item_names) :
                self.lw_atel_ref.addItem(item_name)
                item_atelCount = get_one_tech_stock_atelCount(item_name)
                self.lw_atel_qty.addItem(str(item_atelCount))
        except TypeError :
            pass

    def populate_atel_search_cbb(self): # Peuplement du ComboBox "Recherche" du Tab "Atelier"
        try :
            self.cbb_atel_ref.clear()
            atel_search_items = [""]

            stock_item_names = get_stock_item_names()
            for item_name in sorted(stock_item_names) :
                atel_search_items.append(item_name)

            tech_stock_item_names = get_tech_stock_item_names()
            for item_name in sorted(tech_stock_item_names) :
                atel_search_items.append(item_name)

            self.cbb_atel_ref.addItems(atel_search_items)
        except TypeError :
            pass

    def populate_atel_search_lw(self): # Peuplement du ListWidget de Recherche d'items du Tab "Atelier"
        self.lw_atel_search.clear()
        item_searched = self.cbb_atel_ref.currentText()
        item_list = []

        if item_searched == "" :
            return False
            
        # Récupération des items de l'Atelier

        stock_items = get_stock_item_names()
        tech_stock_items = get_tech_stock_item_names()

        for item in stock_items :
            if item == item_searched :
                atel_count = get_one_stock_atelCount(item_searched)
                if atel_count != 0 :
                    atel_formated_count = f"Atelier : {int(atel_count)}"
                    item_list.append(atel_formated_count)
                elif atel_count == 0 :
                    pass

        for item in tech_stock_items :
            if item == item_searched :
                atel_tech_count = get_one_tech_stock_atelCount(item_searched)
                if atel_tech_count != 0 :
                    atel_formated_count = f"Atelier : {int(atel_tech_count)}"
                    item_list.append(atel_formated_count)
                elif atel_tech_count == 0 :
                    pass

        # Récupération des items dans Prets

        prets_localisations = get_prets_localisations()
        for pret_localisation in prets_localisations :
            pret_list_unformated = get_one_prets_list(pret_localisation)

            if pret_list_unformated != None :
                pret_list = pret_list_unformated.split("\n")
                
                for pret_item in pret_list :
                    if pret_item.split(" : ")[0] == item_searched :
                        item_qty = pret_item.split(" : ")[1]
                        pret_formated_count = """%s : %s""" %(pret_localisation, item_qty)
                        item_list.append(pret_formated_count)

        # Ecriture du ListWidget de Recherche d'Item

        if item_list == [] :
            empty_item = "Cet élément n'est pas en stock"
            self.lw_atel_search.addItem(empty_item)
        else :
            for item in item_list :
                self.lw_atel_search.addItem(item)

    def update(self): # Actualisation des Widgets apres séléction de la Database
        get_db_path()

        calculate_total_prets()

        self.populate_daily_missions_lw()
        self.populate_create_type_cbb()
        self.populate_create_matos_localisation_cbb()
        self.populate_create_matos_prov_cbb()

        self.populate_stock_lw()

        self.populate_tech_stock_lw()
        self.populate_tech_stock_type_cbb()

        self.populate_prets_localisations_lw()

        self.populate_atel_ref_qty_lw()
        self.populate_atel_search_cbb()

    def get_database(self): # Pop Up de recherche du chemin vers la base de données partagée.
        raw_path = QtWidgets.QFileDialog.getOpenFileName(self, "Choisir la base de données partagée", "*.db")
        path = {"path" : raw_path[0]}
        with open(PATH_FILE, 'w', encoding='utf8') as f :
            json.dump(path, f)
        f.close()

### GENERAL METHODS ###################################################################

    def refresh_lw(self): # Rafraichissement des Listwidgets
        self.populate_stock_lw()
        self.populate_tech_stock_lw()
        self.populate_prets_localisations_lw()
        self.populate_atel_ref_qty_lw()

    def refresh_cbb(self): # Rafraichissement des ComboBox
        self.populate_create_matos_localisation_cbb()
        self.populate_create_matos_prov_cbb()
        self.populate_create_matos_items_cbb()
        self.populate_atel_search_cbb()

    def refresh_all(self): # Rafraichissement de tous les Widgets
        self.refresh_lw()
        self.refresh_cbb()

### END OF App CLASS ##################################################################

class CalendarView(QtWidgets.QWidget):
    def __init__(self): # Initialisation de la fenêtre et des fonctions de départ
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("MATOSAURUS REX  |  CALENDRIER HEBDOMADAIRE")
        self.setStyleSheet("background-color: rgb(200, 200, 255)")
        self.setWindowIcon(QtGui.QIcon(ICON_FILE))
        self.calendarUI()
        self.setup_connection()
        self.setup_defaults()
        self.get_current_week()

        self.populate_calendar_monday_missions()
        self.populate_calendar_tuesday_missions()
        self.populate_calendar_wednesday_missions()
        self.populate_calendar_thirsday_missions()
        self.populate_calendar_friday_missions()
        self.populate_calendar_saturday_missions()
        self.populate_calendar_sunday_missions()

    def calendarUI(self): # Génération du Calendrier Hebdomadaire
        self.grid_layout = QtWidgets.QGridLayout(self)
        
        self.lbl_calendar = QtWidgets.QLabel(" 📅 - PLANNING HEBDOMADAIRE ")
        self.btn_save = QtWidgets.QPushButton("ENREGISTRER")
        self.btn_update = QtWidgets.QPushButton("ACTUALISER")

        self.groupBox1 = QtWidgets.QGroupBox()
        self.groupBox2 = QtWidgets.QGroupBox()
        self.groupBox3 = QtWidgets.QGroupBox()
        self.groupBox4 = QtWidgets.QGroupBox()
        self.groupBox5 = QtWidgets.QGroupBox()
        self.groupBox6 = QtWidgets.QGroupBox()
        self.groupBox7 = QtWidgets.QGroupBox()

        self.grid_layout.addWidget(self.lbl_calendar, 0, 0, 1, 4)
        self.grid_layout.addWidget(self.btn_save, 0, 4, 1, 1)
        self.grid_layout.addWidget(self.btn_update, 0, 5, 1, 1)
        self.grid_layout.addWidget(self.groupBox1, 1, 0, 2, 1)
        self.grid_layout.addWidget(self.groupBox2, 1, 1, 2, 1)
        self.grid_layout.addWidget(self.groupBox3, 1, 2, 2, 1)
        self.grid_layout.addWidget(self.groupBox4, 1, 3, 2, 1)
        self.grid_layout.addWidget(self.groupBox5, 1, 4, 2, 1)
        self.grid_layout.addWidget(self.groupBox6, 1, 5, 1, 1)
        self.grid_layout.addWidget(self.groupBox7, 2, 5, 1, 1)

        self.lbl_calendar.setStyleSheet("background-color: rgb(255, 255, 150); font: 14pt; MS Shell Dlg 2")
        self.btn_save.setStyleSheet("background-color: rgb(100, 200, 100)")
        self.btn_update.setStyleSheet("background-color: rgb(200, 100, 100)")

        self.gridLayout1 = QtWidgets.QGridLayout(self.groupBox1)
        self.gridLayout2 = QtWidgets.QGridLayout(self.groupBox2)
        self.gridLayout3 = QtWidgets.QGridLayout(self.groupBox3)
        self.gridLayout4 = QtWidgets.QGridLayout(self.groupBox4)
        self.gridLayout5 = QtWidgets.QGridLayout(self.groupBox5)
        self.gridLayout6 = QtWidgets.QGridLayout(self.groupBox6)
        self.gridLayout7 = QtWidgets.QGridLayout(self.groupBox7)

        self.groupBox1.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.groupBox2.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.groupBox3.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.groupBox4.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.groupBox5.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.groupBox6.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.groupBox7.setStyleSheet("background-color: rgb(150, 150, 255)")

        self.lbl_monday = QtWidgets.QLabel("LUNDI ", self.groupBox1)
        self.le_monday = QtWidgets.QLineEdit(self.groupBox1)
        self.lw_monday = QtWidgets.QListWidget(self.groupBox1)
        self.lw_monday.setAlternatingRowColors(True)

        self.lbl_tuesday = QtWidgets.QLabel("MARDI ", self.groupBox2)
        self.le_tuesday = QtWidgets.QLineEdit(self.groupBox2)
        self.lw_tuesday = QtWidgets.QListWidget(self.groupBox2)
        self.lw_tuesday.setAlternatingRowColors(True)

        self.lbl_wednesday = QtWidgets.QLabel("MERCREDI ", self.groupBox3)
        self.le_wednesday = QtWidgets.QLineEdit(self.groupBox3)
        self.lw_wednesday = QtWidgets.QListWidget(self.groupBox3)
        self.lw_wednesday.setAlternatingRowColors(True)

        self.lbl_thirsday = QtWidgets.QLabel("JEUDI ", self.groupBox4)
        self.le_thirsday = QtWidgets.QLineEdit(self.groupBox4)
        self.lw_thirsday = QtWidgets.QListWidget(self.groupBox4)
        self.lw_thirsday.setAlternatingRowColors(True)

        self.lbl_friday = QtWidgets.QLabel("VENDREDI ", self.groupBox5)
        self.le_friday = QtWidgets.QLineEdit(self.groupBox5)
        self.lw_friday = QtWidgets.QListWidget(self.groupBox5)
        self.lw_friday.setAlternatingRowColors(True)

        self.lbl_saturday = QtWidgets.QLabel("SAMEDI ", self.groupBox6)
        self.le_saturday = QtWidgets.QLineEdit(self.groupBox6)
        self.lw_saturday = QtWidgets.QListWidget(self.groupBox6)
        self.lw_saturday.setAlternatingRowColors(True)

        self.lbl_sunday = QtWidgets.QLabel("DIMANCHE ", self.groupBox7)
        self.le_sunday = QtWidgets.QLineEdit(self.groupBox7)
        self.lw_sunday = QtWidgets.QListWidget(self.groupBox7)
        self.lw_sunday.setAlternatingRowColors(True)

        self.gridLayout1.addWidget(self.lbl_monday, 0, 0, 1, 1)
        self.gridLayout1.addWidget(self.le_monday, 0, 1, 1, 2)
        self.gridLayout1.addWidget(self.lw_monday, 1, 0, 1, 3)

        self.gridLayout2.addWidget(self.lbl_tuesday, 0, 0, 1, 1)
        self.gridLayout2.addWidget(self.le_tuesday, 0, 1, 1, 2)
        self.gridLayout2.addWidget(self.lw_tuesday, 1, 0, 1, 3)
        
        self.gridLayout3.addWidget(self.lbl_wednesday, 0, 0, 1, 1)
        self.gridLayout3.addWidget(self.le_wednesday, 0, 1, 1, 2)
        self.gridLayout3.addWidget(self.lw_wednesday, 1, 0, 1, 3)

        self.gridLayout4.addWidget(self.lbl_thirsday, 0, 0, 1, 1)
        self.gridLayout4.addWidget(self.le_thirsday, 0, 1, 1, 2)
        self.gridLayout4.addWidget(self.lw_thirsday, 1, 0, 1, 3)

        self.gridLayout5.addWidget(self.lbl_friday, 0, 0, 1, 1)
        self.gridLayout5.addWidget(self.le_friday, 0, 1, 1, 2)
        self.gridLayout5.addWidget(self.lw_friday, 1, 0, 1, 3)

        self.gridLayout6.addWidget(self.lbl_saturday, 0, 0, 1, 1)
        self.gridLayout6.addWidget(self.le_saturday, 0, 1, 1, 2)
        self.gridLayout6.addWidget(self.lw_saturday, 1, 0, 1, 3)

        self.gridLayout7.addWidget(self.lbl_sunday, 0, 0, 1, 1)
        self.gridLayout7.addWidget(self.le_sunday, 0, 1, 1, 2)
        self.gridLayout7.addWidget(self.lw_sunday, 1, 0, 1, 3)

        self.le_monday.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.le_monday.setReadOnly(True)
        self.lw_monday.setStyleSheet("background-color: rgb(255, 255, 255)")

        self.le_tuesday.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.le_tuesday.setReadOnly(True)
        self.lw_tuesday.setStyleSheet("background-color: rgb(255, 255, 255)")

        self.le_wednesday.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.le_wednesday.setReadOnly(True)
        self.lw_wednesday.setStyleSheet("background-color: rgb(255, 255, 255)")

        self.le_thirsday.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.le_thirsday.setReadOnly(True)
        self.lw_thirsday.setStyleSheet("background-color: rgb(255, 255, 255)")

        self.le_friday.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.le_friday.setReadOnly(True)
        self.lw_friday.setStyleSheet("background-color: rgb(255, 255, 255)")

        self.le_saturday.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.le_saturday.setReadOnly(True)
        self.lw_saturday.setStyleSheet("background-color: rgb(255, 255, 255)")

        self.le_sunday.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.le_sunday.setReadOnly(True)
        self.lw_sunday.setStyleSheet("background-color: rgb(255, 255, 255)")

    def setup_connection(self): # Parametrage du bouton Update
        self.btn_update.clicked.connect(self.reboot)
        self.btn_save.clicked.connect(self.save)

    def setup_defaults(self): # Parametrage par défaut des Widgets du Calendrier
        self.le_monday.setReadOnly(True)
        self.le_tuesday.setReadOnly(True)
        self.le_wednesday.setReadOnly(True)
        self.le_thirsday.setReadOnly(True)
        self.le_friday.setReadOnly(True)
        self.le_saturday.setReadOnly(True)
        self.le_sunday.setReadOnly(True)

    def populate_calendar_monday_missions(self): # Peuplement des missions du Lundi
        self.lw_monday.clear()
        monday_missions = []
        monday_date = self.le_monday.text()
        monday_missions_ids = get_ids_from_date(monday_date)
        for mission_id in monday_missions_ids :
            mission_title = get_title_from_id(mission_id)
            mission_type = get_type_from_id(mission_id)
            if mission_type == 1 :
                mission_title_formated = """🟡 %s""" %(mission_title)
            if mission_type == 2 :
                mission_title_formated = """🟢 %s""" %(mission_title)
            if mission_type == 3 :
                mission_title_formated = """🟣 %s""" %(mission_title)
            mission_time = get_time_from_id(mission_id)
            mission_localisation = get_localisation_from_id(mission_id)
            mission_time_and_localisation = """- %s - %s""" %(mission_time, mission_localisation)
            
            mission_description_text = get_description_from_id(mission_id)
            mission_description = '\n'.join(textwrap.wrap(mission_description_text, 40, break_long_words=False))

            mission_list = [mission_title_formated, mission_time_and_localisation, mission_description]

            mission_return_status = get_return_status_from_id(mission_id)
            if mission_return_status == 1 :
                mission_return_date = get_return_date_from_id(mission_id)
                mission_return_time = get_return_time_from_id(mission_id)
                mission_return = """- Retour le %s à %s""" %(mission_return_date, mission_return_time)
                mission_list.append(mission_return)

            mission_matos = get_matos_from_id(mission_id)
            if mission_matos != "" :
                mission_list.append(mission_matos)

            mission = "\n".join(mission_list)
            monday_missions.append(mission)
            
        self.lw_monday.addItems(monday_missions)

    def populate_calendar_tuesday_missions(self): # Peuplement des missions du Mardi
        self.lw_tuesday.clear()
        tuesday_missions = []
        tuesday_date = self.le_tuesday.text()
        tuesday_missions_ids = get_ids_from_date(tuesday_date)
        for mission_id in tuesday_missions_ids :
            mission_title = get_title_from_id(mission_id)
            mission_type = get_type_from_id(mission_id)
            if mission_type == 1 :
                mission_title_formated = """🟡 %s""" %(mission_title)
            if mission_type == 2 :
                mission_title_formated = """🟢 %s""" %(mission_title)
            if mission_type == 3 :
                mission_title_formated = """🟣 %s""" %(mission_title)
            mission_time = get_time_from_id(mission_id)
            mission_localisation = get_localisation_from_id(mission_id)
            mission_time_and_localisation = """- %s - %s""" %(mission_time, mission_localisation)

            mission_description_text = get_description_from_id(mission_id)
            mission_description = '\n'.join(textwrap.wrap(mission_description_text, 40, break_long_words=False))

            mission_list = [mission_title_formated, mission_time_and_localisation, mission_description]

            mission_return_status = get_return_status_from_id(mission_id)
            if mission_return_status == 1 :
                mission_return_date = get_return_date_from_id(mission_id)
                mission_return_time = get_return_time_from_id(mission_id)
                mission_return = """- Retour le %s à %s""" %(mission_return_date, mission_return_time)
                mission_list.append(mission_return)

            mission_matos = get_matos_from_id(mission_id)
            if mission_matos != "" :
                mission_list.append(mission_matos)

            mission = "\n".join(mission_list)
            tuesday_missions.append(mission)
            
        self.lw_tuesday.addItems(tuesday_missions)

    def populate_calendar_wednesday_missions(self): # Peuplement des missions du Mercredi
        self.lw_wednesday.clear()
        wednesday_missions = []
        wednesday_date = self.le_wednesday.text()
        wednesday_missions_ids = get_ids_from_date(wednesday_date)
        for mission_id in wednesday_missions_ids :
            mission_title = get_title_from_id(mission_id)
            mission_type = get_type_from_id(mission_id)
            if mission_type == 1 :
                mission_title_formated = """🟡 %s""" %(mission_title)
            if mission_type == 2 :
                mission_title_formated = """🟢 %s""" %(mission_title)
            if mission_type == 3 :
                mission_title_formated = """🟣 %s""" %(mission_title)
            mission_time = get_time_from_id(mission_id)
            mission_localisation = get_localisation_from_id(mission_id)
            mission_time_and_localisation = """- %s - %s""" %(mission_time, mission_localisation)
            
            mission_description_text = get_description_from_id(mission_id)
            mission_description = '\n'.join(textwrap.wrap(mission_description_text, 40, break_long_words=False))

            mission_list = [mission_title_formated, mission_time_and_localisation, mission_description]

            mission_return_status = get_return_status_from_id(mission_id)
            if mission_return_status == 1 :
                mission_return_date = get_return_date_from_id(mission_id)
                mission_return_time = get_return_time_from_id(mission_id)
                mission_return = """- Retour le %s à %s""" %(mission_return_date, mission_return_time)
                mission_list.append(mission_return)

            mission_matos = get_matos_from_id(mission_id)
            if mission_matos != "" :
                mission_list.append(mission_matos)

            mission = "\n".join(mission_list)
            wednesday_missions.append(mission)
            
        self.lw_wednesday.addItems(wednesday_missions)

    def populate_calendar_thirsday_missions(self): # Peuplement des missions du Jeudi
        self.lw_thirsday.clear()
        thirsday_missions = []
        thirsday_date = self.le_thirsday.text()
        thirsday_missions_ids = get_ids_from_date(thirsday_date)
        for mission_id in thirsday_missions_ids :
            mission_title = get_title_from_id(mission_id)
            mission_type = get_type_from_id(mission_id)
            if mission_type == 1 :
                mission_title_formated = """🟡 %s""" %(mission_title)
            if mission_type == 2 :
                mission_title_formated = """🟢 %s""" %(mission_title)
            if mission_type == 3 :
                mission_title_formated = """🟣 %s""" %(mission_title)
            mission_time = get_time_from_id(mission_id)
            mission_localisation = get_localisation_from_id(mission_id)
            mission_time_and_localisation = """- %s - %s""" %(mission_time, mission_localisation)
            
            mission_description_text = get_description_from_id(mission_id)
            mission_description = '\n'.join(textwrap.wrap(mission_description_text, 40, break_long_words=False))

            mission_list = [mission_title_formated, mission_time_and_localisation, mission_description]

            mission_return_status = get_return_status_from_id(mission_id)
            if mission_return_status == 1 :
                mission_return_date = get_return_date_from_id(mission_id)
                mission_return_time = get_return_time_from_id(mission_id)
                mission_return = """- Retour le %s à %s""" %(mission_return_date, mission_return_time)
                mission_list.append(mission_return)

            mission_matos = get_matos_from_id(mission_id)
            if mission_matos != "" :
                mission_list.append(mission_matos)

            mission = "\n".join(mission_list)
            thirsday_missions.append(mission)
            
        self.lw_thirsday.addItems(thirsday_missions)

    def populate_calendar_friday_missions(self): # Peuplement des missions du Vendredi
        self.lw_friday.clear()
        friday_missions = []
        friday_date = self.le_friday.text()
        friday_missions_ids = get_ids_from_date(friday_date)
        for mission_id in friday_missions_ids :
            mission_title = get_title_from_id(mission_id)
            mission_type = get_type_from_id(mission_id)
            if mission_type == 1 :
                mission_title_formated = """🟡 %s""" %(mission_title)
            if mission_type == 2 :
                mission_title_formated = """🟢 %s""" %(mission_title)
            if mission_type == 3 :
                mission_title_formated = """🟣 %s""" %(mission_title)
            mission_time = get_time_from_id(mission_id)
            mission_localisation = get_localisation_from_id(mission_id)
            mission_time_and_localisation = """- %s - %s""" %(mission_time, mission_localisation)
            
            mission_description_text = get_description_from_id(mission_id)
            mission_description = '\n'.join(textwrap.wrap(mission_description_text, 40, break_long_words=False))

            mission_list = [mission_title_formated, mission_time_and_localisation, mission_description]

            mission_return_status = get_return_status_from_id(mission_id)
            if mission_return_status == 1 :
                mission_return_date = get_return_date_from_id(mission_id)
                mission_return_time = get_return_time_from_id(mission_id)
                mission_return = """- Retour le %s à %s""" %(mission_return_date, mission_return_time)
                mission_list.append(mission_return)

            mission_matos = get_matos_from_id(mission_id)
            if mission_matos != "" :
                mission_list.append(mission_matos)

            mission = "\n".join(mission_list)
            friday_missions.append(mission)
            
        self.lw_friday.addItems(friday_missions)

    def populate_calendar_saturday_missions(self): # Peuplement des missions du Samedi
        self.lw_saturday.clear()
        saturday_missions = []
        saturday_date = self.le_saturday.text()
        saturday_missions_ids = get_ids_from_date(saturday_date)
        for mission_id in saturday_missions_ids :
            mission_title = get_title_from_id(mission_id)
            mission_type = get_type_from_id(mission_id)
            if mission_type == 1 :
                mission_title_formated = """🟡 %s""" %(mission_title)
            if mission_type == 2 :
                mission_title_formated = """🟢 %s""" %(mission_title)
            if mission_type == 3 :
                mission_title_formated = """🟣 %s""" %(mission_title)
            mission_time = get_time_from_id(mission_id)
            mission_localisation = get_localisation_from_id(mission_id)
            mission_time_and_localisation = """- %s - %s""" %(mission_time, mission_localisation)
            
            mission_description_text = get_description_from_id(mission_id)
            mission_description = '\n'.join(textwrap.wrap(mission_description_text, 40, break_long_words=False))

            mission_list = [mission_title_formated, mission_time_and_localisation, mission_description]

            mission_return_status = get_return_status_from_id(mission_id)
            if mission_return_status == 1 :
                mission_return_date = get_return_date_from_id(mission_id)
                mission_return_time = get_return_time_from_id(mission_id)
                mission_return = """- Retour le %s à %s""" %(mission_return_date, mission_return_time)
                mission_list.append(mission_return)

            mission_matos = get_matos_from_id(mission_id)
            if mission_matos != "" :
                mission_list.append(mission_matos)

            mission = "\n".join(mission_list)
            saturday_missions.append(mission)
            
        self.lw_saturday.addItems(saturday_missions)

    def populate_calendar_sunday_missions(self): # Peuplement des missions du Dimanche
        self.lw_sunday.clear()
        sunday_missions = []
        sunday_date = self.le_sunday.text()
        sunday_missions_ids = get_ids_from_date(sunday_date)
        for mission_id in sunday_missions_ids :
            mission_title = get_title_from_id(mission_id)
            mission_type = get_type_from_id(mission_id)
            if mission_type == 1 :
                mission_title_formated = """🟡 %s""" %(mission_title)
            if mission_type == 2 :
                mission_title_formated = """🟢 %s""" %(mission_title)
            if mission_type == 3 :
                mission_title_formated = """🟣 %s""" %(mission_title)
            mission_time = get_time_from_id(mission_id)
            mission_localisation = get_localisation_from_id(mission_id)
            mission_time_and_localisation = """- %s - %s""" %(mission_time, mission_localisation)
            
            mission_description_text = get_description_from_id(mission_id)
            mission_description = '\n'.join(textwrap.wrap(mission_description_text, 40, break_long_words=False))

            mission_list = [mission_title_formated, mission_time_and_localisation, mission_description]

            mission_return_status = get_return_status_from_id(mission_id)
            if mission_return_status == 1 :
                mission_return_date = get_return_date_from_id(mission_id)
                mission_return_time = get_return_time_from_id(mission_id)
                mission_return = """- Retour le %s à %s""" %(mission_return_date, mission_return_time)
                mission_list.append(mission_return)

            mission_matos = get_matos_from_id(mission_id)
            if mission_matos != "" :
                mission_list.append(mission_matos)

            mission = "\n".join(mission_list)
            sunday_missions.append(mission)
            
        self.lw_sunday.addItems(sunday_missions)

    def get_current_week(self): # Obtenir la semaine courrante
        current_date = QDate.currentDate().toString()
        year = current_date.split(" ")[3]
        month = current_date.split(" ")[1]
        day = current_date.split(" ")[2]
        if month == "janv." :
            f_month = "01"
        if month == "févr." :
            f_month = "02"
        if month == "mars" :
            f_month = "03"
        if month == "avr." :
            f_month = "04"
        if month == "mai" :
            f_month = "05"
        if month == "juin." :
            f_month = "06"
        if month == "juil." :
            f_month = "07"
        if month == "août" :
            f_month = "08"
        if month == "sept." :
            f_month = "09"
        if month == "oct." :
            f_month = "10"
        if month == "nov." :
            f_month = "11"
        if month == "déc." :
            f_month = "12"
        
        isodate = date(int(year), int(f_month), int(day)).isocalendar()

        current_year = isodate[0]
        current_week_nbr = isodate[1]

        self.setup_dates_le(current_year, current_week_nbr)

    def reboot(self): # ReBoot des fonctions initiales
        self.get_current_week()
        self.populate_calendar_monday_missions()
        self.populate_calendar_tuesday_missions()
        self.populate_calendar_wednesday_missions()
        self.populate_calendar_thirsday_missions()
        self.populate_calendar_friday_missions()
        self.populate_calendar_saturday_missions()
        self.populate_calendar_sunday_missions()

    def save(self): # Enregistre le tableau
        try :
            matos = []
            file_name = QtWidgets.QFileDialog.getSaveFileName(self, 'Enregistrer le planning :','' , '.txt')
            file_path = ("").join(file_name)

            with open(file_path, "w", encoding='utf8') as f :
                f.write("*********************************** PLANNING DE LA SEMAINE ***********************************\n\n")

                f.write("LUNDI ")
                monday_date = self.le_monday.text()
                f.write(monday_date)
                f.write(" : \n\n")

                monday_missions_ids = get_ids_from_date(monday_date)
                if monday_missions_ids != [] :
                    for id in monday_missions_ids :
                        f.write(get_title_from_id(id).upper())
                        f.write(" : ")
                        f.write(get_localisation_from_id(id))
                        f.write("  -  ")
                        f.write(get_time_from_id(id))
                        f.write("\n")
                        f.write(get_description_from_id(id))
                        f.write("\n")
                        matos = get_matos_from_id(id)
                        if matos != [] :
                            for item in matos :
                                f.write(item)
                        f.write("\n\n")

                f.write("----------------------------------------------------------------------------------------------\n\n")

                f.write("MARDI ")
                tuesday_date = self.le_tuesday.text()
                f.write(tuesday_date)
                f.write(" : \n\n")

                tuesday_missions_ids = get_ids_from_date(tuesday_date)
                if tuesday_missions_ids != [] :
                    for id in tuesday_missions_ids :
                        f.write(get_title_from_id(id).upper())
                        f.write(" : ")
                        f.write(get_localisation_from_id(id))
                        f.write("  -  ")
                        f.write(get_time_from_id(id))
                        f.write("\n")
                        f.write(get_description_from_id(id))
                        f.write("\n")
                        matos = get_matos_from_id(id)
                        if matos != [] :
                            for item in matos :
                                f.write(item)
                        f.write("\n\n")

                f.write("----------------------------------------------------------------------------------------------\n\n")

                f.write("MERCREDI ")
                wednesday_date = self.le_wednesday.text()
                f.write(wednesday_date)
                f.write(" : \n\n")

                wednesday_missions_ids = get_ids_from_date(wednesday_date)
                if wednesday_missions_ids != [] :
                    for id in wednesday_missions_ids :
                        f.write(get_title_from_id(id).upper())
                        f.write(" : ")
                        f.write(get_localisation_from_id(id))
                        f.write("  -  ")
                        f.write(get_time_from_id(id))
                        f.write("\n")
                        f.write(get_description_from_id(id))
                        f.write("\n")
                        matos = get_matos_from_id(id)
                        if matos != [] :
                            for item in matos :
                                f.write(item)
                        f.write("\n\n")

                f.write("----------------------------------------------------------------------------------------------\n\n")

                f.write("JEUDI ")
                thirsday_date = self.le_thirsday.text()
                f.write(thirsday_date)
                f.write(" : \n\n")

                thirsday_missions_ids = get_ids_from_date(thirsday_date)
                if thirsday_missions_ids != [] :
                    for id in thirsday_missions_ids :
                        f.write(get_title_from_id(id).upper())
                        f.write(" : ")
                        f.write(get_localisation_from_id(id))
                        f.write("  -  ")
                        f.write(get_time_from_id(id))
                        f.write("\n")
                        f.write(get_description_from_id(id))
                        f.write("\n")
                        matos = get_matos_from_id(id)
                        if matos != [] :
                            for item in matos :
                                f.write(item)
                        f.write("\n\n")

                f.write("----------------------------------------------------------------------------------------------\n\n")

                f.write("VENDREDI ")
                friday_date = self.le_friday.text()
                f.write(friday_date)
                f.write(" : \n\n")

                friday_missions_ids = get_ids_from_date(friday_date)
                if friday_missions_ids != [] :
                    for id in friday_missions_ids :
                        f.write(get_title_from_id(id).upper())
                        f.write(" : ")
                        f.write(get_localisation_from_id(id))
                        f.write("  -  ")
                        f.write(get_time_from_id(id))
                        f.write("\n")
                        f.write(get_description_from_id(id))
                        f.write("\n")
                        matos = get_matos_from_id(id)
                        if matos != [] :
                            for item in matos :
                                f.write(item)
                        f.write("\n\n")

                f.write("----------------------------------------------------------------------------------------------\n\n")

                f.write("SAMEDI ")
                saturday_date = self.le_saturday.text()
                f.write(saturday_date)
                f.write(" : \n\n")

                saturday_missions_ids = get_ids_from_date(saturday_date)
                if saturday_missions_ids != [] :
                    for id in saturday_missions_ids :
                        f.write(get_title_from_id(id).upper())
                        f.write(" : ")
                        f.write(get_localisation_from_id(id))
                        f.write("  -  ")
                        f.write(get_time_from_id(id))
                        f.write("\n")
                        f.write(get_description_from_id(id))
                        f.write("\n")
                        matos = get_matos_from_id(id)
                        if matos != [] :
                            for item in matos :
                                f.write(item)
                        f.write("\n\n")

                f.write("----------------------------------------------------------------------------------------------\n\n")

                f.write("DIMANCHE ")
                sunday_date = self.le_sunday.text()
                f.write(sunday_date)
                f.write(" : \n\n")

                sunday_missions_ids = get_ids_from_date(sunday_date)
                if sunday_missions_ids != [] :
                    for id in sunday_missions_ids :
                        f.write(get_title_from_id(id).upper())
                        f.write(" : ")
                        f.write(get_localisation_from_id(id))
                        f.write("  -  ")
                        f.write(get_time_from_id(id))
                        f.write("\n")
                        f.write(get_description_from_id(id))
                        f.write("\n")
                        matos = get_matos_from_id(id)
                        if matos != [] :
                            for item in matos :
                                f.write(item)
                        f.write("\n\n")

                f.close()

        except FileNotFoundError :
            pass

    def setup_dates_le(self, year, week_nbr): # Peuplement desLineEdits des dates du calendrier
        monday_list = []
        monday_iso_str = """%s %s %s""" %(year, week_nbr, 1)
        monday_return_date = datetime.strptime(monday_iso_str, '%G %V %u').__str__()
        iso_date = monday_return_date.split(" ")[0]
        iso_year = iso_date.split("-")[0]
        iso_month = iso_date.split("-")[1]
        iso_day = iso_date.split("-")[2]
        monday_list.append(iso_day)
        monday_list.append(iso_month)
        monday_list.append(iso_year)
        monday = "/".join(monday_list)
        self.le_monday.setText(monday)

        tuesday_list = []
        tuesday_iso_str = """%s %s %s""" %(year, week_nbr, 2)
        tuesday_return_date = datetime.strptime(tuesday_iso_str, '%G %V %u').__str__()
        iso_date = tuesday_return_date.split(" ")[0]
        iso_year = iso_date.split("-")[0]
        iso_month = iso_date.split("-")[1]
        iso_day = iso_date.split("-")[2]
        tuesday_list.append(iso_day)
        tuesday_list.append(iso_month)
        tuesday_list.append(iso_year)
        tuesday = "/".join(tuesday_list)
        self.le_tuesday.setText(tuesday)

        wednesday_list = []
        wednesday_iso_str = """%s %s %s""" %(year, week_nbr, 3)
        wednesday_return_date = datetime.strptime(wednesday_iso_str, '%G %V %u').__str__()
        iso_date = wednesday_return_date.split(" ")[0]
        iso_year = iso_date.split("-")[0]
        iso_month = iso_date.split("-")[1]
        iso_day = iso_date.split("-")[2]
        wednesday_list.append(iso_day)
        wednesday_list.append(iso_month)
        wednesday_list.append(iso_year)
        wednesday = "/".join(wednesday_list)
        self.le_wednesday.setText(wednesday)

        thirsday_list = []
        thirsday_iso_str = """%s %s %s""" %(year, week_nbr, 4)
        thirsday_return_date = datetime.strptime(thirsday_iso_str, '%G %V %u').__str__()
        iso_date = thirsday_return_date.split(" ")[0]
        iso_year = iso_date.split("-")[0]
        iso_month = iso_date.split("-")[1]
        iso_day = iso_date.split("-")[2]
        thirsday_list.append(iso_day)
        thirsday_list.append(iso_month)
        thirsday_list.append(iso_year)
        thirsday = "/".join(thirsday_list)
        self.le_thirsday.setText(thirsday)

        friday_list = []
        friday_iso_str = """%s %s %s""" %(year, week_nbr, 5)
        friday_return_date = datetime.strptime(friday_iso_str, '%G %V %u').__str__()
        iso_date = friday_return_date.split(" ")[0]
        iso_year = iso_date.split("-")[0]
        iso_month = iso_date.split("-")[1]
        iso_day = iso_date.split("-")[2]
        friday_list.append(iso_day)
        friday_list.append(iso_month)
        friday_list.append(iso_year)
        friday = "/".join(friday_list)
        self.le_friday.setText(friday)

        saturday_list = []
        saturday_iso_str = """%s %s %s""" %(year, week_nbr, 6)
        saturday_return_date = datetime.strptime(saturday_iso_str, '%G %V %u').__str__()
        iso_date = saturday_return_date.split(" ")[0]
        iso_year = iso_date.split("-")[0]
        iso_month = iso_date.split("-")[1]
        iso_day = iso_date.split("-")[2]
        saturday_list.append(iso_day)
        saturday_list.append(iso_month)
        saturday_list.append(iso_year)
        saturday = "/".join(saturday_list)
        self.le_saturday.setText(saturday)

        sunday_list = []
        sunday_iso_str = """%s %s %s""" %(year, week_nbr, 7)
        sunday_return_date = datetime.strptime(sunday_iso_str, '%G %V %u').__str__()
        iso_date = sunday_return_date.split(" ")[0]
        iso_year = iso_date.split("-")[0]
        iso_month = iso_date.split("-")[1]
        iso_day = iso_date.split("-")[2]
        sunday_list.append(iso_day)
        sunday_list.append(iso_month)
        sunday_list.append(iso_year)
        sunday = "/".join(sunday_list)
        self.le_sunday.setText(sunday)

### END OF CalendarView CLASS #########################################################

app = QtWidgets.QApplication(sys.argv)
ex = App()
ex.show()
sys.exit(app.exec_())
