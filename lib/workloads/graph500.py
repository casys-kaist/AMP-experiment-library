#!/usr/bin/env python3

"""
   graph500.py

    Created on: Dec. 22, 2018
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import time
from lib.workloads.cgroup import *
from lib.workloads.docker_workload import *

class graph500(docker_workload):
    docker_image_name = "graph500"
    container_name = None
    container_id = None

    def __init__(self, ssh_client, name):
        docker_workload.__init__(self, ssh_client, name)

    def create(self):
        self.container_name = self.id_generator()
        cmd = "docker run"\
                " --cpuset-cpus=\"`numactl --hardware | grep 'cpus' | grep 'node 0' | cut -d' ' -f4- | sed -e 's/ /,/g'`\""\
                " --name %s -t -d %s"\
                % (self.container_name, self.docker_image_name)
        self.exec_command_block(cmd)

        self.container_id_li = self.get_container_id_li(self.docker_image_name, self.container_name)
        assert len(self.container_id_li) == 1
        self.container_id = self.container_id_li[0]
        self.cgroup_li = [cgroup(self.ssh_client, self.container_id)]

    def run(self):
        splitted_name = self.name.split(":")
        scale = int(splitted_name[2])
        edge_factor = int(splitted_name[3])
        if "bfs" == splitted_name[1]:
            return self.run_graph500_bfs(scale, edge_factor)
        elif "sssp" == splitted_name[1]:
            return self.run_graph500_sssp(scale, edge_factor)

    def run_graph500_bfs(self, scale, edge_factor):
        return self.run_graph500("graph500_reference_bfs", scale, edge_factor)

    def run_graph500_sssp(self, scale, edge_factor):
        return self.run_graph500("graph500_reference_sssp", scale, edge_factor)

    def run_graph500(self, binary_name, scale, edge_factor):
        start_time = time.time()
        cmd = "/usr/bin/time docker exec -t %s /entrypoint.sh %s %d %d" % (self.container_name, binary_name, scale, edge_factor)
        stdin, stdout, stderr = self.exec_command_nonblock(cmd)
        return { "channel": (stdin, stdout, stderr), "start_time": start_time }
