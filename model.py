#! /usr/bin/env python3
# coding: utf-8

import os
import tinydb

DEFAULT_NUMBER_OF_TURNS = 4

TYPE_OF_TIME_CONTROLLER = {"bullet": range(1, 3), "blitz": range(3, 6), "fast_chess": range(10, 61)}

TOURNAMENTS_STATES = ["In progress", "Completed", "aborted"]

list_of_ongoing_tournaments = []


class Player:
    """class which represent a player"""

    def __init__(self, last_name, first_name, date_of_birth, gender, rank):
        """Player constructor"""

        self._last_name = last_name
        self._first_name = first_name
        self._date_of_birth = date_of_birth
        self._gender = gender
        self.rank = rank


class Match:
    """class which represent a match"""
    def __init__(self, player_1, player_2):
        """Match constructor"""
        self.players = [player_1, player_2]
        self.results = "Not set"


class Round:
    """class which represent a round"""
    def __init__(self, ):
        """"""


class Tournament:
    """class which represent a tournament"""

    def __init__(self, name, place, date,
                 round_list, players_index_list, time_controller,
                 number_of_turns=DEFAULT_NUMBER_OF_TURNS):
        """Tournament constructor"""

        self.name = name
        self.place = place
        self.date = date  # list of days
        self.number_of_turns = number_of_turns
        self.round_list = round_list
        self.players_index_list = players_index_list
        self.time_controller = time_controller
        self.actual_tour_number = 0
        self.state = TOURNAMENTS_STATES[0]

    def swiss_system(self):
        """Function used to create all players pair for match"""


class PlayersDataBase:
    """Class which represent the players database of the club"""

    def __init__(self):
        """DataBase constructor"""

        self.players_list = []

    def load_players_database(self, database_file):
        """Function which load players data from the database"""

    def save_into_players_database(self, database_file):
        """Function which save the data into the database"""


class TournamentsDataBase:
    pass
