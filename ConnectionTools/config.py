##################################################
# File: Config.py
#
# This file manages the configuration file for the bot
# A function is provided to load an INI file into a global variable which can then be accessed by other libraries
##################################################
# Version: 1.00
# Date:    25 May 2021
##################################################

# why import configparser
import configparser

# Global variable to hold bot confiuration options
config = configparser.ConfigParser(allow_no_value=True)

# describe function here


def load_configuration(config_file):
    print("Loading system configuration -", config_file)
    config.read(config_file)
