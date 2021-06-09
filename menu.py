#! /usr/bin/env python3
# coding: utf-8


# MENUS CHOICES
# list which contains the choices of the main menu
MAIN_MENU_CHOICES = ["Créer un joueur", "Créer un tournoi", "Gérer un tournoi en cours",
                     "Générer des rapports", "Règlages", "Quitter le logiciel"]

# list which contains the choices of the "correction menu"
CORRECTION_MENU_CHOICES = ["Valider !", "Corriger", "Annuler"]

# FIELD MENUS MESSAGE (key = data name, value = list which contains all message about data)
# {"name" : [request_message, incorrect_input_message], ...]
PLAYERS_FIELD_MESSAGE = {"last_name": ["veuillez saisir le nom du joueur: ", "Nom invalide !"],
                         "first_name": ["veuillez saisir le prénom du joueur: ", "Prénom invalide !"],
                         "date_of_birth": ["veuillez saisir la date de naissance du joueur: ", "date invalide !"],
                         "rank": ["veuillez saisir le rang du joueur: ", "rang invalide !"]}

# VALIDATION MENUS MESSAGE (key = data name, value = list which contains all message about data)
# {"name" : [message, [choice 1, choice 2]], ...]
VALIDATION_MENU_MESSAGE = {"gender": ["Rensseigner le genre du joueur", ["Femme", "Homme", "Autre"]]}

# SIGN MESSAGE
welcome_message = "Bienvenue dans chess management !"
player_already_exists = "Le joueur exist déjà !"


def players_formatting(player_information):
    """Function which take a dict with players information and format it"""
    return "\nNom : {}\nPrénom : {} \nDate de naissance : {}\nGenre : {}\nRang : {}\n".\
        format(player_information["last_name"],
               player_information["first_name"],
               player_information["date_of_birth"],
               player_information["gender"],
               player_information["rank"])
