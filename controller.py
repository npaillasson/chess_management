#! /usr/bin/env python3
# coding: utf-8

import os
import model

import time
from datetime import datetime
import re
from view import ChoiceMenu, FieldMenu, Sign, ValidationMenu
from menu import MAIN_MENU_CHOICES, PLAYERS_FIELD_MESSAGE, CORRECTION_MENU_CHOICES,\
    VALIDATION_MENU_MESSAGE,str_controller, int_controller, date_controller, no_controller
from model import Player, PlayersDataBase, Tournament, TournamentsDataBase, Match

#permet de vérifier que le nom ne contient que des lettres
STR_CONTROL_EXPRESSION = re.compile(r"^[A-Za-z- ]+$")

#permet de vérifier le format de la date
DATE_CONTROL_EXPRESSION = re.compile(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$")

#permet de vérifier le format du rang du joueur
INT_CONTROL_EXPRESSION = re.compile(r"^[0-9]+$")

#NE SEMBLE SERVIR A RIEN
TOURNAMENTS_INFORMATION_CORRECTION_MENU = ["Nom", "Lieu", "Date", "Nombre de tours", "Joueurs",
                                           "Contrôle du temps", "Déscription"]


class Browse:
    """class which manage the navigation of the user according to his input"""

    #Initi
    def __init__(self, main_menu_choices=MAIN_MENU_CHOICES,
                 correction_menu_choices=CORRECTION_MENU_CHOICES,
                 tournaments_information_correction_menu=TOURNAMENTS_INFORMATION_CORRECTION_MENU,
                 str_control_expression=STR_CONTROL_EXPRESSION,
                 date_control_expression=DATE_CONTROL_EXPRESSION,
                 int_control_expression=INT_CONTROL_EXPRESSION,
                 players_database=PlayersDataBase,
                 tournaments_database=TournamentsDataBase):

        #menus choices
        self.main_menu_choices = main_menu_choices
        self.correction_menu_choices = correction_menu_choices
        self.tournaments_information_correction_menu = tournaments_information_correction_menu

        #regular expression
        self.str_control_expression = str_control_expression
        self.date_control_expression = date_control_expression
        self.int_control_expression = int_control_expression

        #View instaciation
        self.choice_menu = ChoiceMenu()
        self.validation_menu = ValidationMenu(correction_menu_choices)
        self.sign = Sign()
        self.field_menu = FieldMenu()

        #DataBase
        self.players_database = players_database
        self.tournaments_database = tournaments_database


    def main_menu_control(self):
        """main menu controller function"""
        choice = self.choice_menu.printing_menu_index(self.main_menu_choices)
        if choice == 0: # Lancer la fonction de creation de joueur
            self.player_creator_control()
        elif choice == 1: # lancer la fonction de création de tournoi
            pass
    #A continuer!

    #fonction principale du menu de création de joueur
    def player_creator_control(self):
        """function which control the user input"""
        player_information = {}
        last_name = self.data_controller("last_name")
        if last_name:
            player_information["last_name"] = last_name
            first_name = self.data_controller("first_name")
            if first_name:
                player_information["first_name"] = first_name
                date_of_birth = self.data_controller("date_of_birth")
                if date_of_birth:
                    player_information["date_of_birth"] = date_of_birth
                    gender = self.validation_menu.printing_validation_menu(VALIDATION_MENU_MESSAGE["gender"][0],
                                                                           VALIDATION_MENU_MESSAGE["gender"][1])
                    player_information["gender"] = gender
                    rank = self.data_controller("rank")
                    if rank:
                        player_information["rank"] = rank
                        choice = self.validation_menu.\
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
    def data_controller(self, data_name):
        """Method which control str data (exemple : name)"""

        while True:
            data = self.field_menu.printing_field(PLAYERS_FIELD_MESSAGE[data_name][0])
            if data == "quit":
                return None
            elif data_name in str_controller:
                if self.str_control_expression.match(data) is not None:
                    return data
                else:
                    self.sign.printing_sign(PLAYERS_FIELD_MESSAGE[data_name][1])
            elif data_name in date_controller:
                if self.date_control(data) is not None:
                    return data
                else:
                    self.sign.printing_sign(PLAYERS_FIELD_MESSAGE[data_name][1])
            elif data_name in int_controller:
                if self.int_control_expression.match(data) is not None:
                    return data
                else:
                    self.sign.printing_sign(PLAYERS_FIELD_MESSAGE[data_name][1])

    # fonction secondaire du menu de création des joueur qui vérifie la validité de la date
    def date_control(self, data):
        """player last name creator menu controller function"""

        if self.date_control_expression.match(data) is not None:
            day = int(data[:2])
            month = int(data[3:5])
            year = int(data[6:])
            try:
                time_stamp = datetime(year, month, day).timestamp()
            except ValueError:
                return None
            else:
                if time_stamp <= time.time():
                    return data
                else:
                    return None
        else:
            return None

    def set_menu(self, data_name):
        """Method which allows to set the menu and return the value"""

        if data_name in no_controller:
            value = self.validation_menu.printing_validation_menu(VALIDATION_MENU_MESSAGE[data_name][0],
                                                                  VALIDATION_MENU_MESSAGE[data_name][1])
            return value
        else:
            value = self.data_controller(data_name)
            if value:
                return value
            else:
                return self.main_menu_control()

if 1==2:
    #    def adding_player_in_database(self, player_information):
        """function which add a player into the database"""
    #        for element in player_information:

    #       self.players_database.append()

def players_formatting(player_information):
    """Function which take a dict with players information and format it"""
    return "Nom : {}\nPrénom : {} \nDate de naissance : {}\nGenre :{}\nRang : {}".\
        format(player_information["last_name"],
               player_information["first_name"],
               player_information["date_of_birth"],
               player_information["gender"],
               player_information["rank"])






browser = Browse()
browser.main_menu_control()

