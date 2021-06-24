#! /usr/bin/env python3
# coding: utf-8

"""model module, contains the next class: Player, Match, Tournament, DAO, Player_DAO, Tournament_DAO"""

import os
from operator import attrgetter, itemgetter
import tinydb
from abc import ABC

import controller
import menu
import time
import datetime

DEFAULT_NUMBER_OF_TURNS = 4

NUMBER_OF_MATCH_PER_TOUR = 4

NUMBER_OF_PLAYER = 8

TOURNAMENTS_STATES = menu.TOURNAMENT_STATE

if not os.path.exists("data/"):
    os.mkdir("data/")

DAO_PATH = "data/chess_database.json"

DAO_OBJECT = tinydb.TinyDB(DAO_PATH)

list_of_ongoing_tournaments = []

DRAW_KEY_WORD = menu.DRAW_MATCH_KEY_WORD

DRAW_INDEX = -1

WINNER_POINT = 1

NULL_POINT = 0.5

MATCH_DATE_FORMAT = "le {} à %H:%M".format(controller.DATE_FORMAT)


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

    def __str__(self):
        """Function that defines how a player is displayed"""
        return "{} {} né(e) le {} : {} pts".format(self.last_name, self.first_name, self.date_of_birth, self.rank)

    def __repr__(self):
        """Function that defines how a player object is represented"""
        return str(self)


class Match:
    """class which represent a match"""
    def __init__(self, players_object_list, players_index_list, winner_absolute_index=None,
                 winner_relative_index=None, start_time=None, end_time=None):
        """Match constructor"""
        if not start_time:
            self.start_time = time.strftime(MATCH_DATE_FORMAT)

        self.players_object_list = players_object_list
        self.players_index_list = players_index_list
        self.player_1_information =\
            self.players_object_list[0].last_name + " " + self.players_object_list[0].first_name
        self.player_2_information = \
            self.players_object_list[1].last_name + " " + self.players_object_list[1].first_name
        self.winner_absolute_index = winner_absolute_index
        self.winner_relative_index = winner_relative_index
        self.end_time = end_time

    def display_match_for_choice(self):
        """Function that defines how a Match object is displayed in the tournament management menu"""
        chain = "{} contre {}".format(self.player_1_information,
                                      self.player_2_information)
        return chain

    def __repr__(self):
        """Function that defines how a Match object is represented"""
        if not self.winner_absolute_index:
            return "{} |contre| {}\nRésultats non rensseignés\nMatch Commencé {}.".format(self.player_1_information,
                                                                                          self.player_2_information,
                                                                                          self.start_time)
        if self.winner_absolute_index == -1:
            return "{} |contre| {}\nMatch nul\nMatch Commencé {}, Terminé {}.".format(self.player_1_information,
                                                                                      self.player_2_information,
                                                                                      self.start_time,
                                                                                      self.end_time)
        else:
            return "{} |contre| {}\nLe gagnant est: {}\nMatch Commencé {}, Terminé {}.".\
                format(self.player_1_information,
                       self.player_2_information,
                       self.players_object_list[self.winner_relative_index],
                       self.start_time,
                       self.end_time)

    def match_date_time(self):
        """Method that records the date and time of the start of the match."""
        time.strftime('')


