#!/usr/bin/env python3

"""
   cgroup.py

    Created on: Nov. 22, 2018
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

from lib.workloads.remote_commander import *

class cgroup(remote_commander):
    cgroup_path = None
    procs = []

    def __init__(self, ssh_client, container_id):
        remote_commander.__init__(self, ssh_client)
        self.cgroup_path = "/sys/fs/cgroup/memory/docker/%s" % (container_id)

    def set_int(self, filename, val, validate=True):
        cmd = "echo %d > /%s/%s" % (val, self.cgroup_path, filename)
        while True:
            self.exec_command_block(cmd)
            if not validate:
                break
            elif validate:
                if self.get_int(filename) == val:
                    break

    def get_int(self, filename, max_retry=10):
        num_retry = 0
        cmd = "cat /%s/%s" % (self.cgroup_path, filename)
        while True:
            try:
                stdoutlines, stderrlines = self.exec_command_block(cmd)
                return int(stdoutlines.strip())
                break
            except:
                pass
            num_retry += 1
            if num_retry > max_retry:
                break
        return None

    def set_str(self, filename, val):
        cmd = "echo %s > /%s/%s" % (val, self.cgroup_path, filename)
        stdoutlines, stderrlines = self.exec_command_block(cmd)
        return stdoutlines

    def get_str(self, filename):
        cmd = "cat /%s/%s" % (self.cgroup_path, filename)
        stdoutlines, stderrlines = self.exec_command_block(cmd)
        return stdoutlines
