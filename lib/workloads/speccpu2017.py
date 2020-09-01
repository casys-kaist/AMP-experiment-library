#!/usr/bin/env python3

"""
   speccpu2017.py

    Created on: Nov. 25, 2018
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import time
from lib.workloads.cgroup import *
from lib.workloads.docker_workload import *

class speccpu2017(docker_workload):
    docker_image_name = "speccpu2017"
    container_name = None
    container_id = None

    def __init__(self, ssh_client, name):
        docker_workload.__init__(self, ssh_client, name)

    def create(self):
        self.container_name = self.id_generator()
        cmd = "docker run --ulimit stack=128849018880:128849018880"\
                " --name %s -t -d %s"\
                % (self.container_name, self.docker_image_name)
        self.exec_command_block(cmd)

        self.container_id_li = self.get_container_id_li(self.docker_image_name, self.container_name)
        assert len(self.container_id_li) == 1
        self.container_id = self.container_id_li[0]
        self.cgroup_li = [cgroup(self.ssh_client, self.container_id)]

    def run(self, dataset="ref", threads=1):
        start_time = time.time()
        cmd = "/usr/bin/time docker exec %s /root/speccpu2017/bin/runcpu %s --size=%s --threads=%d"\
                % (self.container_name, self.name, dataset, threads)
        stdin, stdout, stderr = self.exec_command_nonblock(cmd)
        return { "channel": (stdin, stdout, stderr), "start_time": start_time }
