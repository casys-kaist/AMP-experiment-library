#!/usr/bin/env python3

"""
   page_hotness_tracking_overhead_synthetic_bench.py

    Created on: Sep. 7, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import time
from lib.workloads.docker_workload import *
from lib.workloads.cgroup import *

class page_hotness_tracking_overhead_synthetic_bench(docker_workload):
    docker_image_name = "page_hotness_tracking_overhead_synthetic_bench"
    container_name = None
    container_id = None

    def __init__(self, ssh_client, name):
        docker_workload.__init__(self, ssh_client, name)

    def create(self):
        self.container_name = self.id_generator()
        cmd = "docker run --name %s -t -d %s" % (self.container_name, self.docker_image_name)
        self.exec_command_block(cmd)

        self.container_id_li = self.get_container_id_li(self.docker_image_name, self.container_name)
        assert len(self.container_id_li) == 1
        self.container_id = self.container_id_li[0]
        self.cgroup_li = [cgroup(self.ssh_client, self.container_id)]

    def run(self):
        splitted_name = self.name.split(":")
        workload_name = splitted_name[0]
        cmd = "/usr/bin/time docker exec -t %s /root/src/mem_alloc_seq_access %d"\
                % (self.container_name, int(splitted_name[1]))
        start_time = time.time()
        stdin, stdout, stderr = self.exec_command_nonblock(cmd)
        return { "channel": (stdin, stdout, stderr), "start_time": start_time }
