#! /usr/bin/env python3
# coding: utf-8

import os
import model
from view import ChoiceMenu, FieldMenu, Sign, ValidationMenu
import time
from datetime import datetime
import re

#permet de vérifier que le nom ne contient que des lettres
STR_CONTROL_EXPRESSION = re.compile(r"^[A-Za-z- ]+$")

#permet de vérifier le format de la date
DATE_OF_BIRTH_EXPRESSION = re.compile(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$")

#permet de vérifier le format du rang du joueur
RANK_EXPRESSION = re.compile(r"^[0-9]+$")

#contient les choix du menu principale
MAIN_MENU_CHOICES = ["Créer un joueur", "Créer un tournoi", "Gérer un tournoi en cours",
                     "Générer des rapports", "Règlages", "Quitter le logiciel"]

#contient les choix du menu de confirmation
CORRECTION_MENU_CHOICES = ["Valider !", "Corriger", "Annuler"]

#NE SEMBLE SERVIR A RIEN
TOURNAMENTS_INFORMATION_CORRECTION_MENU = ["Nom", "Lieu", "Date", "Nombre de tours", "Joueurs",
                                           "Contrôle du temps", "Déscription"]


class Browse:
    """class which manage the navigation of the user according to his input"""

    #Initi
    def __init__(self, main_menu_choices=MAIN_MENU_CHOICES,
                 correction_menu_choices=CORRECTION_MENU_CHOICES,
                 tournaments_information_correction_menu=TOURNAMENTS_INFORMATION_CORRECTION_MENU,
                 str_control_expression = STR_CONTROL_EXPRESSION):

        #menus choices
        self.main_menu_choices = main_menu_choices
        self.correction_menu_choices = correction_menu_choices
        self.tournaments_information_correction_menu = tournaments_information_correction_menu

        #regular expression
        self.str_control_expression = str_control_expression

        self.choice_menu = ChoiceMenu()
        self.correction_menu = ValidationMenu(correction_menu_choices)
        self.sign = Sign()
        self.field_menu = FieldMenu()


    def main_menu_control(self):
        """main menu controller function"""
        choice = self.choice_menu.printing_menu(self.main_menu_choices)
        if choice == 0: # Lancer la fonction de creation de joueur
            self.player_creator_control()
        elif choice == 1: # lancer la fonction de création de tournoi
            pass
    #A continuer!

    #fonction principale du menu de création de joueur
    def player_creator_control(self):
        """function which control the user input"""
        player_information = {}
        last_name = self.str_data_control("nom", "veuillez saisir le nom du joueur: ")
        if last_name:
            player_information["last_name"] = last_name
            first_name = self.player_first_name_creator_control()
            if first_name:
                player_information["first_name"] = first_name
                date_of_birth = self.player_date_of_brith_creator_control()
                if date_of_birth:
                    player_information["date_of_birth"] = date_of_birth
                    rank = self.player_rank_creator_control()
                    if rank:
                        player_information["rank"] = rank
                        choice = self.correction_menu.\
                            printing_correction_menu(players_formatting(player_information))
                        if choice == 0:
                            print("OK!")
                            self.main_menu_control()
                        elif choice == 1:
                            self.player_creator_control()
                        else:
                            self.main_menu_control()
                    else:
                        self.main_menu_control()
                else:
                    self.main_menu_control()
            else:
                self.main_menu_control()
        else:
            self.main_menu_control()

    #fonction secondaire du menu de création des joueur récupère le nom
    def str_data_control(self, data_name, message):
        """Method which control str data (exemple : name)"""

        while True:
            str_data = self.field_menu.printing_field(message)
            if str_data == "quit":
                return None
            elif self.str_control_expression.match(str_data) is not None:
                return str_data
            else:
                print("{} incorect".format(data_name))

    # fonction secondaire du menu de création des joueur récupère le prénom
    def player_first_name_creator_control(self):
        """player last name creator menu controller function"""

        while True:
            first_name = self.field_menu.printing_field("veuillez saisir le prénom du joueur: ")
            if first_name == "quit":
                return None
            elif STR_CONTROL_EXPRESSION.match(first_name) is not None:
                return first_name
            else:
                print("Prénom incorect")

    # fonction secondaire du menu de création des joueur qui vérifie la validité de la date
    def player_date_of_brith_creator_control(self):
        """player last name creator menu controller function"""

        while True:
            date_of_birth = self.field_menu.printing_field("veuillez saisir la date de naissance du joueur:")
            if date_of_birth == "quit":
                return None
            elif DATE_OF_BIRTH_EXPRESSION.match(date_of_birth) is not None: #a mettre dans verif de date?

                check_date_validity = self.date_checking(date_of_birth)
                if check_date_validity:
                    return date_of_birth
                else:
                    print("La date est incorect")
            else:
                print("La date est incorect")

    # fonction secondaire du menu de création des joueur récupère la date de naissance
    def date_checking(self,date_of_birth):
        """function which check the date validity"""
        day_of_birth = int(date_of_birth[:2])
        month_of_birth = int(date_of_birth[3:5])
        year_of_birth = int(date_of_birth[6:])
        try:
            time_stamp = datetime(year_of_birth, month_of_birth, day_of_birth).timestamp()
        except ValueError:
            return False
        else:
            if time_stamp <= time.time():
                return True
            else:
                return False

    # fonction secondaire du menu de création des joueur récupère le rang du joueur
    def player_rank_creator_control(self):
        """player last name creator menu controller function"""

        while True:
            rank = self.field_menu.printing_field("veuillez saisir le rang du joueur: ")
            if rank == "quit":
                return None
            elif RANK_EXPRESSION.match(rank) is not None:
                return rank
            else:
                print("Le rang rensseigné est incorect")

def players_formatting(player_information):
    """Function which take a dict with players information and format it"""
    return "Nom : {}\nPrénom : {} \nDate de naissance : {}\nRang : {}".format(player_information["last_name"],
                                                                              player_information["first_name"],
                                                                              player_information["date_of_birth"],
                                                                              player_information["rank"])





browser = Browse()
browser.main_menu_control()

