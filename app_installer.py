# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
import logging

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from api_mat_v_2 import *

CUR_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(CUR_DIR, "data")
ICON_FILE = os.path.join(DATA_DIR, "icone.png")
LOG_FILE = os.path.join(CUR_DIR, "log/mat_app_installer.log")

logging.basicConfig(level = logging.DEBUG, filename = LOG_FILE, filemode = "w", format = "%(levelname)s - %(message)s")
logging.debug("MATOSAURUS INSTALLER LAUNCHED")

## Créer l'interface utilisateur.

## Choisir la version à installer.

## Choisir le chemin du dossier d'installation.

## Choisir l'adresse de la base de données SQL.

## Demander confirmation de création d'un racourci bureau (Oui par défaut).

## Copier les fichier de l'application dans le dossier de destination.

## Appuyer sur "Quitter" pour quitter le programme d'installation.
