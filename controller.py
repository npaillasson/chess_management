#! /usr/bin/env python3
# coding: utf-8

import os
import time
from datetime import datetime
import re
from view import ChoiceMenu, FieldMenu, Sign, ValidationMenu
from menu import MAIN_MENU_CHOICES, PLAYERS_FIELD_MESSAGE, CORRECTION_MENU_CHOICES,\
    VALIDATION_MENU_MESSAGE, players_formatting
from model import Player, PlayersDataBase, Tournament, TournamentsDataBase, Match, DAO_PATH
import menu

# regex that allows to check if the field contains only lettres or space or "-".
STR_CONTROL_EXPRESSION = re.compile(r"^[A-Za-z- ]+$")

# regex which allows to check if the field contains a date in right format
DATE_CONTROL_EXPRESSION = re.compile(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$")

# regex that allows to check if a field is only composed by number
INT_CONTROL_EXPRESSION = re.compile(r"^[0-9]+$")

# list of adapted data_controllers
str_controller = ["last_name", "first_name"]
date_controller = ["date_of_birth"]
int_controller = ["rank"]
no_controller = ["gender"]


class Browse:
    """class which manage the navigation of the user according to his input"""

    def __init__(self, main_menu_choice,
                 correction_menu_choice,
                 str_control_expression,
                 date_control_expression,
                 int_control_expression,
                 players_dao,
                 tournaments_dao):

        # menus choice
        self.main_menu_choice = main_menu_choice
        self.correction_menu_choice = correction_menu_choice

        # regular expression
        self.str_control_expression = str_control_expression
        self.date_control_expression = date_control_expression
        self.int_control_expression = int_control_expression

        # instancing view
        self.choice_menu = ChoiceMenu()
        self.validation_menu = ValidationMenu(correction_menu_choice)
        self.sign = Sign()
        self.field_menu = FieldMenu()

        # instancing DataBase
        self.players_dao = players_dao()
        self.tournaments_dao = tournaments_dao()

    def main_menu_control(self):
        """main menu controller function"""
        choice = self.choice_menu.printing_menu_index(self.main_menu_choice)
        if choice == 0:  # launch the players creation menu
            self.player_creator_control()
        elif choice == 1:  # launch the tournaments creation menu
            pass
    #A continuer!

    def correction_menu_control(self, parent_menu):
        """function that allows to confirm, cancel or correct an entry"""

    # function that manage the players creation feature
    def player_creator_control(self):
        """function which control the user input"""
        player_information = {}
        last_name = self.set_menu("last_name")
        player_information["last_name"] = last_name
        first_name = self.set_menu("first_name")
        player_information["first_name"] = first_name
        date_of_birth = self.set_menu("date_of_birth")
        player_information["date_of_birth"] = date_of_birth
        gender = self.set_menu("gender")
        player_information["gender"] = gender
        rank = self.set_menu("rank")
        player_information["rank"] = rank
        choice = self.validation_menu.\
            printing_correction_menu(players_formatting(player_information))
        if choice == 0:
            print("OK!")
            self.add_player_in_dao(player_information)
        elif choice == 1:
            self.player_creator_control()
        else:
            self.main_menu_control()

    def data_controller(self, data_name):
        """Method which control user's inputs conformity"""

        while True:
            data = self.field_menu.printing_field(PLAYERS_FIELD_MESSAGE[data_name][0])
            if data == "quit":
                return None
            elif data_name in str_controller:
                if self.str_control_expression.match(data) is not None:
                    return data.strip()
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

    # which checks if the date exists and if it has already been exceeded.
    def date_control(self, data):
        """Function that check the date conformity"""

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

        return None

    def set_menu(self, data_name):
        """Method which allows to set the menu and return the value"""

        if data_name in no_controller:
            value = self.validation_menu.printing_proposal_menu(VALIDATION_MENU_MESSAGE[data_name][0],
                                                                VALIDATION_MENU_MESSAGE[data_name][1],
                                                                index=False)
            return value
        else:
            value = self.data_controller(data_name)
            if value:
                return value
            else:
                return self.main_menu_control()

    def add_player_in_dao(self, player_information):
        """function which add a player into the database"""

        new_player = Player(player_information["last_name"],
                            player_information["first_name"],
                            player_information["date_of_birth"],
                            player_information["gender"],
                            player_information["rank"])

        if self.players_dao.players_exists(new_player):
            self.sign.printing_sign(menu.player_already_exists)

        else:
            self.players_dao.players_list.append(new_player)
            self.players_dao.save_dao()

        self.main_menu_control()


def program_init():
    """Function that checks if the database already exists"""

    if not os.path.exists("data/"):
        os.mkdir("data")
        return False
    else:
        if not os.path.exists(DAO_PATH):
            return False
        else:
            return True


browser = Browse(main_menu_choice=MAIN_MENU_CHOICES,
                 correction_menu_choice=CORRECTION_MENU_CHOICES,
                 str_control_expression=STR_CONTROL_EXPRESSION,
                 date_control_expression=DATE_CONTROL_EXPRESSION,
                 int_control_expression=INT_CONTROL_EXPRESSION,
                 players_dao=PlayersDataBase,
                 tournaments_dao=TournamentsDataBase)

browser.main_menu_control()
