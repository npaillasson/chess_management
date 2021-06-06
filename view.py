#! /usr/bin/env python3
# coding: utf-8

from simple_term_menu import TerminalMenu


class Menu:
    """Main menu class"""

    def __init__(self, choices_main_menu_list):
        """MainMenu Constructor"""
        self.choices_main_menu_list = choices_main_menu_list

    def main_menu(self):
        """Function which display the main menu"""
        main_menu = TerminalMenu(self.choices_main_menu_list, title="Main menu")
        choice_index = main_menu.show()
        print(self.choices_main_menu_list[choice_index])
        return choice_index

    def player_last_name(self):
        """Function which display the player last name menu"""

        last_name = input("veuillez saisir le nom du joueur: ")
        return last_name

    def player_first_name(self):
        """Function which display the player first name menu"""

        first_name = input("veuillez saisir le prénom du joueur: ")
        return first_name

    def player_date_of_birth(self):
        """Function which display the player first name menu"""

        date_of_birth = input("veuillez saisir la date de naissance du joueur: ")
        return date_of_birth



