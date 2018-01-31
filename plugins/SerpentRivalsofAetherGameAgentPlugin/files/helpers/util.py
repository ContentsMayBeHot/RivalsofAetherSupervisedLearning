def get_replays_path():
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

def get_version_names(replays_path=None):
    if not replays_path:
        replays_path = get_replays_path()
    p = re.compile('[0-9]{2}_[0-9]{2}_[0-9]{2}')
    return [ x for x in os.listdir(replays_path) if p.match(x) ]
