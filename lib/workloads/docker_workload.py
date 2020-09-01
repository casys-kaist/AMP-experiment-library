#!/usr/bin/env python3

"""
   docker_workload.py

    Created on: Nov. 25, 2018
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import random
import string
from lib.workloads.remote_commander import *

class docker_workload(remote_commander):
    name = None
    container_id_li = None
    cgroup_li = None

    def __init__(self, ssh_client, name):
        self.name = name
        remote_commander.__init__(self, ssh_client)

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def get_container_id_li(self, image_name=None, container_name=None):
        """Returns the list of docker IDs which are created on container start"""
        if image_name == None:
            assert self.container_id_li != None
            return self.container_id_li
        else:
            if container_name != None:
                cmd = "docker ps -f ancestor='%s' -a --no-trunc | grep %s | cut -d' ' -f 1" % (image_name, container_name)
            else:
                cmd = "docker ps -f ancestor='%s' -a --no-trunc | cut -d' ' -f 1 | sed -n '1!p' | tr '\\n' ','" % (image_name)
            while True:
                try:
                    stdoutlines, stderrlines = self.exec_command_block(cmd)
                    if len(stdoutlines) >= 64:
                        if "," in stdoutlines:
                            container_id_li = stdoutlines.split(",")
                            if len(container_id_li) > 0:
                                container_id_li = container_id_li[:-1]
                                break
                        else:
                            container_id_li = [stdoutlines.strip()]
                            break
                except:
                    pass
        return container_id_li

    def get_container_id_from_container_name(self, container_name):
        cmd = "docker ps -f name=\"%s\" -a --no-trunc | cut -d' ' -f 1 | sed -n '1!p'" % (container_name)
        stdoutlines, stderrlines = self.exec_command_block(cmd)
        container_id = stdoutlines.strip()
        return container_id

    def get_cgroup_li(self):
        """Returns the list of cgroup ids"""
        assert self.cgroup_li != None
        return self.cgroup_li

    def create(self):
        """Create containers, required volumes, and network"""
        pass

    def run(self):
        """Run workloads"""
        pass
