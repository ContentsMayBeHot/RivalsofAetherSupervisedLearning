from serpent.game_agent import GameAgent
from serpent.input_controller import KeyboardKey

from serpent.frame_grabber import FrameGrabber
from serpent.input_controller import KeyboardKey

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

class SerpentRivalsofAetherGameAgent(GameAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frame_handlers["PLAY"] = self.handle_play
        self.frame_handler_setups["PLAY"] = self.setup_play
        self.analytics_client = None

    def setup_play(self):
        input_mapping = {
            'Z': [KeyboardKey.KEY_Z],
            'X': [KeyboardKey.KEY_X],
            'C': [KeyboardKey.KEY_C],
            'D': [KeyboardKey.KEY_D],
            'S': [KeyboardKey.KEY_S],
            'UP': [KeyboardKey.KEY_UP],
            'DOWN': [KeyboardKey.KEY_DOWN],
            'LEFT': [KeyboardKey.KEY_LEFT],
            'RIGHT': [KeyboardKey.KEY_RIGHT]
        }
        self.key_mapping = {
            KeyboardKey.KEY_Z.name: 'JUMP',
            KeyboardKey.KEY_X.name: 'ATTACK',
            KeyboardKey.KEY_C.name: 'SPECIAL',
            KeyboardKey.KEY_D.name: 'STRONG',
            KeyboardKey.KEY_S.name: 'DODGE',
            KeyboardKey.KEY_UP.name: 'UP',
            KeyboardKey.KEY_DOWN.name: 'DOWN',
            KeyboardKey.KEY_LEFT.name: 'LEFT',
            KeyboardKey.KEY_RIGHT.name: 'RIGHT'
        }

    def handle_play(self, game_frame):
        for i, game_frame in enumerate(self.game_frame_buffer.frames):
            self.visual_debugger.store_image_data(
                game_frame.frame,
                game_frame.frame.shape,
                str(i)
            )
        game_frame_buffer
