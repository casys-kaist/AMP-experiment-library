#!/usr/bin/env python3

"""
   sysfs.py

    Created on: Sep. 20, 2018
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

from lib.workloads.remote_commander import *

class sysfs(remote_commander):
    def __init__(self, ssh_client, sysfs_path):
        self.sysfs_path = sysfs_path
        remote_commander.__init__(self, ssh_client)

    def set_int(self, filename, val):
        cmd = "echo %d > /%s/%s" % (val, self.sysfs_path, filename)
        stdoutlines, stderrlines = self.exec_command_block(cmd)
        return stdoutlines

    def get_int(self, filename):
        cmd = "cat /%s/%s" % (self.sysfs_path, filename)
        stdoutlines, stderrlines = self.exec_command_block(cmd)
        return int(stdoutlines.strip())

    def set_str(self, filename, val):
        cmd = "echo %s > /%s/%s" % (val, self.sysfs_path, filename)
        stdoutlines, stderrlines = self.exec_command_block(cmd)
        return stdoutlines

    def get_str(self, filename):
        cmd = "cat /%s/%s" % (self.sysfs_path, filename)
        stdoutlines, stderrlines = self.exec_command_block(cmd)
        return stdoutlines
