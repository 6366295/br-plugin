#!/usr/bin/env python2
# adb_helper.py

""" 
Author: 
    Mike Trieu

Last Update: 
    15 July 2018 

"""

from subprocess import call, Popen, PIPE

class ADBHelper():
    """ Class for calling ADB related functions """

    __logger = None

    adb_path = None

    def __init__(self, logger, adb_path="adb"):
        self.__logger = logger

        self.adb_path = adb_path

    def install(self, apk):
        self.__logger.info('Installing %s:' % apk)

        call([self.adb_path, "install", "-r", apk])

    def uninstall(self, package):
        self.__logger.info('Uninstalling %s:' % package)

        call([self.adb_path, "shell", "pm", "uninstall", "-k", package])

    def start_activity(self, activity):
        self.__logger.info('Starting Activity: %s' % activity)

        call([self.adb_path, "shell", "am", "start", "-a", "android.intent.action.MAIN", "-n", activity])

    def send_broadcast(self, action, extra, component):
        self.__logger.info(
            'Sending broadcast containing IntentDescription'
        )

        call([self.adb_path, "shell", "am", "broadcast", "-a", action, "--es", "'IntentDescription'", extra, "-n", "'" + component + "'"])

    def clear_logcat(self):
        """ Clear Logcat for a clean slate """

        call([self.adb_path, "logcat", "-c"])

    def enable_logcat_tag(self, tag):
        """ Enable logging of tag in Logcat """

        call([self.adb_path, "shell", "setprop", "log.tag." + tag, "VERBOSE"])

    def read_logcat_tag(self, tag):
        """ Check Logcat for logs with tag """

        output = Popen([self.adb_path, "logcat", "-d", "-s", "MyBroadcastReceiver"], stdout=PIPE)

        return output.communicate()[0]

    def log_cpu_usage(self, package):
        """ Check CPU usage of a process using top """

        output = Popen([self.adb_path, "shell", "top", "-n", "1"], stdout=PIPE)
        output = Popen(["grep", "-w", package], stdin=output.stdout, stdout=PIPE)

        return output.communicate()[0]

    def log_mem_usage(self, package):
        """ Check memory usage of a process using dumpsys meminfo """

        output = Popen([self.adb_path, "shell", "dumpsys", "meminfo", package], stdout=PIPE)
        
        return output.communicate()[0]