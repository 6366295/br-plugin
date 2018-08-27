#!/usr/bin/env python2
# output_helper.py

""" 
Author: 
    Mike Trieu

Last Update: 
    15 July 2018 

"""

from csv import DictWriter
from os.path import isdir
from os import mkdir
from sys import exit

class OutputHelper():
    """ Class for input output related functions """

    __logger = None
    __filename = None
    __fieldnames = None
    __output_path = None

    def __init__(self, output_path, datetime, logger):
        self.__logger = logger
        self.__output_path = output_path

        self.__fieldnames = [
            'Execution Time (ms)', 
            'Average CPU Usage (%)',
            'Average Memory Usage (kB)'
        ]
        
        self.__filename = '%s.csv' % datetime

        """ Create Output directory is it does not exist """

        if isdir(self.__output_path + '/brplugin_output') == False:
            self.__logger.info('Creating \'brplugin_output\' directory')

            mkdir(self.__output_path + '/brplugin_output')

        self.create_file_for_writing()

    def create_file_for_writing(self):
        self.__logger.info('Creating %s for writing' % self.__filename)

        with open('%s/brplugin_output/%s' % (self.__output_path, self.__filename), 'w') as csv_file:
            writer = DictWriter(csv_file,
                                fieldnames = self.__fieldnames)
            writer.writeheader()

    def write_file(self, *arg):
        if len(arg) != len(self.__fieldnames):
            self.__logger.error(
                'Arguments length does not match fieldnames'
            )

            exit()
        else:
            with open('%s/brplugin_output/%s' % (self.__output_path, self.__filename), 'a') as csv_file:
                writer = DictWriter(csv_file, 
                                    fieldnames = self.__fieldnames)

                self.__logger.info('Writing entry to %s' % 
                                   self.__filename)

                writer.writerow({
                    'Execution Time (ms)' : arg[0], 
                    'Average CPU Usage (%)' : arg[1], 
                    'Average Memory Usage (kB)': arg[2]
                })