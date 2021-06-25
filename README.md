# Chess management

***

This project is entirely coded in python 3.

This project is realized in the framework of a training on [OpenClassrooms](https://openclassrooms.com/fr/).
This project aims to create an offline software that allows to manage chess tournaments.


## Table of contents
1. [General information](#general-information)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Documentation](#documentation)

***

## General Information


This program allows you to manage chess tournaments, i.e:
* To create tournaments
* To register players 
* To enter match results 
* To maintain a player rating 
* To record the status of the program in a database
* etc ...

It also allows you to generate reports (player rating, list of matches ...). 

This software has been designed according to the MVC model,
so it is divided into three distinct parts: the **model**,
the **view** and the **controller**. It is also PEP8 compliant.


### What contains this repository?

#### Python files

**High level module**
* **main.py** : Allows to run the program from a terminal

**M**odel:
* **model.py** : Contains all classes related to the model

**V**iew:
* **view.py** : Contains all classes related to the view
* **menu.py** : Contains all texts, messages (alerts , information) in French

**C**ontroller:
* **controller.py** : Contains all classes related to the controller

#### Others
* **requierements.txt** (used to install required packages)
* **.gitignore** (contains paths of files that we don't want in our depository)
* **README.md** (the file you are reading now)

***

## Technologies

This project uses the next packages:


* [tinydb](https://pypi.org/project/tinydb/): version 4.4.0
* [simple-term-menu](https://pypi.org/project/simple-term-menu/): version 1.2.1
* [flake8](https://pypi.org/project/flake8/): version 3.9.2
* [flake8-html](https://pypi.org/project/flake8-html/): version 0.4.1



And their dependencies:

* [importlib-metadata](https://pypi.org/project/importlib-metadata/): version 4.5.0
* [Jinja2](https://pypi.org/project/Jinja2/): version 3.0.1
* [MarkupSafe](https://pypi.org/project/MarkupSafe/): version 2.0.1
* [mccabe](https://pypi.org/project/mccabe/): version 0.6.1
* [pycodestyle](https://pypi.org/project/pycodestyle/): version 2.7.0
* [pyflakes](https://pypi.org/project/pyflakes/): version 2.3.1
* [Pygments](https://pypi.org/project/Pygments/): version 2.9.0
* [zipp](https://pypi.org/project/zipp/): version 3.4.1

This project also uses the modules **'re'**, **'time'**, **'os'**, **'sys'**, **'abc'** and **'operator'**.

###

## Installation

To use this script you need a bash Terminal, if you are on Windows, please use the bash
terminal with "windows subsystem for linux" (WSL): 
[check here](https://docs.microsoft.com/en-us/windows/wsl/install-win10) for more information.

To get this project on your computer you can clone it:
```
$ git clone https://github.com/npaillasson/chess_management.git
```
To create your virtual environment you can use:
```
$ python3 -m venv env
```
Then activate your new virtual environment:
```
$ source env/bin/activate
```
Then install the required packages using the file 'requirements.txt':
```
$ pip install requirements.txt
```
To execute the script simply use:
```
$ python3 main.py
```
Or, alternatively:
```
$ ./main.py
```
At the end, you can deactivate the virtual environment with:
```
$ deactivate
```

###How to generate a new flake8-html file?

simply use:
```
$ flake8 --format=html --htmldir=flake-report main.py model.py controller.py menu.py view.py
```

###

##Documentation

When you run the script, you access the main menu.

This menu allows you to access the different functions of the software.

While using the software, don't worry about saving, the script automatically saves all 
modifications you make to the database (adding a player, adding a tournament, entering a score, etc.).

If you already have a database in the right format,
you can place it in the **'data/'** folder
(instead of the current database) in the root of the project.
This directory appears after the first use of the program.
If you do this, please respect the following file name: 'chess_database.json'.

* **Créer un joueur**

This menu allows you to create new players in the database.

Two players are considered identical if their name,
surname and date of birth are the same.
Two identical players cannot be added to the database.

* **Créer un tournoi**

This menu allows you to create a new tournament. 
It is only available if eight players are already in the database.
  
It is possible to indicate a different start and end date if needed.
The number of rounds is by default set to four, but it can be changed.

* **Modifier le score d'un joueur**

This menu allows you to change the current score of a player.

* **Gérer un tournoi en cours**

This menu allows you to enter the results of the matches in the current tournaments. 
It also allows you to launch rounds.
Moreover you can also cancel a tournament in progress if needed.

* **Générer des rapports** 

This menu allows you to generate different reports
(list of players, list of tournaments, etc.).

* **Quitter le logiciel**

This option allows you to exit the software.


