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
    @classmethod
    def __init__(self):
        self.replays_abspath = ReplayManager.get_replays_path()
        self.config_abspath = ReplayManager.get_ini_path()

        self.subdataset_abspath = None
        self.subdataset = None
        self.subdataset_unvisited = None
        self.subdataset_visited = None

    def set_subdataset(self, subdataset_dname):
        self.subdataset_abspath = os.path.join(self.replays_abspath,
                                               subdataset_dname)
        self.subdataset = [
            dirent for dirent in os.listdir(self.subdataset_abspath)
            if dirent.endswith('.roa')
            ]
        self.subdataset_unvisited = list(self.subdataset)
        self.subdataset_visited = []

    @staticmethod
    def get_ini_path():
        # Source: https://stackoverflow.com/a/3220762
        # The game agent will be run from SerpentAI\plugins. However, it needs
        # to be able to access roa.ini, which is located in capstone\plugins.
        plugins_path_relative = os.path.join('..', '..', '..')
        plugins_path = os.path.join(os.path.dname(plugins_path_relative),
                                    os.readlink(plugins_path_relative))
        return os.path.join(plugins_path, '..', 'scripts', 'roa.ini')

    @staticmethod
    def read_replays_path(ini_path=None):
        if not ini_path:
            ini_path = get_ini_path()
        config = configparser.ConfigParser()
        config.read(ini_path)
        return config['RivalsofAether']['PathToReplays']

    @staticmethod
    def read_replay_version(ini_path=None):
        if not ini_path:
            ini_path = get_ini_path()
        config = configparser.ConfigParser()
        config.read(ini_path)
        return config['RivalsofAether']['GameVersion']

    @staticmethod
    def get_version_names(replays_path=None):
        if not replays_path:
            replays_path = get_replays_path()
        p = re.compile('[0-9]{2}_[0-9]{2}_[0-9]{2}')
        return [ x for x in os.listdir(replays_path) if p.match(x) ]

    @classmethod
    def get_random_replay(self, replay_name=None):
        if not replay_name:
            replay_name = random.choice(self.dataset_unvisited)
        self.replace_current_replay(next_replay_name)
        return next_replay_name

    @classmethod
    def get_next_roa(self):
        '''Replace current .roa file in replays folder with an unvisited one.'''
        if not self.dataset_unvisited:
            return None
        roa_fname = self.subdataset_unvisited[0]

        self.__flush_roas()
        self.__move_roa_to_replays(roa_fname)
        self.__visit(roa_fname)

        return roa_fname

    @classmethod
    def __flush_roas(self):
        ''' Remove all .roa files from the replays folder.'''
        for dirent in os.listdir(self.replays_abspath):
            if dirent.endswith('.roa'):
                dirent_path = os.path.join(self.replays_abspath, dirent)
                os.remove(dirent_path)

    @classmethod
    def __move_roa_to_replays(self, roa_fname):
        '''Copy specified .roa file from subdataset folder to replays folder.'''
        # Copy the specified replay file to the game's replays folder
        roa_abspath = os.path.join(self.subdataset_abspath, roa_fname)
        shutil.copy(roa_abspath, self.replays_abspath)

    @classmethod
    def __visit_roa(self, roa_fname):
        '''Mark specified .roa file as visited.'''
        self.dataset_visited.append(roa_fnameroa_fname)
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
