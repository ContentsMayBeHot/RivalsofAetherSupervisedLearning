import configparser
import enum
import os
import random
import re
import shutil

import numpy as np


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


class Player:
    def __init__(self, alias):
        self.alias = alias
        self.actions = []


class Replay:
    def __init__(self, replay_file):
        self.name = replay_file.name
        metadata = replay.readline()
        settings = replay.readlin()
        players = []
        for i in range(4):
            player_data = fin.readline()
            player_inputs = fin.readline()
            if player[0] is 'H':
                players.append((player_data, player_inputs))


def get_version_names(replays_path):
    p = re.compile('[0-9]{2}_[0-9]{2}_[0-9]{2}')
    return [ x for x in os.listdir(replays_path) if p.match(x) ]


class ReplayManager:
    def __init__(self, version_name):
        self.replays_path = self.__get_replays_path()
        self.version_path = os.path.join(self.replays_path, batch_name)
        self.batch = [
            dirent for dirent in os.listdir(self.version_path)
            if dirent.endswith('.roa')
            ]
        self.batch_unvisited = self.batch
        self.batch_visited = []
        self.current_replay = None

    def __get_replays_path(self):
        # Source: https://stackoverflow.com/a/3220762
        # The game agent will be run from SerpentAI\plugins. However, it needs
        # to be able to access roa.ini, which is located in capstone\plugins.
        plugins_path_relative = os.path.join('..', '..', '..')
        plugins_path = os.path.join(os.path.dirname(plugins_path_relative),
                                    os.readlink(plugins_path_relative))
        ini_path = os.path.join(plugins_path, '..', 'scripts', 'roa.ini')
        config = configparser.ConfigParser()
        config.read(ini_path)
        return config['RivalsofAether']['PathToReplays']

    def select_random_replay(self):
        next_replay_name = random.choice(self.batch_unvisited)
        self.replace_current_replay(next_replay_name)
        return self.read_current_replay()

    def read_current_replay(self):
        current_replay_path = os.path.join(self.replays_path,
                                           self.current_replay)
        with open(current_replay_path, 'r') as replay_file:
            return Replay(replay_file)

    def replace_current_replay(self, next_replay_name):
        self.current_replay = next_replay_name
        # Remove any existing replay files from the game's replays folder
        # Only one is allowed at a time because that's easier to deal with
        for dirent in os.listdir(self.replays_path):
            if dirent.endswith('.roa'):
                dirent_path = os.path.join(self.replays_path, dirent)
                os.remove(dirent_path)
        # Copy the specified replay file to the game's replays folder
        target_replay_path = os.path.join(self.version_path, replay_name)
        shutil.copy(target_replay_path, self.replays_path)
        # Update the batch trackers
        self.batch_visited.append(next_replay_name)
        self.batch_unvisited.remove(next_replay_name)
