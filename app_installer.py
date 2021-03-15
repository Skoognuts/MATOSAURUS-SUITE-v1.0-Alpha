# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
import logging

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QToolTip, QMessageBox, QLabel, QFileDialog)
from PyQt5.QtCore import *
from PyQt5.QtGui import *

CUR_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(CUR_DIR, "data")
ICON_FILE = os.path.join(DATA_DIR, "icone.png")
REX_FILE = os.path.join(DATA_DIR, "installer_rex.png")
LOG_FILE = os.path.join(CUR_DIR, "log/mat_app.log")

class Version(str):
    def __init__(self, vers):
        self.vers = ""

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MATOSAURUS SUITE INSTALLER - Alpha")
        self.setStyleSheet("background-color: rgb(215, 215, 255)")
        self.setMinimumWidth(700)
        self.setMinimumHeight(508)
        self.setMaximumWidth(700)
        self.setMaximumHeight(508)
        self.setWindowIcon(QtGui.QIcon(ICON_FILE))
        
        self.windowUI()
        self.setup_connections()
        self.show()

    def windowUI(self):
        self.grid_layout = QtWidgets.QGridLayout(self)

        self.lbl_desc_1 = QtWidgets.QLabel("Vous êtes sur le point d'installer la suite MATOSAURUS sur votre \nordinateur.")
        self.lbl_desc_2 = QtWidgets.QLabel("Avant de démarrer l'installation, il est recommandé de fermer toutes les \nautres applications. Cela permettra la mise à jour de certains fichiers \nsystème sans redémarrer votre ordinateur.")
        self.lbl_desc_3 = QtWidgets.QLabel("Cliquez sur Suivant pour continuer.")

        self.lbl_desc_1.setFont(QtGui.QFont("sanserif", 10))
        self.lbl_desc_2.setFont(QtGui.QFont("sanserif", 10))
        self.lbl_desc_3.setFont(QtGui.QFont("sanserif", 10))

        self.lbl_title = QtWidgets.QLabel("Bienvenue dans le programme \nd'installation de la suite MATOSAURUS.")
        self.lbl_title.setFont(QtGui.QFont("sanserif", 18))
        self.lbl_title.setStyleSheet('color:black')

        self.btn_continue_1 = QtWidgets.QPushButton("Suivant  >", self)
        self.btn_cancel_1 = QtWidgets.QPushButton("Annuler", self)

        self.btn_continue_1.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.btn_cancel_1.setStyleSheet("background-color: rgb(150, 150, 255)")

        self.lbl_rex_pic = QtWidgets.QLabel(self)
        pixmap = QPixmap(REX_FILE)
        self.lbl_rex_pic.setPixmap(pixmap)

        self.grid_layout.addWidget(self.lbl_rex_pic, 0, 0, 6, 1)
        self.grid_layout.addWidget(self.lbl_title, 0, 1, 1, 4)
        self.grid_layout.addWidget(self.lbl_desc_1, 1, 1, 1, 4)
        self.grid_layout.addWidget(self.lbl_desc_2, 2, 1, 1, 4)
        self.grid_layout.addWidget(self.lbl_desc_3, 3, 1, 1, 4)
        self.grid_layout.addWidget(self.btn_continue_1, 5, 3, 1, 1)
        self.grid_layout.addWidget(self.btn_cancel_1, 5, 4, 1, 1)

        self.grid_layout.setRowStretch(0, 1)
        self.grid_layout.setRowStretch(1, 2)
        self.grid_layout.setRowStretch(2, 2)
        self.grid_layout.setRowStretch(3, 2)
        self.grid_layout.setRowStretch(4, 3)

    def setup_connections(self):
        self.btn_continue_1.clicked.connect(self.window2)
        self.btn_cancel_1.clicked.connect(self.cancel)

    def cancel(self):
        self.close()

    def window2(self):
        self.w = Window2()
        self.w.show()
        self.close()

