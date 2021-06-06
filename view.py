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
