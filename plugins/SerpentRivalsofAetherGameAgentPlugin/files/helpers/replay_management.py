import configparser
import os
import shutil

class ReplayManager:
    all_batch_names = [
        '01_00_02',
        '01_00_03',
        '01_00_05',
        '01_01_02',
        '01_02_01',
        '01_02_02'
    ]
    def __init__(self, batch_name):
        # Source: https://stackoverflow.com/a/3220762
        # The game agent will be run from SerpentAI\plugins. However, it needs
        # to be able to access roa.ini, which is located in capstone\plugins.
        plugins_path = os.path.join(os.path.dirname('..'), os.readlink('..'))
        ini_path = os.path.join(plugins_path, '..', 'scripts', 'roa.ini')
        config = configparser.ConfigParser()
        config.read(ini_path)

        self.replays_path = config['RivalsofAether']['PathToReplays']
        self.batch_path = os.path.join(self.replays_path, batch_name)
        self.batch = [
            dirent for dirent in os.listdir(self.batch_path)
            if dirent.endswith('.roa')
            ]

    def replace_current_replay(target_replay_name):
        # Remove any existing replay files from the game's replays folder
        for dirent in os.listdir(self.replays_path):
            if dirent.endswith('.roa'):
                dirent_path = os.path.join(self.replays_path, dirent)
                os.remove(dirent_path)
        # Copy the specified replay file to the game's replays folder
        target_replay_path = os.path.join(self.batch_path, replay_name)
        shutil.copy(target_replay_path, self.replays_path)
