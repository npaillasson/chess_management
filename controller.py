#! /usr/bin/env python3
# coding: utf-8

import os
import time
from datetime import datetime
import re
from view import ChoiceMenu, FieldMenu, Sign, ValidationMenu
from menu import MAIN_MENU_CHOICES, FIELD_MESSAGE, CORRECTION_MENU_CHOICES,\
    PROPOSAL_MENU_MESSAGE, players_formatting, tournament_formatting
from model import Player, PlayersDAO, Tournament, TournamentsDAO, Match, DAO_PATH, DEFAULT_NUMBER_OF_TURNS
import menu

# regex that allows to check if the field contains only lettres or space or "-".
STR_CONTROL_EXPRESSION = re.compile(r"^[A-Za-z- 'éèàêöç]+$")

# regex which allows to check if the field contains a date in right format
DATE_FORMAT = "%d/%m/%Y"

# regex that allows to check if a field is only composed by number
INT_CONTROL_EXPRESSION = re.compile(r"^[0-9]+$")

STR_INT_CONTROL_EXPRESSION = re.compile(r"^[A-Za-z0-9 'éèàêöç!.;:,/]+$")

stop_function = "quit"

# list of adapted data_controllers
# Field which have to contains only str, no int
str_controller = ["last_name", "first_name"]
# Field that can contain str and int, can not be empty.
str_int_controller =["tournament_name", "tournament_place", "tournament_comments"]
# Field which contains a date
date_controller = ["date_of_birth", "tournament_date", "end_date"]
# Field  which contains only int, no str
int_controller = ["rank", "number_of_turn"]
# Data already checked as proposal list
no_controller = ["gender", "selected_player", "time_control", "participating_players", "other_date_request"]


