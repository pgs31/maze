'''
    example.py

    Some examples of creating mazes, running games, collecting statistics, and opening the GUI.
'''

import sys
import time
import imp

from collections import defaultdict

from PyQt5.QtWidgets import QApplication

from maze import Maze, Game, game_repeater
from mazes import OPEN, TIGHT
from goodies import RandomGoody
from baddies import RandomBaddy
from gui import GameViewer
from sw_players import Explorer, Ninja

GUI = False
STATS = True

USERS = "wuhyun1120 TorbenSell ChristopherDesira"

EXAMPLE_MAZE = Maze(10, 10, "0001010000"
                            "0111010101"
                            "0100000011"
                            "0110100010"
                            "0000100110"
                            "1111100000"
                            "0000001000"
                            "1000111010"
                            "0010001010"
                            "1100101010")

def text_example():
    ''' Prints the state of the game to stdout after each round of turns '''

    goody0 = RandomGoody()
    goody1 = RandomGoody()
    baddy = Ninja()

    game = Game(EXAMPLE_MAZE * (2, 2), goody0, goody1, baddy)

    def hook(game):
        print(game, "\n")
        time.sleep(0.1)  # Max speed of 10 updates per second

    game.play(hook=hook)


def stats_play(maze, goody1, goody2, baddy, total_games):

    #import pdb; pdb.set_trace()
    # Gui first
    if GUI:
        gv = GameViewer()
        gv.show()
        gv.set_game(Game(maze, goody1(), goody2(), baddy()))
        gv.setWindowTitle("{} and {} vs {}".format(goody1.__module__, goody2.__module__, baddy.__name__))
        gv.exec_()

    if STATS:
        # Then stats
        results = defaultdict(int)
            
        for game_number, game in enumerate(game_repeater(maze, goody1, goody2, baddy)):
            if game_number == total_games:
                break
            result, _rounds = game.play()
            results[result] += 1

        fraction_won = float(results['goodies win']) / (results['goodies win'] + results['baddy wins'])
        return fraction_won
    return float('nan')
    
def goodie_for_user(user):
    user_module = imp.load_source(user, user + '/goodies.py')
    goody = user_module.RandomGoody
    return goody

    
def stats_example(user, total_games):
    ''' Plays many games, printing cumulative and final stats '''

    app = QApplication.instance() or QApplication(sys.argv)

    goody = goodie_for_user(user)
    
    print("{} random  example {:0>2.0f}%".format(user.ljust(20), stats_play(EXAMPLE_MAZE* (2, 2), goody, goody, RandomBaddy, total_games) * 100))
    print("{} random  open    {:0>2.0f}%".format(user.ljust(20), stats_play(OPEN* (2, 2),         goody, goody, RandomBaddy, total_games) * 100))
    print("{} random  tight   {:0>2.0f}%".format(user.ljust(20), stats_play(TIGHT* (2, 2),        goody, goody, RandomBaddy, total_games) * 100))
    print("{} ninja   example {:0>2.0f}%".format(user.ljust(20), stats_play(EXAMPLE_MAZE* (2, 2),  goody, goody, Ninja, total_games) * 100))
    print("{} ninja   open    {:0>2.0f}%".format(user.ljust(20), stats_play(OPEN* (2, 2),          goody, goody, Ninja, total_games) * 100))
    print("{} ninja   tight   {:0>2.0f}%".format(user.ljust(20), stats_play(TIGHT* (2, 2),         goody, goody, Ninja, total_games) * 100))

def gui_example():
    ''' Opens a GUI, allowing games to be stepped through or quickly played one after another '''
    app = QApplication.instance() or QApplication(sys.argv)
    gv = GameViewer()
    gv.show()
    gv.set_game_generator(game_repeater(EXAMPLE_MAZE * (3, 3), RandomGoody, RandomGoody, RandomBaddy))
    app.exec_()

if __name__ == "__main__":
    # Uncomment whichever example you want to run
    # text_example()
    for user in USERS.split():
        stats_example(user, 100)
    # gui_example()

    