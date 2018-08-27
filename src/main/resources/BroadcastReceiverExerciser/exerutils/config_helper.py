#!/usr/bin/env python2
# config_helper.py

""" 
Author: 
    Mike Trieu

Last Update: 
    15 July 2018 

"""

from json import load, dumps
from re import escape
from sys import exit

class ConfigHelper():
    """ Class for loading the configuration JSON """

    __logger = None

    __config_file = None

    __adb_path = None
    __input_apk = None
    __package = None
    __activity = None

    __intent_description = None

    __delay = None
    __reps = None

    def __init__(self, config_file, logger):
        self.__logger = logger
        self.__config_file = config_file

        self.__logger.info('Loading Configuration')

        self.parse_data(self.__config_file)

    def parse_data(self, config_file):
        try:
            with open(config_file) as file:
                json_data = load(file)
        except IOError:
            self.__logger.error('Did not find a configuration file')

            exit()
        except ValueError:
            self.__logger.error('JSON file format incorrect')

            exit()

        try:
            self.__adb_path = json_data["Configuration"]["ADBPath"]
            self.__input_apk = json_data["Configuration"]["APK"]
            self.__package = json_data["Configuration"]["Package"]
            self.__activity = json_data["Configuration"]["Activity"]

            self.__intent_description = json_data["IntentDescription"]

            self.__delay = json_data["Configuration"]["Delay"]
            self.__reps = json_data["Configuration"]["Repetitions"]
        except KeyError as e:
            self.__logger.error('Keyerror: %s does not exist', (e))

            exit()

    def read_file(self, config_file):
        with open(config_file) as file:
            return file.read()

    def get_adb_path(self):
        return self.__adb_path

    def get_input_apk(self):
        return self.__input_apk

    def get_package(self):
        return self.__package

    def get_activity(self):
        return self.__activity

    def get_intent_description(self):
        return escape(dumps(self.__intent_description))

    def get_delay(self):
        return self.__delay

    def get_repetitions(self):
        return self.__reps