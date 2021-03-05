# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
import logging

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QToolTip, QMessageBox, QLabel)
from PyQt5.QtCore import *
from PyQt5.QtGui import *

CUR_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(CUR_DIR, "data")
ICON_FILE = os.path.join(DATA_DIR, "icone.png")
REX_FILE = os.path.join(DATA_DIR, "installer_rex.png")
LOG_FILE = os.path.join(CUR_DIR, "log/mat_app.log")

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MATOSAURUS SUITE INSTALLER - Alpha")
        self.setStyleSheet("background-color: rgb(200, 200, 255)")
        self.setMinimumWidth(750)
        self.setMinimumHeight(508)
        self.setMaximumWidth(750)
        self.setMaximumHeight(508)
        self.setWindowIcon(QtGui.QIcon(ICON_FILE))
        
        self.windowUI()
        self.setup_connections()
        self.show()

    def windowUI(self):
        self.grid_layout = QtWidgets.QGridLayout(self)

        self.lbl_title = QtWidgets.QLabel("Bienvenue dans le programme d'installation \nde la suite MATOSAURUS.")
        self.lbl_title.setFont(QtGui.QFont("sanserif", 18))
        self.lbl_title.setStyleSheet('color:black')

        self.btn_continue = QtWidgets.QPushButton("Continuer", self)

        self.lbl_rex_pic = QtWidgets.QLabel(self)
        pixmap = QPixmap(REX_FILE)
        self.lbl_rex_pic.setPixmap(pixmap)

        self.grid_layout.addWidget(self.lbl_rex_pic, 0, 0, 2, 1)
        self.grid_layout.addWidget(self.lbl_title, 0, 1, 1, 4)
        self.grid_layout.addWidget(self.btn_continue, 1, 4, 1, 1)

    def setup_connections(self):
        self.btn_continue.clicked.connect(self.window2)

    def window2(self):
        self.w = Window2()
        self.w.show()
        self.hide()

class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MATOSAURUS SUITE INSTALLER - Alpha")
        self.setStyleSheet("background-color: rgb(200, 200, 255)")
        self.setMinimumWidth(750)
        self.setMinimumHeight(508)
        self.setMaximumWidth(750)
        self.setMaximumHeight(508)
        self.setWindowIcon(QtGui.QIcon(ICON_FILE))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())

## Choisir la version à installer.

## Choisir le chemin du dossier d'installation.

## Choisir l'adresse de la base de données SQL.

## Demander confirmation de création d'un racourci bureau (Oui par défaut).

## Copier les fichier de l'application dans le dossier de destination.

## Appuyer sur "Quitter" pour quitter le programme d'installation.
