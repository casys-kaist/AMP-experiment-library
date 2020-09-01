#!/usr/bin/env python3

"""
   npb.py

    Created on: May. 29, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import time
from lib.workloads.cgroup import *
from lib.workloads.docker_workload import *

class npb(docker_workload):
    docker_image_name = "npb"
    container_name = None
    container_id = None

    def __init__(self, ssh_client, name):
        docker_workload.__init__(self, ssh_client, name)

    def create(self):
        self.container_name = self.id_generator()
        cmd = "docker run"\
                " --name %s -t -d %s"\
                % (self.container_name, self.docker_image_name)
        self.exec_command_block(cmd)

        self.container_id_li = self.get_container_id_li(self.docker_image_name, self.container_name)
        assert len(self.container_id_li) == 1
        self.container_id = self.container_id_li[0]
        self.cgroup_li = [cgroup(self.ssh_client, self.container_id)]

    def run(self):
        start_time = time.time()
        cmd = "/usr/bin/time docker exec %s /root/NPB3.4/NPB3.4-OMP/bin/%s"\
                % (self.container_name, self.name)
        stdin, stdout, stderr = self.exec_command_nonblock(cmd)
        return { "channel": (stdin, stdout, stderr), "start_time": start_time }
