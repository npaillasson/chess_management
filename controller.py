#! /usr/bin/env python3
# coding: utf-8

import os
import model
from view import Menu

MAIN_MENU_CHOICES = ["Créer un joueur", "Créer un tournoi", "Gérer un tournoi en cours",
                     "Générer des rapports", "Règlages", "Quitter le logiciel"]

CONFIRMATION_OR_CORRECTION_MENU = ["Valider !", "Corriger"]

PLAYERS_INFORMATION_CORRECTION_MENU = ["Nom", "Prénom", "Date de naissance", "Genre", "Rang"]

TOURNAMENTS_INFORMATION_CORRECTION_MENU = ["Nom", "Lieu", "Date", "Nombre de tours", "Joueurs",
                                           "Contrôle du temps", "Déscription"]


class Browse:
    """class which manage the navigation of the user according to his input"""

    def __init__(self, main_menu_choices=MAIN_MENU_CHOICES,
                 confirmation_or_correction_menu=CONFIRMATION_OR_CORRECTION_MENU,
                 players_information_correction_menu=PLAYERS_INFORMATION_CORRECTION_MENU,
                 tournaments_information_correction_menu=TOURNAMENTS_INFORMATION_CORRECTION_MENU):

        self.main_menu_choices = main_menu_choices
        self.confirmation_or_correction_menu = confirmation_or_correction_menu
        self.players_information_correction_menu = players_information_correction_menu
        self.tournaments_information_correction_menu = tournaments_information_correction_menu

        self.menu = Menu(self.main_menu_choices)

    def main_menu_ctrl(self):
        """main menu controller function"""
        choice = self.menu.main_menu()
        if choice == 0: # Lancer la fonction de creation de joueur
            pass
        elif choice == 1: # lancer la fonction de création de tournoi
            pass
    #A continuer!



browser = Browse()
browser.main_menu_ctrl()

