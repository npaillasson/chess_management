#! /usr/bin/env python3
# coding: utf-8


# MENUS CHOICES
MAIN_MENU_CHOICES = ["Créer un joueur", "Créer un tournoi", "Gérer un tournoi en cours",
                     "Générer des rapports", "Règlages", "Quitter le logiciel"]

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

# list of adapted controllers
str_controller = ["last_name", "first_name"]
date_controller = ["date_of_birth"]
int_controller = ["rank"]

#TROUVER UN MOYEN D'AJOUTER LE GENRE!