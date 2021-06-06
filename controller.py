#! /usr/bin/env python3
# coding: utf-8

import os
import model
from view import Menu
import re

NAME_CONTROL_EXPRESSION = re.compile(r"^[A-Za-z- ]+$")

DATE_OF_BIRTH_EXPRESSION = re.compile(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}")

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
            self.player_creator_ctrl()
        elif choice == 1: # lancer la fonction de création de tournoi
            pass
    #A continuer!

    def player_creator_ctrl(self):
        """function which control the user input"""
        player_information = {}
        last_name = self.player_last_name_creator_ctrl()
        if last_name:
            player_information["last_name"] = last_name
            first_name = self.player_first_name_creator_ctrl()
            if first_name:
                player_information["first_name"] = first_name
                date_of_birth = self.player_date_of_brith_creator_ctrl()
                if date_of_birth:
                    player_information["date_of_birth"] = date_of_birth
                    print(player_information)
                else:
                    self.main_menu_ctrl()
            else:
                self.main_menu_ctrl()
        else:
            self.main_menu_ctrl()


    def player_last_name_creator_ctrl(self):
        """player last name creator menu controller function"""

        while True:
            last_name = self.menu.player_last_name()
            if last_name == "quit":
                return None
            elif NAME_CONTROL_EXPRESSION.match(last_name) is not None:
                return last_name
            else:
                print("Nom incorect")

    def player_first_name_creator_ctrl(self):
        """player last name creator menu controller function"""

        while True:
            first_name = self.menu.player_first_name()
            if first_name == "quit":
                return None
            elif NAME_CONTROL_EXPRESSION.match(first_name) is not None:
                return first_name
            else:
                print("Prénom incorect")

    def player_date_of_brith_creator_ctrl(self):
        """player last name creator menu controller function"""

        while True:
            date_of_birth = self.menu.player_date_of_birth()
            if date_of_birth == "quit":
                return None
            elif DATE_OF_BIRTH_EXPRESSION.match(date_of_birth) is not None:
                return date_of_birth
            else:
                print("La date est incorect")





browser = Browse()
browser.main_menu_ctrl()

