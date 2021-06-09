#! /usr/bin/env python3
# coding: utf-8

import tinydb
from abc import ABC

DEFAULT_NUMBER_OF_TURNS = 4

TYPE_OF_TIME_CONTROLLER = {"bullet": range(1, 3), "blitz": range(3, 6), "fast_chess": range(10, 61)}

TOURNAMENTS_STATES = ["In progress", "Completed", "aborted"]

DAO_PATH = "data/chess_database.json"

DAO_OBJECT = tinydb.TinyDB(DAO_PATH)

list_of_ongoing_tournaments = []


class Player:
    """class which represent a player"""

    def __init__(self, last_name, first_name, date_of_birth, gender, rank):
        """Player constructor"""

        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.rank = rank

    def __eq__(self, other):
        """Function that allows to check if a player already exists"""

        if not isinstance(other, Player):
            return False
        if self.last_name.upper() != other.last_name.upper():
            return False
        if self.first_name.upper() != other.first_name.upper():
            return False
        if self.date_of_birth != other.date_of_birth:
            return False
        else:
            return True


class Match:
    """class which represent a match"""
    def __init__(self, player_1, player_2):
        """Match constructor"""
        self.players = [player_1, player_2]
        self.results = "Not set"


class Tournament:
    """class which represent a tournament"""

    def __init__(self, name, place, date,
                 round_list, players_index_list, time_controller,
                 number_of_turns=DEFAULT_NUMBER_OF_TURNS, actual_tour_number=0, state=TOURNAMENTS_STATES[0]):
        """Tournament constructor"""

        self.name = name
        self.place = place
        self.date = date  # list of days
        self.number_of_turns = number_of_turns
        self.round_list = round_list
        self.players_index_list = players_index_list
        self.time_controller = time_controller
        self.actual_tour_number = actual_tour_number
        self.state = state

    def swiss_system(self):
        """Function used to create all players pair for match"""


class DAO(ABC):
    """Abstract DAO Class"""

    def __init__(self, dao=DAO_OBJECT):
        """DOA constructor"""
        self.dao = dao


class PlayersDataBase(DAO):
    """Class which represent the players database of the club"""

    def __init__(self):
        """DataBase constructor"""

        DAO.__init__(self)
        self.players_list = []
        self.players_table = self.dao.table("players")

    def load_dao(self):
        """Function which load players data from the database"""

        new_players_list = []
        serialized_players_list = self.players_table.all()

        for serialized_player in serialized_players_list:
            new_players_list.append(Player(serialized_player["last_name"],
                                           serialized_player["first_name"],
                                           serialized_player["date_of_birth"],
                                           serialized_player["gender"],
                                           serialized_player["rank"]))
        self.players_list = new_players_list

    def save_dao(self):
        """Function which save the data into the database"""

        serialized_players_list = []
        for player in self.players_list:
            serialized_player = {"last_name": player.last_name,
                                 "first_name": player.first_name,
                                 "date_of_birth": player.date_of_birth,
                                 "gender": player.gender,
                                 "rank": player.rank}

            serialized_players_list.append(serialized_player)

        self.players_table.truncate()
        self.players_table.insert_multiple(serialized_players_list)

    def players_exists(self, new_player):
        """function that return True if the player 1 is already in the database"""

        for player in self.players_list:
            if new_player == player:
                return True
        return False


class TournamentsDataBase(DAO):
    """Class which represent the tournaments database of the club"""

    def __init__(self):
        """DataBase constructor"""

        DAO.__init__(self)
        self.tournaments_list = []
        self.tournaments_table = self.dao.table("tournaments")

    def load_dao(self):
        """Function which load tournaments data from the database"""

        new_tournaments_list = []
        serialized_tournaments_list = self.tournaments_table.all()

        for serialized_tournament in serialized_tournaments_list:
            new_tournaments_list.append(Tournament(serialized_tournament["name"],
                                                   serialized_tournament["place"],
                                                   serialized_tournament["date"],
                                                   serialized_tournament["round_list"],
                                                   serialized_tournament["players_index_list"],
                                                   serialized_tournament["time_controller"],
                                                   serialized_tournament["number_of_turns"],
                                                   serialized_tournament["actual_tour_number"],
                                                   serialized_tournament["state"]))

        return new_tournaments_list

    def save_dao(self):
        """Function which save the data into the database"""

        serialized_tournaments_list = []
        for tournament in self.tournaments_list:
            serialized_tournament = {"name": tournament.name,
                                     "place": tournament.place,
                                     "date": tournament.date,
                                     "round_list": tournament.round_list,
                                     "players_index_list": tournament.players_index_list,
                                     "time_controller": tournament.time_controller,
                                     "number_of_turns": tournament.number_of_turns,
                                     "actual_tour_number": tournament.actual_tour_number,
                                     "state": tournament.state}

            serialized_tournaments_list.append(serialized_tournament)

        self.tournaments_table.truncate()
        self.tournaments_table.insert_multiple(serialized_tournaments_list)
