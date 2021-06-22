#! /usr/bin/env python3
# coding: utf-8

"""view module, contains the next classes, ChoiceMenu, FieldMenu, Sign, ValidationMenu"""

from simple_term_menu import TerminalMenu


class ChoiceMenu:
    """Choice menu class"""

    @staticmethod
    def printing_menu_index(choices_list):
        """Function which display the menu and return the index of the user's choice"""
        menu = TerminalMenu(choices_list)
        choice_index = menu.show()
        return choice_index

    @staticmethod
    def printing_menu_value(choices_list):
        """Function which display the menu and return the value of the user's choice"""
        menu = TerminalMenu(choices_list)
        choice_index = menu.show()
        choice_value = choices_list[choice_index]
        return choice_value


# class that allows to display a field to fill to the user
class FieldMenu:
    """Field menu class"""

    @staticmethod
    def printing_field(message):
        """Method to print a message and an input field to allow the user to enter information"""
        while True:
            try:
                value = input(message)
            except UnicodeDecodeError:
                print("la chaine de caractère contient un caractère interdit... (par exemple '°')")
                continue
            return value.strip()


class Sign:
    """Sign class"""

    @staticmethod
    def printing_sign(*message):
        """displays a message to the user"""
        print(*message)


class ValidationMenu(ChoiceMenu):
    """validation menu class"""

    def __init__(self, validation_choices):
        """Validation menu constructor"""

        ChoiceMenu.__init__(self)
        self.validation_choices = validation_choices

    def printing_correction_menu(self, message):
        """function which displays a choice menu to confirm, cancel or correct an entry
        ex: name = John
        are you sure?
        - Confirm
        - Correct
        - Cancel"""

        print(message)
        choice = self.printing_menu_index(self.validation_choices)
        return choice

    def printing_proposal_menu(self, message, validation_choices, index=True):
        """function which displays a proposal menu. It's a choice menu with a contextual message. return a value.
        ex: please select the gender of the player:
        -Man
        -Woman
        -Else

        if index is True, the function return the index of the value. If not, the function return the value"""

        print(message)
        if index:
            choice = self.printing_menu_index(validation_choices)
        else:
            choice = self.printing_menu_value(validation_choices)
        return choice
