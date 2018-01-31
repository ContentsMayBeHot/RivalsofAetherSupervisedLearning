import configparser
import enum
import os
import random
import re
import shutil

import util

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


class ReplayManager:
    def __init__(self, version_name):
        self.replays_path = util.get_replays_path()
        self.version_path = os.path.join(self.replays_path, batch_name)
        
        self.dataset = [
            dirent for dirent in os.listdir(self.version_path)
            if dirent.endswith('.roa')
            ]
        self.dataset_unvisited = self.dataset
        self.dataset_visited = []

    def select_replay(self, replay_name=None):
        if not replay_name:
            replay_name = random.choice(self.dataset_unvisited)
        self.replace_current_replay(next_replay_name)
        return next_replay_name

    def replace_current_replay(self, replay_name):
        self.current_replay = replay_name
        # Remove any existing replay files from the game's replays folder
        # Only one is allowed at a time because that's easier to deal with
        for dirent in os.listdir(self.replays_path):
            if dirent.endswith('.roa'):
                dirent_path = os.path.join(self.replays_path, dirent)
                os.remove(dirent_path)
        # Copy the specified replay file to the game's replays folder
        target_replay_path = os.path.join(self.version_path, replay_name)
        shutil.copy(target_replay_path, self.replays_path)
        # Update the visited tracker
        self.dataset_visited.append(replay_name)
        self.dataset_unvisited.remove(replay_name)


# Reference: https://github.com/sorki/python-mnist/blob/master/mnist/loader.py
class ReplayLoader:
    def __init__(self, path='.'):
        self.path = path
        self.test_path = os.path.join(path, 'test')
        self.train_path = os.path.join(path, 'train')

        self.test_frames = []
        self.train_frames = []

        self.test_replays = []
        self.train_replays = []

    def load(self, frames_path, replays_path):
        pass

    def load_testing(self):
        return self.test_frames, self.test_replays

    def load_training(self):
        return self.train_frames, self.train_replays
