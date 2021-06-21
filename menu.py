#! /usr/bin/env python3
# coding: utf-8

DRAW_MATCH_KEY_WORD = "Match nul"
STOP_FUNCTION_KEY_WORD = "quit"
TOURNAMENT_STATE = ["En cours", "abandonné", "Terminé"]

# MENUS CHOICES
# list which contains the choices of the main menu
MAIN_MENU_CHOICES = ["Créer un joueur", "Créer un tournoi", "Modifier le score d'un joueur",
                     "Gérer un tournoi en cours", "Générer des rapports", "chargé une base de donnée",
                     "Quitter le logiciel"]

# list which contains the choices of the "correction menu"
CORRECTION_MENU_CHOICES = ["Valider !", "Corriger", "Annuler"]

# FIELD MENUS MESSAGE (key = data name, value = list which contains all message about data)
# {"name" : [request_message, incorrect_input_message], ...]
yes_no_menu = ["Non", "Oui"]
FIELD_MESSAGE = {"last_name": ["veuillez saisir le nom du joueur: ", "Nom invalide !"],
                 "first_name": ["veuillez saisir le prénom du joueur: ", "Prénom invalide !"],
                 "date_of_birth": ["veuillez saisir la date de naissance du joueur: ", "date invalide !"],
                 "rank": ["veuillez saisir le rang du joueur: ", "rang invalide !"],
                 "number_of_turn": ["Reglez le nombre de tours (4 par défaut) ", "Nombre de tous invalide !"],
                 "tournament_name": ["Quel est le nom du tournoi ? ", "Nom invalide !"],
                 "tournament_place": ["Ou se déroule le tournoi ? ", "lieu invalide ! "],
                 "tournament_comments": ["Voulez-vous faire un commentaire (facultatif)? "],
                 "tournament_date": ["A quelle date le tournoi commence t'il ? ", "date invalide !"],
                 "end_date": ["A quelle date le tournoi fini t'il ? ", "date invalide !"],
                 "score_request": ["Veuillez saisir le score du joueur: ", "score invalide ! "]}

# VALIDATION MENUS MESSAGE (key = data name, value = list which contains all message about data)
# {"name" : [message, [choice 1, choice 2]], ...]
PROPOSAL_MENU_MESSAGE = {"gender": ["Rensseigner le genre du joueur", ["Femme", "Homme", "Autre"]],
                         "other_date_request": ["Le tournoi se déroule t'il sur plus d'un jour ?",
                                                yes_no_menu],
                         "time_control": ["quel est le type de jeu souhaité?", ["Bullet", "Blitz", "Fast chess"]],
                         "set_match": "choisissez le match dont vous souhaitez saisir le score",
                         "abort_tournament": ["souhaitez-vous annuler définitivement le tournoi ?",
                                              yes_no_menu],
                         "result_match_request": ["quel joueur à gagné le match?"]}

# SIGN MESSAGE
welcome_message = "Bienvenue dans chess management !"
player_already_exists = "Le joueur exist déjà !"
not_enough_players = "Vous avez moins de 8 joueurs dans la base de données !"
tour_number = "Tour numéro"
add_comments = "ajouter un commentaire au tournoi"
abort_tournament = "Abandonner le tournoi"
end_of_tournament = "Le tournoi est désormais terminé !"


def players_formatting(player_information):
    """Function which take a dict with players information and format it"""
    return "\nNom : {}\nPrénom : {} \nDate de naissance : {}\nGenre : {}\nRang : {}\n".\
        format(player_information["last_name"],
               player_information["first_name"],
               player_information["date_of_birth"],
               player_information["gender"],
               player_information["rank"])

def tournament_formatting(tournament_information):
    """Function which take a dict with players information and format it"""

    return "\nNom : {}\nlieu : {} \nDate de début : {}\nDate de fin : {}\nNombre de tours : {}\n" \
           "joueurs participants : {}\n type de match : {}\n commentaire : {}".\
        format(tournament_information["tournament_name"],
               tournament_information["tournament_place"],
               tournament_information["tournament_date"],
               tournament_information["end_date"],
               tournament_information["number_of_turn"],
               tournament_information["players_object_list"],
               tournament_information["time_control"],
               tournament_information["tournament_comments"])


def match_formatting(player_1, player_2, winner_player):

    return "GOGGG{} {} contre {} {}\ngagnant: {}".format(player_1.first_name,
                                                    player_1.last_name,
                                                    player_2.first_name,
                                                    player_2.last_name,
                                                    winner_player)
