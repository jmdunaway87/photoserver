import configparser, os

def get_config():

    config = configparser.ConfigParser()
    config.read_file(open('settings.ini'))
    return config

    