class Tournament:
    """class which represent a tournament"""

    def __init__(self, tournament_name, tournament_place, tournament_date, end_date, time_controller,
                 number_of_turns, players_index_list, players_object_list, players_points=None,
                 actual_tour_number=None, state=None, round_list=None, tournament_comments=None):
        """Tournament constructor"""

        if actual_tour_number is None:
            actual_tour_number = 1
        if state is None:
            state = TOURNAMENTS_STATES[0]
        if players_points is None:
            players_points = [0, 0, 0, 0, 0, 0, 0, 0]
        if round_list is None:
            round_list = []
        if tournament_comments is None:
            tournament_comments = ""
        self.tournament_name = tournament_name
        self.tournament_place = tournament_place
        self.tournament_date = tournament_date
        self.end_date = end_date
        self.number_of_turns = number_of_turns
        self.round_list = round_list
        self.players_index_list = players_index_list
        self.players_points = players_points
        self.players_list = players_object_list
        self.time_controller = time_controller
        self.tournament_comments = tournament_comments
        self.actual_tour_number = actual_tour_number
        self.state = state

    def swiss_system(self):
        """Function used to create all players pair for match"""
        list_match = []
        index = 0
        sorted_players_list = self.players_list
        if self.actual_tour_number == 1:
            if not self.round_list:
                sorted_players_list = sorted(sorted_players_list, key=attrgetter("rank"), reverse=True)
                while index != NUMBER_OF_MATCH_PER_TOUR:
                    player_1 = sorted_players_list[index]
                    player_1_index = self.players_list.index(player_1)
                    player_2 = sorted_players_list[index + 4]
                    player_2_index = self.players_list.index(player_2)
                    list_match.append(Match([player_1, player_2], [player_1_index, player_2_index]))
                    index += 1
                self.round_list.append(list_match)
        if len(self.round_list) < self.actual_tour_number:
            sorted_list = []
            for player_index in self.players_index_list:
                sorted_list.append((player_index, self.players_points[player_index],
                                    str(self.players_list[player_index].rank)))
            sorted_list = sorted(sorted_list, key=itemgetter(1, 2), reverse=True)
            while index != NUMBER_OF_PLAYER:
                player_1_index = sorted_list[index][0]
                player_2_index = sorted_list[index + 1][0]
                player_1 = self.players_list[player_1_index]
                player_2 = self.players_list[player_2_index]
                list_match.append(Match([player_1, player_2], [player_1_index, player_2_index]))
                index += 2
            self.round_list.append(list_match)

    def __repr__(self):
        """Function that defines how a tournament object is represented"""
        return "Tournoi: {}, lieu: {}, date de debut: {}, date de fin: {}, etat:{}".format(self.tournament_name,
                                                                                           self.tournament_place,
                                                                                           self.tournament_date,
                                                                                           self.end_date,
                                                                                           self.state)


class DAO(ABC):
    """Abstract DAO Class"""

    def __init__(self, dao=DAO_OBJECT):
        """DOA constructor"""
        self.dao = dao


class PlayersDAO(DAO):
    """Class which represent the players database of the club"""

    def __init__(self):
        """PlayersDAO constructor"""

        DAO.__init__(self)
        self.players_list = []
        self.players_table = self.dao.table("players")

    def load_dao(self):
        """Function which loads players data from the dao"""

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
        """Function which saves the data into the dao"""

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
        """function that return True if the new player is already in the database"""

        for player in self.players_list:
            if new_player == player:
                return True
        return False


