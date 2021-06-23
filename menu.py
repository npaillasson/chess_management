#! /usr/bin/env python3
# coding: utf-8

"""menu module, contains all menu choices and messages"""

DRAW_MATCH_KEY_WORD = "Match nul"

STOP_FUNCTION_KEY_WORD = "quit"

TOURNAMENT_STATE = ["En cours", "abandonné", "Terminé"]

# MENUS CHOICES
# list which contains the choices of the main menu
MAIN_MENU_CHOICES = ["Créer un joueur", "Créer un tournoi", "Modifier le score d'un joueur",
                     "Gérer un tournoi en cours", "Générer des rapports",
                     "Quitter le logiciel"]

REPORTS_MAIN_MENU = ["Liste des joueurs", "Liste des tournois", "Liste des joueurs d'un tournoi",
                     "Liste des tours et matchs d'un tournoi", STOP_FUNCTION_KEY_WORD]

REPORTS_SUB_MENU = ["Trié par ordre alphabétique", "Trié par classement", STOP_FUNCTION_KEY_WORD]

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
                         "result_match_request": ["quel joueur à gagné le match?"],
                         "load_new_database": ["Placer une nouvelle base de données dans le fichier '/data'\n"
                                               "à la racine du logiciel puis cliquer sur 'valider' pour\n"
                                               " charger la nouvelle base de données", ["Annuler", "Valider"]]}

# SIGN MESSAGE
welcome_message = "Bienvenue dans chess management !"
player_already_exists = "Le joueur exist déjà !"
not_enough_players = "Vous avez moins de 8 joueurs dans la base de données !"
add_comments = "ajouter un commentaire au tournoi"
abort_tournament = "Abandonner le tournoi"
end_of_tournament = "Le tournoi est désormais terminé !"
quit_report = "\n(Pour revenir au menu principal tapez 'quit')\n\n"


def actual_turn_formating(tournament):
    """stop"""
    return "Round numéro: {}/{}".format(str(tournament.actual_tour_number), str(tournament.number_of_turns))


def players_formatting(player_information):
    """Function which takes a dict with players information as argument, and returns a formatted string"""
    return "\nNom : {}\nPrénom : {} \nDate de naissance : {}\nGenre : {}\nRang : {}\n".\
        format(player_information["last_name"],
               player_information["first_name"],
               player_information["date_of_birth"],
               player_information["gender"],
               player_information["rank"])


def tournament_formatting(tournament_information):
    """Function which takes a dict with tournament information as argument, and returns a formatted string"""

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
    """Function which returns a formatted string with various information about the match"""

    return "{} {} contre {} {}\ngagnant: {}".format(player_1.last_name,
                                                    player_1.first_name,
                                                    player_2.last_name,
                                                    player_2.first_name,
                                                    winner_player)


def tournament_report_formatting(tournament):
    """Function that takes a dict with tournament information as argument, and returns a formatted
    string used to generate reports."""

    return "Nom: {}, lieu: {} \nDate de début: {}, Date de fin: {}\nNombre de tours: {}," \
           " Type de match: {}\nEtat du tournoi: {}\nCommentaire(s): {}\n".format(tournament.tournament_name,
                                                                                  tournament.tournament_place,
                                                                                  tournament.tournament_date,
                                                                                  tournament.end_date,
                                                                                  tournament.number_of_turns,
                                                                                  tournament.time_controller,
                                                                                  tournament.state,
                                                                                  tournament.tournament_comments)


def tour_report_formatting(tour, index):
    """Function that takes a dict with tour information as argument, and returns a formatted
        string used to generate reports."""

    return "Tour n°{}\n____\n{}\n____\n{}\n____\n{}\n____\n{}\n____\n".format(index,
                                                                              tour[0],
                                                                              tour[1],
                                                                              tour[2],
                                                                              tour[3])
