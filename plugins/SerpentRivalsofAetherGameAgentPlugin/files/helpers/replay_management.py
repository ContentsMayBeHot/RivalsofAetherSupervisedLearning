import configparser
import enum
import os
import random
import re
import shutil


FRAMES_PER_SECOND = 60.0


class Stage(enum.Enum):
    TREETOP_LODGE = 1
    FIRE_CAPITOL = 2
    AIR_ARMADA = 3
    ROCK_WALL = 4
    MERCHANT_PORT = 5
    BLAZING_HIDEOUT = 7
    TOWER_OF_HEAVEN = 8


class StageMode(enum.Enum):
    BASIC = 0
    AETHER = 1


class Character(enum.Enum):
    ZETTERBURN = 2
    ORCANE = 3
    WRASTOR = 4
    KRAGG = 5
    FORSBURN = 6
    MAYPUL = 7
    ABSA = 8
    ETALUS = 9
    ORI = 10
    RANNO = 11
    CLAIREN = 12


class InputSequences:
    splash_to_main = [1.5, 'Z', 'X', 'Z', 'Z', 'Z', 'Z']
    main_to_replay = [0.5, 'DOWN', 'DOWN', 'DOWN', 'Z', 1, 'Z']
    start_replay_1 = [1, 'Z', 'Z']
    back_and_forth = [1, 'X', 'Z']


class ReplayManager:
    def __init__(self):
        # Get path to plugins folder
        # Traversing symlinks: https://stackoverflow.com/a/3220762
        plugins_relpath = os.path.join('..', '..', '..')
        plugins_abspath = os.path.join(os.path.dname(plugins_relpath),
                                       os.readlink(plugins_relpath))
        # Establish path from plugins folder to configuration file
        self.config_abspath = os.path.join(plugins_path, '..',
                                           'scripts', 'roa.ini')
        # Open the configuration file
        self.config = configparser.ConfigParser()
        config.read(self.config_abspath)

        # Establish path to replays folder
        self.replays_abspath = config['RivalsofAether']['PathToReplays']

        # Initialize subdataset values to 'None'
        self.__flush_subdataset()

    def load_subdataset(self, subdataset_dname):
        '''Load the subdataset for a particular game version.'''
        self.subdataset_abspath = os.path.join(self.replays_abspath,
                                               subdataset_dname)
        self.subdataset = [
            dirent for dirent in os.listdir(self.subdataset_abspath)
            if dirent.endswith('.roa')
            ]
        self.subdataset_unvisited = list(self.subdataset) # Ensure it's a copy
        self.subdataset_visited = []

    def __flush_subdataset(self):
        '''Reset subdataset to starting values.'''
        self.subdataset_abspath = None
        self.subdataset = None
        self.subdataset_unvisited = None
        self.subdataset_visited = None

    def get_available_subdatasets(self):
        '''Get a list of subdatasets, where each represents a game version.'''
        p = re.compile('[0-9]{2}_[0-9]{2}_[0-9]{2}')
        return [ x for x in os.listdir(self.replays_abspath) if p.match(x) ]

    def next_roa(self):
        '''Get a new .roa file.'''
        if not self.dataset_unvisited:
            return None
        roa_fname = self.subdataset_unvisited[0]

        self.__flush_replays()
        self.__transfer_roa(roa_fname)
        self.__visit(roa_fname)

        return roa_fname

    def __flush_replays(self):
        ''' Remove all .roa files from the replays folder.'''
        # Get contents of replays folder
        for dirent in os.listdir(self.replays_abspath):
            # Check for .roa extension
            if dirent.endswith('.roa'):
                # Delete the .roa file
                dirent_abspath = os.path.join(self.replays_abspath, dirent)
                os.remove(dirent_abspath)

    def __transfer_roa(self, roa_fname):
        '''Copy specified .roa file from subdataset folder to replays folder.'''
        # Copy the specified replay file to the game's replays folder
        roa_abspath = os.path.join(self.subdataset_abspath, roa_fname)
        shutil.copy(roa_abspath, self.replays_abspath)

    def __visit_roa(self, roa_fname):
        '''Mark specified .roa file as visited.'''
        self.dataset_visited.append(roa_fname)
        self.dataset_unvisited.remove(roa_fname)


# Reference: https://github.com/sorki/python-mnist/blob/master/mnist/loader.py
class ReplayLoader:
    def __init__(self, replays_abspath='.'):
        self.replays_abspath = replays_abspath
        self.testing_dname = 'testing'
        self.training_dname = 'training'

        self.testing_x = []
        self.testing_y = []

        self.training_x = []
        self.training_y = []

    def load(self, x_abspath, y_abspath):
        pass

    def load_testing(self):
        return self.testing_x, self.testing_y

    def load_training(self):
        return self.training_x, self.training_y
