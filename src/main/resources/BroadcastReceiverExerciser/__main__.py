#!/usr/bin/env python2
# __main__.py

""" 
Author: 
    Mike Trieu

Last Update: 
    15 July 2018 

"""

from exerutils.adb_helper import ADBHelper
from exerutils.config_helper import ConfigHelper
from exerutils.output_helper import OutputHelper
from exerutils.sampler import SamplerProcess
from exerutils.time_helper import TimeHelper

import logging
import argparse
import re

from numpy import mean
from os.path import dirname, abspath
from os import chdir

def init_logger():
    logger = logging.getLogger('BRExerciser')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger

def setup_br_trigger(adb, plugin_path, logger):
    # br_trigger_apk = "/home/mt/Thesis/ToolChain/BroadcastReceiverTrigger/app/build/outputs/apk/debug/app-debug.apk"
    br_trigger_apk = plugin_path + "/brtrigger.apk"

    logger.info('Setup BroadcastReceiverTrigger')

    adb.install(br_trigger_apk)
    adb.start_activity(
        "vu.thesis.mike.broadcastreceivertrigger/.MainActivity"
    )

def setup_input_apk(adb, config, logger):
    logger.info('Setup BroadcastReceiverTrigger')

    adb.install(config.get_input_apk())

    adb.start_activity('%s/.%s' % 
                      (config.get_package(), config.get_activity()))

def process_cpu_samples(raw_cpu_samples):
    cpu_usage_array = []

    for i in range(len(raw_cpu_samples)):
        """ Sometimes it does not find a top entry """

        try:
            cpu_usage_array.append(
                raw_cpu_samples[i].split()[4].split("%")[0]
            )
        except IndexError:
            continue

    return mean(map(float, cpu_usage_array))

def process_mem_samples(raw_mem_samples):
    mem_usage_array = []

    for i in range(len(raw_mem_samples)):
        try:
            mem_usage_array.append(
                re.findall("TOTAL(.*)", raw_mem_samples[i])[0].split()[0]
            )
        except IndexError:
            continue

    return mean(map(float, mem_usage_array))

def main():
    parser = argparse.ArgumentParser(description='Config and output destinations')
    parser.add_argument('config_file')
    parser.add_argument('output_path')
    parser.add_argument('plugin_path')

    arguments = vars(parser.parse_args())

    # chdir(dirname(abspath(__file__)))

    logger = init_logger()

    logger.info('Initializing BroadcastReceiverExerciser')

    time = TimeHelper(logger)

    # config = ConfigHelper('configuration.json', logger)
    config = ConfigHelper(arguments['config_file'], logger)

    output = OutputHelper(arguments['output_path'], time.get_datetime(), logger)

    adb = ADBHelper(logger, config.get_adb_path())

    adb.clear_logcat()
    adb.enable_logcat_tag("MyBroadcastReceiver")

    cpu_sampler = SamplerProcess(
        adb.log_cpu_usage, 
        config.get_package(),
        config.get_delay(),
        logger
    )

    mem_sampler = SamplerProcess(
        adb.log_mem_usage, 
        config.get_package(), 
        config.get_delay(),
        logger
    )

    setup_br_trigger(adb, arguments['plugin_path'], logger)

    setup_input_apk(adb, config, logger)

    cpu_sampler.start_process()
    mem_sampler.start_process()

    time.sleep(5)

    prev_execution_time = 0

    for i in range(config.get_repetitions()):
        adb.send_broadcast(
            "vu.thesis.mike.broadcastreceivertrigger.IntentDescriptionBroadcastReceiver", 
            config.get_intent_description(), 
            "vu.thesis.mike.broadcastreceivertrigger/.IntentDescriptionBroadcastReceiver"
        )

        time.start_time('adb.sendBroadcast')

        """ 
        Check when target BroadcastReceiver finished executing, 
        by checking the Timelogger measurements on Logcat 

        """

        while(1):
            logs = adb.read_logcat_tag('MyBroadcastReceiver')

            execution_time = re.findall("end, (.*) ms", logs)

            if (len(execution_time) > 0):
                time.end_time('adb.sendBroadcast')

                cpu_sampler.pause_process()
                mem_sampler.pause_process()

                # prev_execution_time = len(execution_time)

                output.write_file(
                    execution_time[-1], 
                    process_cpu_samples(cpu_sampler.read_queue()), 
                    process_mem_samples(mem_sampler.read_queue())
                )

                adb.clear_logcat()

                break

            time.sleep(0.001)

        cpu_sampler.continue_process()
        mem_sampler.continue_process()

        """ Delay between each repetition """
        logger.info('Sleeping for %s seconds', config.get_delay())
        time.sleep(config.get_delay())

    cpu_sampler.stop_process()
    mem_sampler.stop_process()

    adb.uninstall('vu.thesis.mike.broadcastreceivertrigger')
    adb.uninstall(config.get_package())


if __name__ == "__main__":
    main()