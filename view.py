#! /usr/bin/env python3
# coding: utf-8

from simple_term_menu import TerminalMenu


class ChoiceMenu:
    """Choice menu class"""

    def __init__(self):
        """Menu Constructor"""
        pass

    def printing_menu(self, choices_list):
        """Function which display the menu"""
        menu = TerminalMenu(choices_list)
        choice_index = menu.show()
        return choice_index

#class qui permet d'afficher un champ à remplir à l'utilisateur
class FieldMenu:
    """Field menu class"""

    def __init__(self):
        """FieldMenu constructor"""
        pass

    def printing_field(self, message):
        """Method which print the field"""
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
        print(message)
        choice = self.printing_menu(self.validation_choices)
        return choice



class MainMenu(ChoiceMenu):

    def printing_menu(self):
        """Function which display the main menu"""
        main_menu = TerminalMenu(self.menu_choices)
        choice_index = main_menu.show()
        print(self.choice[choice_index])
        return choice_index

#class PlayerLastName():
        """Function which display the player last name menu"""

        last_name = input("veuillez saisir le nom du joueur: ")
        #return last_name

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



