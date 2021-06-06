#! /usr/bin/env python3
# coding: utf-8

from simple_term_menu import TerminalMenu


class Menu:
    """Main menu class"""

    def __init__(self, choices_main_menu_list, choices_correction_menu):
        """Menu Constructor"""
        self.choices_main_menu_list = choices_main_menu_list
        self.choices_correction_menu = choices_correction_menu

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
        """Function which display the player date_of_birth menu"""

        date_of_birth = input("veuillez saisir la date de naissance du joueur: ")
        return date_of_birth

    def player_rank(self):
        """Function which display the player rank menu"""
        player_rank = input("veuillez saisir le rang du joueur: ")
        return player_rank

    def player_validation(self, player_information, correction_menu_choices):
        """function which allows to check and correct the player information"""
        print("Nom : {} \nPrénom : {} \nDate de naissance : {}\nRang : {}".format(player_information["last_name"],
                                                                                  player_information["first_name"],
                                                                                  player_information["date_of_birth"],
                                                                                  player_information["rank"]))
        correction_menu = TerminalMenu(self.choices_correction_menu)
        choice_index = correction_menu.show()
        print(self.choices_correction_menu[choice_index])
        return choice_index



