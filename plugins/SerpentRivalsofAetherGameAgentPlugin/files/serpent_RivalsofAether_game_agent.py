from serpent.game_agent import GameAgent
from serpent.input_controller import KeyboardKey

from serpent.frame_grabber import FrameGrabber
from serpent.input_controller import KeyboardKey

#from .helpers.replay_management import ReplayManager, ReplayLoader
#from .helpers.util import get_replays_path, get_version_names
from .helpers.util import InputSequences as inseq

import datetime
import time

class SerpentRivalsofAetherGameAgent(GameAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frame_handlers["PLAY"] = self.handle_play
        self.frame_handlers["COLLECT"] = self.handle_collect
        self.frame_handler_setups["PLAY"] = self.setup_play
        self.frame_handler_setups["COLLECT"] = self.setup_collect
        self.analytics_client = None

    def setup_common(self):
        self.input_mapping = {
            'Z': KeyboardKey.KEY_Z,
            'X': KeyboardKey.KEY_X,
            'C': KeyboardKey.KEY_C,
            'D': KeyboardKey.KEY_D,
            'S': KeyboardKey.KEY_S,
            'UP': KeyboardKey.KEY_UP,
            'DOWN': KeyboardKey.KEY_DOWN,
            'LEFT': KeyboardKey.KEY_LEFT,
            'RIGHT': KeyboardKey.KEY_RIGHT
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

    def setup_play(self):
        self.setup_common()

    def setup_collect(self):
        self.setup_common()

    def handle_play(self, game_frame):
        print('Hellow')

    def handle_collect(self, game_frame):
        self.tap_sequence(inseq.splash_to_main)
        self.tap_sequence(inseq.main_to_replay)
        self.tap_sequence(inseq.start_replay_1)
        print('Done')
        quit()

    def tap_sequence(self, sequence, delay_override=None):
        # Must contain delay value and one input/wait token
        if len(sequence) < 2:
            return

        # Retrieve delay value
        delay = sequence[0]
        if delay_override:
            delay = delay_override

        # Read the rest of the sequence
        for token in sequence[1:]:
            if isinstance(token, str):
                mapped_input = self.input_mapping[token.upper()]
                self.input_controller.tap_key(mapped_input)
                time.sleep(delay)
            elif isinstance(token, int):
                time.sleep(token)
