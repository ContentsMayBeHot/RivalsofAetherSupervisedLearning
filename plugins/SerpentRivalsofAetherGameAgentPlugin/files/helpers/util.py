import configparser
import os
import re

FRAMES_PER_SECOND = 60.0

def get_ini_path():
    # Source: https://stackoverflow.com/a/3220762
    # The game agent will be run from SerpentAI\plugins. However, it needs
    # to be able to access roa.ini, which is located in capstone\plugins.
    plugins_path_relative = os.path.join('..', '..', '..')
    plugins_path = os.path.join(os.path.dirname(plugins_path_relative),
                                os.readlink(plugins_path_relative))
    return os.path.join(plugins_path, '..', 'scripts', 'roa.ini')

def read_replays_path(ini_path=None):
    if not ini_path:
        ini_path = get_ini_path()
    config = configparser.ConfigParser()
    config.read(ini_path)
    return config['RivalsofAether']['PathToReplays']

def get_version_names(replays_path=None):
    if not replays_path:
        replays_path = get_replays_path()
    p = re.compile('[0-9]{2}_[0-9]{2}_[0-9]{2}')
    return [ x for x in os.listdir(replays_path) if p.match(x) ]

class InputSequences:
    splash_to_main = [1.5, 'Z', 'X', 'Z', 'Z', 'Z', 'Z']
    main_to_replay = [0.5, 'DOWN', 'DOWN', 'DOWN', 'Z', 1, 'Z']
    start_replay_1 = [1, 'Z', 'Z']
    back_and_forth = [1, 'X', 'Z']
