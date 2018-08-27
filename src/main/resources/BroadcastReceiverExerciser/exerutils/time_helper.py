#!/usr/bin/env python2
# output_helper.py

""" 
Author: 
    Mike Trieu

Last Update: 
    15 July 2018 

"""

from datetime import datetime
from time import time, sleep

class TimeHelper():
    """ Class for time and date related functions """

    __datetime = None
    __logger = None

    __start = {}

    def __init__(self, logger):
        """ Set time stamp when class is first created """

        self.__logger = logger

        self.__datetime = datetime.fromtimestamp(time()).\
                          strftime('%Y-%m-%d_%H:%M:%S')

    def sleep(self, seconds):
        sleep(seconds)

    def get_datetime(self):
        """ Getter for datetime """

        return self.__datetime
        
    def start_time(self, tag):
        """ Set a tag and start time of execution time measurement """

        self.__start[tag] = time()

    def end_time(self, tag):
        """ Set end time and calculate elapsed time """

        end = time()

        try:
            elapsed_time = end - self.__start[tag]
            
            self.__start.pop(tag, None)

            self.__logger.info('%s: Executed %s seconds' % 
                               (tag, elapsed_time))
        except KeyError:
            self.__logger.warning('No start time found!')