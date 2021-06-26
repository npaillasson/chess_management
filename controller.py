#! /usr/bin/env python3
# coding: utf-8

"""Controller module"""

import time
import sys
import re

from operator import attrgetter

import model
from view import ChoiceMenu, FieldMenu, Sign, ValidationMenu
import menu

# regex that allows to check if the field contains only lettres or space or "-".
STR_CONTROL_EXPRESSION = re.compile(r"^[A-Za-z- 'éèàêöç]+$")

# regex which allows to check if the field contains a date in right format
DATE_FORMAT = "%d/%m/%Y"

# regex that allows to check if a field is only composed by number
INT_CONTROL_EXPRESSION = re.compile(r"^[0-9]+$")

STR_INT_CONTROL_EXPRESSION = re.compile(r"^[A-Za-z0-9 'éèàêöç!.;:,/_-]+$")

stop_function = menu.STOP_FUNCTION_KEY_WORD

# list of adapted data_controllers
# Field which have to contains only str, no int
str_controller = ["last_name", "first_name"]
# Field that can contain str and int, can not be empty.
str_int_controller = ["tournament_name", "tournament_place", "tournament_comments"]
# Field which contains a date
date_controller = ["date_of_birth", "tournament_date", "end_date"]
# Field  which contains only int, no str
int_controller = ["rank", "number_of_turn"]
# Data already checked as proposal list
no_controller = ["gender", "selected_player", "time_control", "participating_players", "other_date_request",
                 "score_request", "load_new_database", "launch_tournament"]


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
        """Browse constructor"""

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
        self.tournaments_dao = tournaments_dao(self.players_dao)

    def main_menu_control(self):
        """main menu controller function"""
        choice = self.choice_menu.printing_menu_index(self.main_menu_choice)
        if choice == 0:
            return self.player_creator_control()
        elif choice == 1:
            if len(self.players_dao.players_list) < 8:
                self.sign.printing_sign(menu.not_enough_players)
                return self.main_menu_control()
            return self.tournament_creator_control()
        elif choice == 2:
            return self.score_edit_controller()
        elif choice == 3:
            return self.select_tournaments()
        elif choice == 4:
            return self.report_main_menu()
        else:
            self.tournaments_dao.save_dao()
            sys.exit(0)

    def player_creator_control(self):
        """method which control the user input in the player creation menu"""

        while True:
            player_information = {}
            last_name = self.set_menu("last_name")
            if last_name == stop_function:
                break
            player_information["last_name"] = last_name.upper()
            first_name = self.set_menu("first_name")
            if first_name == stop_function:
                break
            player_information["first_name"] = first_name.capitalize()
            player_information["date_of_birth"] = self.set_menu("date_of_birth")
            if player_information["date_of_birth"] == stop_function:
                break
            player_information["gender"] = self.set_menu("gender")
            player_information["rank"] = self.set_menu("rank")
            if player_information["rank"] == stop_function:
                break
            choice = self.validation_menu.\
                printing_correction_menu(menu.players_formatting(player_information))
            if choice == 0:
                self.add_player_in_dao(player_information)
                break
            elif choice == 1:
                continue
            else:
                break
        return self.main_menu_control()

    def tournament_creator_control(self):
        """Method which control the user input in the player creation menu"""

        while True:
            tournament_information = {"tournament_name": self.set_menu("tournament_name")}
            if tournament_information["tournament_name"] == stop_function:
                break
            tournament_information["tournament_place"] = self.set_menu("tournament_place")
            if tournament_information["tournament_place"] == stop_function:
                break
            tournament_information["tournament_date"] = self.set_menu("tournament_date",
                                                                      date_not_passed=False)
            if tournament_information["tournament_date"] == stop_function:
                break
            other_date_request = self.set_menu("other_date_request", index=True)
            if other_date_request == 1:
                tournament_information["end_date"] = self.set_menu("end_date", date_not_passed=False,
                                                                   greater_than=tournament_information
                                                                   ["tournament_date"])
            else:
                tournament_information["end_date"] = tournament_information["tournament_date"]
            tournament_information["number_of_turn"] = self.set_menu("number_of_turn", empty_field_permitted=True)
            if tournament_information["number_of_turn"] == "":
                tournament_information["number_of_turn"] = model.DEFAULT_NUMBER_OF_TURNS
            players_index_list, players_object_list = self.add_players_in_tournament()
            tournament_information["players_index_list"] = players_index_list
            tournament_information["players_object_list"] = players_object_list
            tournament_information["time_control"] = self.set_menu("time_control")
            tournament_information["tournament_comments"] = self.set_menu("tournament_comments",
                                                                          empty_field_permitted=True)
            choice = self.validation_menu.printing_correction_menu(menu.tournament_formatting(tournament_information))
            if choice == 0:
                self.add_tournament_in_dao(tournament_information)
                self.tournaments_dao.tournaments_distribution(self.tournaments_dao.tournaments_list)
                break
            elif choice == 1:
                continue
            else:
                break
        return self.main_menu_control()

    def score_edit_controller(self):
        """Method which control the user input in the menu for editing player's scores"""

        displayed_list = self.display_player_list(self.players_dao.players_list)
        selected_player_index = self.choice_menu.printing_menu_index(displayed_list)

        # if the user chooses the quit option (which is the last one in the list)
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
        """Method to select an active tournament before manage it"""

        displayed_list, object_list = self.display_tournament_list(object_list=True, active_only=True)
        selected_tournament_index = self.choice_menu.printing_menu_index(displayed_list)

        # if the user choose the quit option (which is the last one on the list)
        if selected_tournament_index == len(displayed_list) - 1:
            return self.main_menu_control()

        else:
            return self.tournaments_management(object_list[selected_tournament_index])

    def tournaments_management(self, tournament):
        """Method that allows to manage the progress of a tournament and enter the results of a match"""

        if tournament.actual_tour_number != len(tournament.round_list):

            return self.start_tour(tournament)
        self.sign.printing_sign(menu.actual_turn_formating(tournament))
        while tournament.actual_tour_number <= tournament.number_of_turns:
            displayed_list, match_object_list = self.display_matches_list(tournament.round_list
                                                                          [tournament.actual_tour_number - 1])
            selected_match_index = self.validation_menu.printing_proposal_menu(menu.PROPOSAL_MENU_MESSAGE["set_match"],
                                                                               validation_choices=displayed_list)

            if selected_match_index == len(displayed_list) - 1:
                return self.main_menu_control()

            elif selected_match_index == len(displayed_list) - 2:
                return self.aborted_tournament(tournament)

            elif selected_match_index == len(displayed_list) - 3:
                return self.add_comments_to_tournament(tournament)

            else:
                match = match_object_list[selected_match_index]
                return self.entering_matches_results(match, tournament, match_object_list)

    def entering_matches_results(self, match, tournament, match_object_list):
        """method to enter the results of matches"""

        while True:

            player_1 = match.players_object_list[0]
            player_1_index = tournament.players_list.index(player_1)
            player_2 = match.players_object_list[1]
            player_2_index = tournament.players_list.index(player_2)
            players_str_list = [str(player_1), str(player_2), model.DRAW_KEY_WORD]
            players_index_list = [player_1_index, player_2_index, model.DRAW_INDEX]
            # winner is an int number
            winner = self.validation_menu.printing_proposal_menu(
                menu.PROPOSAL_MENU_MESSAGE["result_match_request"][0], players_str_list)

            choice = self.validation_menu.printing_correction_menu(
                menu.match_formatting(player_1, player_2,
                                      winner_player=players_str_list[winner]))

            if choice == 0:
                match.winner_absolute_index = players_index_list[winner]
                match.winner_relative_index = winner

                if match.winner_absolute_index == model.DRAW_INDEX:
                    tournament.players_points[player_1_index] += model.NULL_POINT
                    tournament.players_points[player_2_index] += model.NULL_POINT
                else:
                    tournament.players_points[match.winner_absolute_index] += model.WINNER_POINT
                match.end_time = time.strftime(model.MATCH_DATE_FORMAT)
                self.tournaments_dao.save_dao()
                return self.tours_management(tournament, match_object_list)
            if choice == 1:
                continue
            else:
                return self.select_tournaments()

    def start_tour(self, tournament):
        """Method to launch a new tour"""

        choice = self.set_menu("launch_tournament", index=True)

        if choice == 0:
            return self.main_menu_control()
        else:
            tournament.swiss_system()
            self.tournaments_dao.save_dao()
            return self.tournaments_management(tournament)

    def tours_management(self, tournament, match_object_list):
        """Method to manage the progress of a round and move to the next round if necessary"""

        actual_match_list = match_object_list
        remaining_match = 0
        for match in actual_match_list:
            if match.winner_absolute_index == model.WINNER_NOT_SET:
                remaining_match += 1
        if remaining_match == 0:
            tournament.actual_tour_number += 1
            if tournament.actual_tour_number > tournament.number_of_turns:
                tournament.state = model.TOURNAMENTS_STATES[2]
                self.sign.printing_sign(menu.end_of_tournament)
                self.add_tournament_points_to_player(tournament)
                self.tournaments_dao.save_dao()
                self.tournaments_dao.tournaments_distribution(self.tournaments_dao.tournaments_list)
                return self.printing_tournament_ranking(tournament, to_main_menu=True)
            else:
                return self.tournaments_management(tournament)
        else:
            return self.tournaments_management(tournament)

    def aborted_tournament(self, tournament):
        """Method which manage the drop out af tournament"""
        choice = self.validation_menu.printing_proposal_menu(menu.PROPOSAL_MENU_MESSAGE["abort_tournament"][0],
                                                             menu.PROPOSAL_MENU_MESSAGE["abort_tournament"][1],
                                                             index=True)
        if choice == 1:
            tournament.state = model.TOURNAMENTS_STATES[1]
            self.tournaments_dao.save_dao()
            self.tournaments_dao.tournaments_distribution(self.tournaments_dao.tournaments_list)
            return self.main_menu_control()
        else:
            return self.tournaments_management(tournament)

    @staticmethod
    def add_tournament_points_to_player(tournament):
        """Method which add tournament point to the players at the end of the tournament"""
        for index, player in enumerate(tournament.players_list):
            player.rank += tournament.players_points[index]

    def add_players_in_tournament(self):
        """method which allows to add 8 players in a tournament"""

        # We have two lists, one with the representation of the players in str
        # for the menu and the other one containing the player objects to get
        # the real index in the list of players in the database
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

    @staticmethod
    def display_player_list(player_list, object_list=False):
        """Method to display players list"""
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
        """Method to display tournaments list"""

        if active_only:
            all_tournaments = False

        displayed_list = []
        tournament_list_object = []

        if all_tournaments:
            tournament_list = self.tournaments_dao.tournaments_list
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
    def display_matches_list(round_list):
        """Method to display matches list"""

        displayed_list = []
        match_list_object = []
        for match in round_list:
            if match.winner_absolute_index == model.WINNER_NOT_SET:
                displayed_list.append(match.display_match_for_choice())
                match_list_object.append(match)
        displayed_list.append(menu.add_comments)
        displayed_list.append(menu.abort_tournament)
        displayed_list.append(stop_function)
        return displayed_list, match_list_object

    def add_comments_to_tournament(self, tournament):
        """Method to add a comment into the tournament"""

        new_comment = self.set_menu("tournament_comments")
        if new_comment == stop_function:
            return self.tournaments_management(tournament)
        tournament.tournament_comments = tournament.tournament_comments + "|{}|".format(new_comment)
        self.tournaments_dao.save_dao()
        return self.tournaments_management(tournament)

    def data_controller(self, data_name, empty_field_permitted=False):
        """Method which control user's inputs conformity"""

        while True:
            data = self.field_menu.printing_field(menu.FIELD_MESSAGE[data_name][0])
            if data == stop_function:
                return data
            elif data_name in str_controller:
                if self.str_control_expression.match(data) is not None:
                    return data.strip()
                else:
                    self.sign.printing_sign(menu.FIELD_MESSAGE[data_name][1])
            elif data_name in str_int_controller:
                if self.str_int_control_expression.match(data) is not None:
                    return data.strip()
                elif data == "" and empty_field_permitted:
                    return data
            elif data_name in int_controller:
                if self.int_control_expression.match(data) is not None:
                    return int(data)
                elif not data and empty_field_permitted:
                    return ""
                else:
                    self.sign.printing_sign(menu.FIELD_MESSAGE[data_name][1])

    def date_control(self, data_name, date_not_passed=True, greater_than=None):
        """Method that check the date conformity"""

        while True:
            data = self.field_menu.printing_field(menu.FIELD_MESSAGE[data_name][0])
            if data == stop_function:
                return data
            try:
                time_object = time.strptime(data, DATE_FORMAT)
            except ValueError:
                self.sign.printing_sign(menu.FIELD_MESSAGE[data_name][1])
                continue
            if date_not_passed:
                if time_object <= time.localtime():
                    return data
                else:
                    self.sign.printing_sign(menu.FIELD_MESSAGE[data_name][1])
            if not date_not_passed and not greater_than:
                return data
            if not date_not_passed and greater_than:
                compared_time_object = time.strptime(greater_than, DATE_FORMAT)
                if time_object > compared_time_object:
                    return data
                else:
                    self.sign.printing_sign(menu.FIELD_MESSAGE[data_name][1])

    def set_menu(self, data_name, index=None, empty_field_permitted=False, date_not_passed=True, greater_than=None):
        """Method which allows to set the menu and return the value"""

        if data_name in no_controller:
            value = self.validation_menu.printing_proposal_menu(menu.PROPOSAL_MENU_MESSAGE[data_name][0],
                                                                menu.PROPOSAL_MENU_MESSAGE[data_name][1],
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
        """Method which add a player into the database"""

        new_player = model.Player(player_information["last_name"],
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
        """Method which add a tournament into the database"""

        new_tournament = model.Tournament(tournament_name=tournament_information["tournament_name"],
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
        self.tournaments_dao.load_dao()

        return self.main_menu_control()

    def report_main_menu(self):
        """Method that manages the reports main menu"""

        choice = self.choice_menu.printing_menu_index(menu.REPORTS_MAIN_MENU)
        if choice == 0:
            return self.report_sub_menu(players_list=self.players_dao.players_list)
        elif choice == 1:
            return self.printing_tournament_report()
        elif choice == 2:
            return self.select_tournament_for_report(players_report=True)
        elif choice == 3:
            return self.select_tournament_for_report(tours_report=True)
        else:
            return self.main_menu_control()

    def report_sub_menu(self, players_list=None, with_tournament_ranking=False, tournament=None):
        """Method that manages the reports sub menu"""
        if with_tournament_ranking:
            choice = self.choice_menu.printing_menu_index(menu.REPORTS_SUB_MENU_TOURNAMENT)
        else:
            choice = self.choice_menu.printing_menu_index(menu.REPORTS_SUB_MENU_PLAYER)
        if choice == 0:
            return self.printing_players_report(players_list)
        elif choice == 1:
            return self.printing_players_report(players_list, alpha=False)
        elif with_tournament_ranking and choice == 2:
            return self.printing_tournament_ranking(tournament=tournament)
        else:
            return self.main_menu_control()

    def printing_players_report(self, players_list, alpha=True):
        """Method that display players reports"""

        if alpha:
            sorted_list = sorted(players_list, key=attrgetter("last_name", "first_name"))
        else:
            sorted_list = sorted(players_list, key=attrgetter("rank", "last_name", "first_name"), reverse=True)
        for index, player in enumerate(sorted_list):
            sorted_list[index] = str(player)
        display_chain = menu.quit_report + "\n".join(sorted_list) + "\n:"

        while True:
            quit_report = self.field_menu.printing_field(display_chain)
            if quit_report == stop_function:
                break
        return self.report_main_menu()

    def printing_tournament_report(self):
        """Method that display tournaments reports"""

        display_list = []
        display_chain = ""
        for tournament in self.tournaments_dao.tournaments_list:
            display_list.append(menu.tournament_report_formatting(tournament))
            display_chain = menu.quit_report + "\n".join(display_list) + "\n:"
        while True:
            quit_report = self.field_menu.printing_field(display_chain)
            if quit_report == stop_function:
                break
        return self.report_main_menu()

    def printing_tours_report(self, tournament):
        """Method that display tours reports"""

        display_list = []
        display_chain = ""
        for index, tour in enumerate(tournament.round_list):
            display_list.append(menu.tour_report_formatting(tour, index + 1))
            display_chain = menu.quit_report + "\n".join(display_list) + "\n:"
        while True:
            quit_report = self.field_menu.printing_field(display_chain)
            if quit_report == stop_function:
                break
        return self.report_main_menu()

    def select_tournament_for_report(self, players_report=False, tours_report=False):
        """Method that manage tournaments selection before display reports"""
        display_list, tournament_objects_list = self.display_tournament_list(object_list=True)
        tournament_index = self.choice_menu.printing_menu_index(display_list)
        if tournament_index == len(display_list) - 1:
            return self.report_main_menu()
        else:
            tournament = tournament_objects_list[tournament_index]
            if players_report:
                return self.report_sub_menu(tournament=tournament, players_list=tournament.players_list,
                                            with_tournament_ranking=True)
            elif tours_report:
                return self.printing_tours_report(tournament)

    def printing_tournament_ranking(self, tournament, to_main_menu=False):
        """Method that displays the tournament ranking"""
        sorted_list = []
        for index, points_amount in enumerate(tournament.players_points):
            sorted_list.append((tournament.players_list[index].last_name + " "
                                + tournament.players_list[index].first_name, points_amount))
        sorted_list = sorted(sorted_list, key=lambda column: column[1], reverse=True)
        display_chain = menu.quit_report + menu.tournament_rank_formatting(sorted_list)
        while True:
            quit_report = self.field_menu.printing_field(display_chain)
            if quit_report == stop_function:
                break
        if to_main_menu:
            return self.main_menu_control()
        else:
            return self.report_main_menu()


def launch_program():
    """function that launch the application"""

    browser = Browse(main_menu_choice=menu.MAIN_MENU_CHOICES,
                     correction_menu_choice=menu.CORRECTION_MENU_CHOICES,
                     str_control_expression=STR_CONTROL_EXPRESSION,
                     str_int_control_expression=STR_INT_CONTROL_EXPRESSION,
                     date_control_expression=DATE_FORMAT,
                     int_control_expression=INT_CONTROL_EXPRESSION,
                     players_dao=model.PlayersDAO,
                     tournaments_dao=model.TournamentsDAO)

    browser.players_dao.load_dao()
    browser.tournaments_dao.load_dao()
    browser.main_menu_control()