class Browse:
    """class which manage the navigation of the user according to his input"""

    def __init__(self, main_menu_choice,
                 correction_menu_choice,
                 str_control_expression,
                 str_int_control_expression,
                 date_control_expression,
                 int_control_expression,
                 players_dao,
                 tournaments_dao):

        # menus choice
        self.main_menu_choice = main_menu_choice
        self.correction_menu_choice = correction_menu_choice

        # regular expression
        self.str_control_expression = str_control_expression
        self.str_int_control_expression = str_int_control_expression
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
            return self.player_creator_control()
        elif choice == 1:  # launch the tournaments creation menu
            if len(self.players_dao.players_list) < 8:
                self.sign.printing_sign(menu.not_enough_players)
                return self.main_menu_control()
            return self.tournament_creator_control()
        elif choice == 2:  # launch the menu for editing player's scores #A continuer!
            return self.score_edit_controller()
        elif choice ==3:
            return self.select_tournaments()

    # function that manage the players creation feature
    def player_creator_control(self):
        """method which control the user input in the player creation menu"""

        while True:
            player_information = {}
            last_name = self.set_menu("last_name")
            if last_name == stop_function:
                break
            player_information["last_name"] = last_name.upper()
            first_name = self.set_menu("first_name")
            if last_name == stop_function:
                break
            player_information["first_name"] = first_name.capitalize()
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
                break
            elif choice == 1:
                continue
            else:
                break
        return self.main_menu_control()

    def tournament_creator_control(self):
        """method which control the user input in the player creation menu"""
        while True:
            tournament_information = {}
            tournament_name = self.set_menu("tournament_name")
            if tournament_name == stop_function:
                break
            tournament_information["tournament_name"] = tournament_name
            tournament_place = self.set_menu("tournament_place")
            if tournament_place == stop_function:
                break
            tournament_information["tournament_place"] = tournament_place
            tournament_date = self.set_menu("tournament_date", date_not_passed=False)
            tournament_information["tournament_date"] = tournament_date
            other_date_request = self.set_menu("other_date_request", index=True)
            if other_date_request == 0:
                end_date = self.set_menu("end_date", date_not_passed=False,
                                         greater_than=tournament_information["tournament_date"])
            else:
                end_date = tournament_date
            tournament_information["end_date"] = end_date
            number_of_turn = self.set_menu("number_of_turn", empty_field_permitted=True)
            if number_of_turn == "":
                tournament_information["number_of_turn"] = DEFAULT_NUMBER_OF_TURNS
            else:
                tournament_information["number_of_turn"] = number_of_turn
            players_index_list, players_object_list = self.add_players_in_tournament()
            tournament_information["players_index_list"] = players_index_list
            tournament_information["players_object_list"] = players_object_list
            time_control = self.set_menu("time_control")
            tournament_information["time_control"] = time_control
            tournament_comments = self.set_menu("tournament_comments", empty_field_permitted=True)
            tournament_information["tournament_comments"] = tournament_comments

            choice = self.validation_menu.printing_correction_menu(tournament_formatting(tournament_information))
            if choice == 0:
                print("OK")
                self.add_tournament_in_dao(tournament_information)
                break
            elif choice == 1:
                continue
            else:
                break
        return self.main_menu_control()

    def score_edit_controller(self):
        """method which control the user input in the menu for editing player's scores"""
        displayed_list = self.display_player_list(self.players_dao.players_list)
        selected_player_index = self.choice_menu.printing_menu_index(displayed_list)

        # if the user choose the quit option (which is the last one on the list
        if selected_player_index == len(displayed_list) - 1:
            return self.main_menu_control()
        else:
            selected_player = self.players_dao.players_list[selected_player_index]
            self.sign.printing_sign(selected_player)
            new_rank = self.set_menu("rank")
            selected_player.rank = new_rank
            # we save the new score in the dao
            self.players_dao.save_dao()
            return self.main_menu_control()


    def select_tournaments(self):

        displayed_list, object_list = self.display_tournament_list(object_list=True, active_only=True)
        selected_tournament_index = self.choice_menu.printing_menu_index(displayed_list)

        # if the user choose the quit option (which is the last one on the list)
        if selected_tournament_index == len(displayed_list) - 1:
            return self.main_menu_control()

        else:
            return self.tournaments_management(object_list[selected_tournament_index])


    def tournaments_management(self, tournament):

        tournament.swiss_system() #ici on affiche les joueurs
        while tournament.actual_tour_number < tournament.number_of_turns + 1:
            displayed_list, object_list = self.display_match_list(tournament.round_list[tournament.actual_tour_number])
            selected_match_index = self.validation_menu.printing_proposal_menu(PROPOSAL_MENU_MESSAGE["set_match"],
                                                                               validation_choices=displayed_list)

            if selected_match_index == len(displayed_list) - 1:
                return self.main_menu_control()

            else: # ici on affiche une premiere page d'entrée pour le joueur 1 puis une seconde pour le joueur 2
                while True:
                    self.sign.printing_sign(object_list[selected_match_index].players[0])
                    self.field_menu.printing_field("score_request")
                    #A FINIR, CONTROLLER ET AJOUTER LE SCORE POUR LA SUITE DE LA RONDE SUISSE

    def add_players_in_tournament(self):
        """method which allows to add 8 players in a tournament"""

        # On a deux liste, une avec la représentation des joueurs en str
        # pour le menu et l'autre contenant les objets joueurs pour récuperer
        # l'index reel dans la liste des joueur de la base de données
        displayed_list, players_list_object = self.display_player_list(self.players_dao.players_list, object_list=True)
        participating_players_index_list = []
        participating_players_object_list = []

        while len(participating_players_index_list) < 8:
            selected_player_index = self.choice_menu.printing_menu_index(displayed_list)
            if selected_player_index == len(displayed_list) - 1:
                return self.main_menu_control()
            else:
                player_object = players_list_object[selected_player_index]
                del displayed_list[selected_player_index]
                del players_list_object[selected_player_index]
                participating_players_index_list.append(self.players_dao.players_list.index(player_object))
                participating_players_object_list.append(player_object)

        return participating_players_index_list, participating_players_object_list

    def display_player_list(self, player_list, object_list=False):
        displayed_list = []
        players_list_object = []
        for player in player_list:
            displayed_list.append(str(player))
            players_list_object.append(player)
        displayed_list.append(stop_function)  # we add the quit choice
        if object_list:
            return displayed_list, players_list_object
        else:
            return displayed_list

    def display_tournament_list(self, object_list=False, all_tournaments=True, active_only=False):

        if active_only:
            all_tournaments = False

        displayed_list = []
        tournament_list_object = []

        if all_tournaments:
            tournament_list = self.tournaments_dao.tournaments_list + self.tournaments_dao.active_tournaments_list
        else:
            tournament_list = self.tournaments_dao.active_tournaments_list

        for tournament in tournament_list:
            displayed_list.append(str(tournament))
            tournament_list_object.append(tournament)
        displayed_list.append(stop_function)  # we add the quit choice
        if object_list:
            return displayed_list, tournament_list_object
        else:
            return displayed_list

    @staticmethod
    def display_match_list(round_list):

        displayed_list = []
        match_list_object = []
        for match in round_list:
            displayed_list.append(str(match))
            match_list_object.append(match)
            displayed_list.append(stop_function)
        return displayed_list, match_list_object

    def data_controller(self, data_name, empty_field_permitted=False):
        """Method which control user's inputs conformity"""

        while True:
            data = self.field_menu.printing_field(FIELD_MESSAGE[data_name][0])
            if data == stop_function:
                return data
            elif data_name in str_controller:
                if self.str_control_expression.match(data) is not None:
                    return data.strip()
                else:
                    self.sign.printing_sign(FIELD_MESSAGE[data_name][1])
            elif data_name in str_int_controller:
                if self.str_int_control_expression.match(data) is not None:
                    return data.strip()
                elif data == "" and empty_field_permitted:
                    return data
            elif data_name in int_controller:
                if self.int_control_expression.match(data) is not None:
                    return data
                elif not data and empty_field_permitted:
                    return ""
                else:
                    self.sign.printing_sign(FIELD_MESSAGE[data_name][1])

    # which checks if the date exists and if it has already been exceeded.
    def date_control(self, data_name, date_not_passed=True, greater_than=None):
        """Function that check the date conformity"""

        while True:
            data = self.field_menu.printing_field(FIELD_MESSAGE[data_name][0])
            try:
                time_object = time.strptime(data, DATE_FORMAT)
            except ValueError:
                self.sign.printing_sign(FIELD_MESSAGE[data_name][1])
                continue
            if date_not_passed:
                if time_object <= time.localtime():
                    return data
                else:
                    self.sign.printing_sign(FIELD_MESSAGE[data_name][1])
            if not date_not_passed and not greater_than:
                return data
            if not date_not_passed and greater_than:
                compared_time_object = time.strptime(greater_than, DATE_FORMAT)
                if time_object > compared_time_object:
                    return data
                else:
                    self.sign.printing_sign(FIELD_MESSAGE[data_name][1])

    def set_menu(self, data_name, index=None, empty_field_permitted=False, date_not_passed=True, greater_than=None):
        """Method which allows to set the menu and return the value"""

        if data_name in no_controller:
            value = self.validation_menu.printing_proposal_menu(PROPOSAL_MENU_MESSAGE[data_name][0],
                                                                PROPOSAL_MENU_MESSAGE[data_name][1],
                                                                index=index)
            return value
        elif data_name in date_controller:
            value = self.date_control(data_name, date_not_passed=date_not_passed, greater_than=greater_than)
            return value
        else:
            if empty_field_permitted:
                value = self.data_controller(data_name, empty_field_permitted=True)
                return value
            else:
                value = self.data_controller(data_name)
                return value

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

        return self.main_menu_control()

    def add_tournament_in_dao(self, tournament_information):
        """function which add a tournament into the database"""

        new_tournament = Tournament(tournament_name=tournament_information["tournament_name"],
                                    tournament_place=tournament_information["tournament_place"],
                                    tournament_date=tournament_information["tournament_date"],
                                    end_date=tournament_information["end_date"],
                                    players_index_list=tournament_information["players_index_list"],
                                    players_object_list=tournament_information["players_object_list"],
                                    number_of_turns=tournament_information["number_of_turn"],
                                    time_controller=tournament_information["time_control"],
                                    tournament_comments=tournament_information["tournament_comments"],
                                    round_list=None,)

        self.tournaments_dao.tournaments_list.append(new_tournament)
        self.tournaments_dao.save_dao()

        return self.main_menu_control()


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
                 str_int_control_expression=STR_INT_CONTROL_EXPRESSION,
                 date_control_expression=DATE_FORMAT,
                 int_control_expression=INT_CONTROL_EXPRESSION,
                 players_dao=PlayersDAO,
                 tournaments_dao=TournamentsDAO)

browser.players_dao.load_dao()
browser.tournaments_dao.load_dao(browser.players_dao.players_list)
print("inactif", browser.tournaments_dao.tournaments_list)
print("actif", browser.tournaments_dao.active_tournaments_list)
browser.main_menu_control()