class Window2(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MATOSAURUS SUITE INSTALLER - Alpha")
        self.setStyleSheet("background-color: rgb(215, 215, 255)")
        self.setMinimumWidth(700)
        self.setMinimumHeight(508)
        self.setMaximumWidth(700)
        self.setMaximumHeight(508)
        self.setWindowIcon(QtGui.QIcon(ICON_FILE))

        self.windowUI()
        self.setup_connections()

    def windowUI(self):
        self.grid_layout = QtWidgets.QGridLayout(self)

        self.lbl_title = QtWidgets.QLabel("Choisir la version du programme à \ninstaller.")
        self.lbl_title.setFont(QtGui.QFont("sanserif", 18))
        self.lbl_title.setStyleSheet('color:black')

        self.lbl_desc_1 = QtWidgets.QLabel("Veuillez choisir la version du programme à installer. Il n'est possible \nd'en choisir qu'une.")
        self.lbl_desc_1.setFont(QtGui.QFont("sanserif", 10))

        self.cb_prog_1 = QtWidgets.QCheckBox(" -  MATOSAURUS REX :", self)
        self.cb_prog_1.setFont(QtGui.QFont("sanserif", 12))
        self.lbl_prog_1 = QtWidgets.QLabel("    MATOSAURUS REX est la version principale du programme. Elle \npermet la gestion complète des missions, du stock et dispose d'un accès \npermanent à la base de données.")
        self.lbl_prog_1.setFont(QtGui.QFont("sanserif", 10))

        self.cb_prog_2 = QtWidgets.QCheckBox(" -  MATOSAURUS VIEWER :", self)
        self.cb_prog_2.setFont(QtGui.QFont("sanserif", 12))
        self.lbl_prog_2 = QtWidgets.QLabel("    MATOSAURUS VIEWER est la version allégée du programme. Elle \npermet la visualisation simple du stock. Elle dispose quand même d'un \naccès permanent à la base de données.")
        self.lbl_prog_2.setFont(QtGui.QFont("sanserif", 10))

        self.btn_continue_2 = QtWidgets.QPushButton("Suivant  >", self)
        self.btn_back_2 = QtWidgets.QPushButton("< Retour", self)

        self.btn_continue_2.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.btn_back_2.setStyleSheet("background-color: rgb(150, 150, 255)")

        self.lbl_rex_pic = QtWidgets.QLabel(self)
        pixmap = QPixmap(REX_FILE)
        self.lbl_rex_pic.setPixmap(pixmap)

        self.grid_layout.addWidget(self.lbl_title, 0, 1, 1, 4)
        self.grid_layout.addWidget(self.lbl_desc_1, 1, 1, 1, 4)

        self.grid_layout.addWidget(self.cb_prog_1, 2, 1, 1, 1)
        self.grid_layout.addWidget(self.lbl_prog_1, 3, 1, 1, 4)

        self.grid_layout.addWidget(self.cb_prog_2, 4, 1, 1, 1)
        self.grid_layout.addWidget(self.lbl_prog_2, 5, 1, 1, 4)

        self.grid_layout.addWidget(self.lbl_rex_pic, 0, 0, 7, 1)
        self.grid_layout.addWidget(self.btn_continue_2, 6, 4, 1, 1)
        self.grid_layout.addWidget(self.btn_back_2, 6, 3, 1, 1)

        self.grid_layout.setRowStretch(0, 1)
        self.grid_layout.setRowStretch(1, 2)
        self.grid_layout.setRowStretch(2, 1)
        self.grid_layout.setRowStretch(3, 2)
        self.grid_layout.setRowStretch(4, 1)
        self.grid_layout.setRowStretch(5, 2)

    def setup_connections(self):
        self.cb_prog_1.clicked.connect(self.cb_1_setup)
        self.cb_prog_2.clicked.connect(self.cb_2_setup)
        self.btn_continue_2.clicked.connect(self.window3)
        self.btn_back_2.clicked.connect(self.window1)

    def cb_1_setup(self):
        if self.cb_prog_1.isChecked() :
            self.cb_prog_2.setChecked(False)

    def cb_2_setup(self):
        if self.cb_prog_2.isChecked() :
            self.cb_prog_1.setChecked(False)

    def window1(self):
        self.w = Window()
        self.w.show()
        self.close()

    def window3(self):
        global version
        if self.cb_prog_1.isChecked() :
            version = Version("Matosaurus Rex")
            self.w = Window3()
            self.w.show()
            self.hide()
        elif self.cb_prog_2.isChecked() :
            version = Version("Matosaurus Viewer")
            self.w = Window3()
            self.w.show()
            self.hide()
        else :
            QtWidgets.QMessageBox.warning(self, "ATTENTION", "Veuillez choisir au moins une version.          ")

class Window3(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MATOSAURUS SUITE INSTALLER - Alpha")
        self.setStyleSheet("background-color: rgb(215, 215, 255)")
        self.setMinimumWidth(700)
        self.setMinimumHeight(508)
        self.setMaximumWidth(700)
        self.setMaximumHeight(508)
        self.setWindowIcon(QtGui.QIcon(ICON_FILE))

        self.windowUI()
        self.setup_default()
        self.setup_connections()
    
    def windowUI(self):
        self.grid_layout = QtWidgets.QGridLayout(self)

        self.lbl_title = QtWidgets.QLabel("Choisir le dossier de destination.")
        self.lbl_title.setFont(QtGui.QFont("sanserif", 18))
        self.lbl_title.setStyleSheet('color:black')

        self.lbl_desc_3 = QtWidgets.QLabel("Veuillez choisir le dossier dans lequel sera installée le programme. \nPar défaut, celui-ci sera installé dans un dossier à la racine du disque.")

        self.lbl_desc_3.setFont(QtGui.QFont("sanserif", 10))

        self.btn_continue_3 = QtWidgets.QPushButton("Suivant  >", self)
        self.btn_back_3 = QtWidgets.QPushButton("< Retour", self)
        self.btn_browse_3 = QtWidgets.QPushButton("Parcourir", self)
        self.le_browse_3 = QtWidgets.QLineEdit("", self)

        self.btn_continue_3.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.btn_back_3.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.btn_browse_3.setStyleSheet("background-color: rgb(150, 150, 255)")
        self.le_browse_3.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.le_browse_3.setReadOnly(True)

        self.lbl_rex_pic = QtWidgets.QLabel(self)
        pixmap = QPixmap(REX_FILE)
        self.lbl_rex_pic.setPixmap(pixmap)

        self.grid_layout.addWidget(self.lbl_title, 0, 1, 1, 4)
        self.grid_layout.addWidget(self.lbl_desc_3, 1, 1, 1, 4)

        self.grid_layout.addWidget(self.le_browse_3, 2, 1, 1, 3)
        self.grid_layout.addWidget(self.btn_browse_3, 2, 4, 1, 1)

        self.grid_layout.addWidget(self.lbl_rex_pic, 0, 0, 6, 1)
        self.grid_layout.addWidget(self.btn_continue_3, 5, 4, 1, 1)
        self.grid_layout.addWidget(self.btn_back_3, 5, 3, 1, 1)

    def setup_default(self):
        global DISC
        global default_path
        DISC = CUR_DIR.split(":/")[0]
        vers = Version(version)
        default_path = f"{DISC.capitalize()}:\\{vers}"
        self.le_browse_3.setText(default_path)

    def setup_connections(self):
        self.btn_continue_3.clicked.connect(self.window4)
        self.btn_back_3.clicked.connect(self.window2)
        self.btn_browse_3.clicked.connect(self.browser)

    def browser(self):
        global path
        root_path = f"{DISC.capitalize()}:\\"
        path = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier d'installation :", root_path)
        if path != default_path :
            self.le_browse_3.setText(path)
        if path == "" :
            path = default_path
            self.le_browse_3.setText(path)
        
    def window2(self):
        self.w = Window2()
        self.w.show()
        self.close()

    def window4(self):
        self.w = Window4()
        self.w.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())

## Choisir l'adresse de la base de données SQL.

## Demander confirmation de création d'un racourci bureau (Oui par défaut).

## Copier les fichier de l'application dans le dossier de destination.

## Appuyer sur "Quitter" pour quitter le programme d'installation.
