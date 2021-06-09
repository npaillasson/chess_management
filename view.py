#! /usr/bin/env python3
# coding: utf-8

from simple_term_menu import TerminalMenu


class ChoiceMenu:
    """Choice menu class"""

    def __init__(self):
        """Menu Constructor"""
        pass

    def printing_menu_index(self, choices_list):
        """Function which display the menu"""
        menu = TerminalMenu(choices_list)
        choice_index = menu.show()
        return choice_index

    def printing_menu_value(self, choices_list):
        menu = TerminalMenu(choices_list)
        choice_index = menu.show()
        choice_value = choices_list[choice_index]
        return choice_value

#class qui permet d'afficher un champ à remplir à l'utilisateur
class FieldMenu:
    """Field menu class"""

    def __init__(self):
        """FieldMenu constructor"""
        pass

    def printing_field(self, message):
        """Method which print the field"""
        print("tapez 'quit' pour revenir au menu principale")
        value = input(message)
        return value

#class qui permet d'afficher un message
class Sign:
    """Sign class"""

    def __init__(self):
        """Sign class constructor"""
        pass

    def printing_sign(self, message):
        """method which print the sign"""
        print(message)


class ValidationMenu(ChoiceMenu):
    """validation menu class"""

    def __init__(self, validation_choices):
        """Validation menu constructor"""

        ChoiceMenu.__init__(self)
        self.validation_choices = validation_choices

    def printing_correction_menu(self, message):
        """function wich displays a choice menu to confirm, cancel or correct an entry
        ex: name = John
        are you sure?
        - Confirm
        - Correct
        - Cancel"""

        print(message)
        choice = self.printing_menu_index(self.validation_choices)
        return choice

    def printing_proposal_menu(self, message, validation_choices, index=True):
        """function which displays a proposal menu. it is a choice menu with a contextual message. return a value.
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






