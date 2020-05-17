import configparser

config = configparser.ConfigParser()
config.read('config.ini')

PORTS = config['PORTS']
ROM = config['ROM']
STATE = config['STATE']
TWITCH = config['TWITCH']
