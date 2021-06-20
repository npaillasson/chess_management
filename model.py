#! /usr/bin/env python3
# coding: utf-8

from operator import attrgetter
import tinydb
from abc import ABC

DEFAULT_NUMBER_OF_TURNS = 4

TOURNAMENTS_STATES = ["In progress", "aborted", "Completed"]

DAO_PATH = "data/chess_database.json"

DAO_OBJECT = tinydb.TinyDB(DAO_PATH)

list_of_ongoing_tournaments = []

WINNER_POINT = 1

NULL_POINT = 0.5


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
        return str(self)

class Match:
    """class which represent a match"""
    def __init__(self, players_object_list, players_index_list, winner_index=None):
        """Match constructor"""
        self.players_object_list = players_object_list
        self.players_index_list = players_index_list
        self.player_1_information = self.players_object_list[0].last_name + self.players_object_list[0].first_name
        self.player_2_information = self.players_object_list[1].last_name + self.players_object_list[1].first_name
        self.winner_index = winner_index

    def __repr__(self):
        if not self.winner_index:
            return "{} contre {}".format(self.player_1_information, self.player_2_information)
        else:
            return "Le gagnant est: {}".format(self.players_object_list[self.winner_index])

class Round:
    """class which represent a round (list of 4 matches)"""

    def __init__(self, first_match, second_match, third_match, fourth_match):
        self.first_match = first_match
        self.second_match = second_match
        self.third_match = third_match
        self.fourth_match = fourth_match

    def __repr__(self):
        return "[{}, {}, {}, {}]".format(self.first_match, self.second_match, self.fourth_match, self.fourth_match)


class Tournament:
    """class which represent a tournament"""

    def __init__(self, tournament_name, tournament_place, tournament_date, end_date, time_controller,
                 number_of_turns, players_index_list, players_object_list, players_points=None,
                 actual_tour_number=0, state=None, round_list=None, tournament_comments=None):
        """Tournament constructor"""
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
        if self.actual_tour_number == 0:
            sorted_players_list = self.players_list
            sorted(sorted_players_list, key=attrgetter("rank"))
            list_match = []
            index = 0
            while index != 4:
                player_1 = sorted_players_list[index]
                player_1_index = self.players_list.index(player_1)
                player_2 = sorted_players_list[index + 4]
                player_2_index = self.players_list.index(player_2)
                list_match.append(Match([player_1, player_2], [player_1_index, player_2_index]))
                index += 1
            self.round_list.append(list_match)
        else:
            pass

    def __repr__(self):
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
        """function that return True if the new player is already in the database"""

        for player in self.players_list:
            if new_player == player:
                return True
        return False


class TournamentsDAO(DAO):
    """Class which represent the tournaments database of the club"""

    def __init__(self, player_dao):
        """DataBase constructor"""

        DAO.__init__(self)
        self.tournaments_list = []
        self.archived_tournaments_list = []
        self.active_tournaments_list = []
        self.tournaments_table = self.dao.table("tournaments")
        self.player_dao = player_dao

    def load_dao(self):
        """Function which load tournaments data from the database"""

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
        """Function which save the data into the database"""

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
            print(serialized_tournament)

            serialized_tournaments_list.append(serialized_tournament)
        print("tournament_list_after_save", self.tournaments_list)
        self.tournaments_table.truncate()
        self.tournaments_table.insert_multiple(serialized_tournaments_list)
        #self.tournaments_distribution(self.tournaments_list)

    def match_serialization(self, tournament):
        """function which serialise match object in round_list"""
        serialized_round_list = []
        if tournament.round_list:
            for tour in tournament.round_list:
                serialized_match_list = []
                for match in tour:
                    print(match)
                    serialized_match = {"players_index_list": match.players_index_list,
                                        "winner_index": match.winner_index}
                    serialized_match_list.append(serialized_match)
            serialized_round_list.append(serialized_match_list)
            #print("liste de match serialisé:",serialized_match_list)
            #print("liste des tour serialisé:",serialized_round_list)
            return serialized_round_list
        else:
            return tournament.round_list

    def match_deserialization(self, serialized_round_list):
        """function which deserialize match"""
        round_list = []
        if serialized_round_list:
            for tour in serialized_round_list:
                match_list = []
                for serialized_match in tour:
                    player_object_list = self.find_player_object(serialized_match, self.player_dao.players_list)
                    match_list.append(Match(players_object_list=player_object_list,
                                            players_index_list=serialized_match["players_index_list"],
                                            winner_index=serialized_match["winner_index"]))
                    round_list.append(match_list)
            return round_list
        else:
            return serialized_round_list

    @staticmethod
    def find_player_object(serialized_tournament_or_match, players_list):

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