class TournamentsDAO(DAO):
    """Class which represent the tournaments database of the club"""

    def __init__(self, player_dao):
        """Dao constructor"""

        DAO.__init__(self)
        self.tournaments_list = []
        self.archived_tournaments_list = []
        self.active_tournaments_list = []
        self.tournaments_table = self.dao.table("tournaments")
        self.player_dao = player_dao

    def load_dao(self):
        """Method which loads tournaments data from the dao"""

        new_tournaments_list = []
        serialized_tournaments_list = self.tournaments_table.all()

        for serialized_tournament in serialized_tournaments_list:
            players_object_list = self.find_player_object(serialized_tournament, self.player_dao.players_list)
            round_list = self.match_deserialization(serialized_tournament["round_list"])
            new_tournaments_list.append(Tournament(tournament_name=serialized_tournament["tournament_name"],
                                                   tournament_place=serialized_tournament["tournament_place"],
                                                   tournament_date=serialized_tournament["tournament_date"],
                                                   end_date=serialized_tournament["end_date"],
                                                   number_of_turns=serialized_tournament["number_of_turns"],
                                                   players_points=serialized_tournament["players_points"],
                                                   round_list=round_list,
                                                   players_index_list=serialized_tournament["players_index_list"],
                                                   players_object_list=players_object_list,
                                                   time_controller=serialized_tournament["time_controller"],
                                                   tournament_comments=serialized_tournament["tournament_comments"],
                                                   actual_tour_number=serialized_tournament["actual_tour_number"],
                                                   state=serialized_tournament["state"]))

        self.tournaments_list = new_tournaments_list
        self.tournaments_distribution(new_tournaments_list)

    def save_dao(self):
        """Method which saves the data into the dao"""

        serialized_tournaments_list = []
        for tournament in self.tournaments_list:
            serialized_round_list = self.match_serialization(tournament)
            serialized_tournament = {"tournament_name": tournament.tournament_name,
                                     "tournament_place": tournament.tournament_place,
                                     "tournament_date": tournament.tournament_date,
                                     "end_date": tournament.end_date,
                                     "number_of_turns": tournament.number_of_turns,
                                     "round_list": serialized_round_list,
                                     "players_points": tournament.players_points,
                                     "players_index_list": tournament.players_index_list,
                                     "time_controller": tournament.time_controller,
                                     "tournament_comments": tournament.tournament_comments,
                                     "actual_tour_number": tournament.actual_tour_number,
                                     "state": tournament.state}

            serialized_tournaments_list.append(serialized_tournament)
        self.tournaments_table.truncate()
        self.tournaments_table.insert_multiple(serialized_tournaments_list)

    @staticmethod
    def match_serialization(tournament):
        """Method which serializes match object in round_list"""
        serialized_round_list = []
        if tournament.round_list:
            for tour in tournament.round_list:
                serialized_match_list = []
                for match in tour:
                    serialized_match = {"players_index_list": match.players_index_list,
                                        "winner_absolute_index": match.winner_absolute_index,
                                        "winner_relative_index": match.winner_relative_index,
                                        "start_time": match.start_date,
                                        "end_time": match.end_time}
                    serialized_match_list.append(serialized_match)
                serialized_round_list.append(serialized_match_list)
            return serialized_round_list
        else:
            return tournament.round_list

    def match_deserialization(self, serialized_round_list):
        """function which deserializes match from the dao"""

        round_list = []
        if serialized_round_list:
            for tour in serialized_round_list:
                match_list = []
                for serialized_match in tour:
                    player_object_list = self.find_player_object(serialized_match, self.player_dao.players_list)
                    match_list.append(Match(players_object_list=player_object_list,
                                            players_index_list=serialized_match["players_index_list"],
                                            winner_absolute_index=serialized_match["winner_absolute_index"],
                                            winner_relative_index=serialized_match["winner_relative_index"],
                                            start_time=serialized_match["start_time"],
                                            end_time=serialized_match["end_time"]))
                round_list.append(match_list)
            return round_list
        else:
            return serialized_round_list

    @staticmethod
    def find_player_object(serialized_tournament_or_match, players_list):
        """Method which returns a list containing player object find from a player index list """

        player_object_list = []
        index_list = serialized_tournament_or_match["players_index_list"]

        for index in index_list:
            player_object = players_list[index]
            player_object_list.append(player_object)

        return player_object_list

    def tournaments_distribution(self, tournaments_list):
        """Method that divides the tournaments into two lists depending on whether the
        tournament is in progress or not."""

        active_tournaments_list = [tournament for tournament in tournaments_list
                                   if tournament.state in TOURNAMENTS_STATES[0]]

        archived_tournaments_list = [tournament for tournament in tournaments_list
                                     if tournament.state in TOURNAMENTS_STATES[1:]]

        self.archived_tournaments_list = archived_tournaments_list
        self.active_tournaments_list = active_tournaments_list
