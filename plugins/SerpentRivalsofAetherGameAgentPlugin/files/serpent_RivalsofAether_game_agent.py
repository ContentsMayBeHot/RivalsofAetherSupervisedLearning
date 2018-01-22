from serpent.game_agent import GameAgent
from serpent.input_controller import KeyboardKey

from serpent.frame_grabber import FrameGrabber
from serpent.input_controller import KeyboardKey

import configparser
import os

class ReplayManager:
    def __init__(self, version):
        self.version = version
        self.batch = []
        for dirent in os.listdir(version):
            if dirent.endswith('.roa'):
                self.batch.append(dirent)

class SerpentRivalsofAetherGameAgent(GameAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frame_handlers["PLAY"] = self.handle_play
        self.frame_handler_setups["PLAY"] = self.setup_play
        self.analytics_client = None

    def setup_play(self):
        # Source: https://stackoverflow.com/a/3220762
        # The game agent will be run from SerpentAI\plugins. However, it needs
        # to be able to access roa.ini, which is located in capstone\plugins.
        plugins = os.path.join(os.path.dirname('..'), os.readlink('..'))
        ini_path = os.path.join(plugins, '..', 'scripts', 'roa.ini')
        config = configparser.ConfigParser()
        config.read(ini_path)
        self.fq_replays = config['RivalsofAether']['PathToReplays']

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
