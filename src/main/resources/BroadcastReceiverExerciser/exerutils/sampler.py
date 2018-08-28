#!/usr/bin/env python2
# sampler.py

""" 
Author: 
    Mike Trieu

Last Update: 
    21 June 2018 

"""

from multiprocessing import Process, Queue
from subprocess import call, Popen, PIPE
from time import sleep

class SamplerProcess():
    """ Class sampling asynchronously """

    __logger = None
    
    __read_queue = None
    __write_queue = None

    __name = None
    __delay = None
    __process = None

    def __init__(self, sampling_code, package, delay, logger):
        """ Initialize process """

        self.__logger = logger
        self.__name = sampling_code.__name__
        self.__delay = delay

        self.__logger.info('Initializing %s process' % self.__name)

        self.__read_queue = Queue()
        self.__write_queue = Queue()

        self.__process = Process(target=self.sampler, args=(
            sampling_code, 
            package, 
            self.__read_queue, 
            self.__write_queue)
        )

    def start_process(self):
        self.__logger.info('Starting %s process' % self.__name)

        self.__process.start()

    def stop_process(self):
        self.__logger.info('Stopping %s process' % self.__name)

        self.__process.terminate()
        self.__process.join()

    def pause_process(self):
        self.__logger.info('Pausing %s process' % self.__name)

        self.__read_queue.put('pause')

    def continue_process(self):
        # self.__logger.info('Continuing %s process' % self.__name)

        self.__read_queue.put('cont')

    def read_queue(self):
        return self.__write_queue.get()

    def sampler(self, sampling_code, package, read_queue, write_queue):
        """ Sample """

        samples = []

        sleep(5)

        while(1):
            if read_queue.empty():
                samples.append(sampling_code(package))

                sleep(0.001)
            else:
                read_queue.get()

                write_queue.put(samples)

                samples = []

                if ((read_queue.get() == "cont")):
                    sleep(self.__delay)

                    self.__logger.info('Continuing %s process' % self.__name)

                    continue