import configparser
import os
import random
import re
import shutil


class ReplayManager:
    def __init__(self):
        # Source: https://stackoverflow.com/a/3220762
        # The game agent will be run from SerpentAI\plugins. However, it needs
        # to be able to access roa.ini, which is located in capstone\plugins.
        plugins_path = os.path.join(os.path.dirname('..'), os.readlink('..'))
        ini_path = os.path.join(plugins_path, '..', 'scripts', 'roa.ini')
        config = configparser.ConfigParser()
        config.read(ini_path)
        self.replays_path = config['RivalsofAether']['PathToReplays']
        self.all_batch_names = [
            x for x in os.listdir(self.replays_path) if x.
        ]
        p = re.compile('[0-9]{2}_[0-9]{2}_[0-9]{2}')
        self.valid_batch_names = [x for x in os.listdir() if p.match(x)]

    def set_batch(self, batch_name):
        self.batch_path = os.path.join(self.replays_path, batch_name)
        self.batch = [
            dirent for dirent in os.listdir(self.batch_path)
            if dirent.endswith('.roa')
            ]
        self.batch_unvisited = self.batch
        self.batch_visited = []
        self.current_replay = None

    def select_random_replay(self):
        next_replay_name = random.choice(self.batch_unvisited)
        self.replace_current_replay(next_replay_name)
        return self.read_current_replay()

    def read_current_replay(self):
        current_replay_path = os.path.join(self.replays_path,
                                           self.current_replay)
        with open(current_replay_path, 'r') as fin:
            replay_metadata = fin.readline()
            match_settings = fin.readline()
            players = []
            for i in range(4):
                player_data = fin.readline()
                player_inputs = fin.readline()
                if player[0] is 'H':
                    players.append((player_data, player_inputs))
        return (replay_metadata, match_settings, players)

    def replace_current_replay(self, target_replay_name):
        self.current_replay = target_replay_name
        # Remove any existing replay files from the game's replays folder
        # Only one is allowed at a time because that's easier to deal with
        for dirent in os.listdir(self.replays_path):
            if dirent.endswith('.roa'):
                dirent_path = os.path.join(self.replays_path, dirent)
                os.remove(dirent_path)
        # Copy the specified replay file to the game's replays folder
        target_replay_path = os.path.join(self.batch_path, replay_name)
        shutil.copy(target_replay_path, self.replays_path)
        # Update the batch trackers
        self.batch_visited.append(target_replay_name)
        self.batch_unvisited.remove(target_replay_name)
