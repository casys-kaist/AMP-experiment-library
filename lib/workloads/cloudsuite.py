#!/usr/bin/env python3

"""
   cloudsuite.py

    Created on: Sep. 20, 2018
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import time
from lib.workloads.docker_workload import *
from lib.workloads.cgroup import *

class cloudsuite(docker_workload):
    def __init__(self, ssh_client, name):
        docker_workload.__init__(self, ssh_client, name)

    def create(self):
        if "graph-analytics" in self.name:
            return self.create_graph_analytics()
        elif "in-memory-analytics" in self.name:
            return self.create_in_memory_analytics()

    def run(self):
        if "graph-analytics" in self.name:
            return self.run_graph_analytics()
        elif "in-memory-analytics" in self.name:
            return self.run_in_memory_analytics()

    def create_graph_analytics(self):
        # create dataset container
        cmd = "docker create --name data cloudsuite/twitter-dataset-graph"
        self.exec_command_block(cmd)

        # create graph analytics container
        cmd = "docker run"\
            + " --volumes-from data"\
            + " --name graph-analytics -t -d cloudsuite/graph-analytics"
        self.exec_command_block(cmd)

        # update cgroup_li
        self.container_id_li = self.get_container_id_li("cloudsuite/graph-analytics")
        self.cgroup_li = []
        for container_id in self.container_id_li:
            self.cgroup_li.append(cgroup(self.ssh_client, container_id))

    def run_graph_analytics(self):
        driver_memory_size = int(self.name.split(":")[1])
        executor_memory_size = int(self.name.split(":")[2])
        start_time = time.time()
        cmd = "/usr/bin/time docker exec graph-analytics /root/entrypoint.sh --driver-memory %dg --executor-memory %dg"\
                % (driver_memory_size, executor_memory_size)
        stdin, stdout, stderr = self.exec_command_nonblock(cmd)
        return { "channel": (stdin, stdout, stderr), "start_time": start_time }

    def create_in_memory_analytics(self):
        # create dataset container
        cmd = "docker create --name data cloudsuite/movielens-dataset"
        self.exec_command_block(cmd)

        # create in-memory analytics container
        cmd = "docker run "\
            + " --volumes-from data"\
            + " --name in-memory-analytics -t -d cloudsuite/in-memory-analytics"
        self.exec_command_block(cmd)

        # update cgroup_li
        self.container_id_li = self.get_container_id_li("cloudsuite/in-memory-analytics")
        assert len(self.container_id_li) == 1
        self.cgroup_li = []
        for container_id in self.container_id_li:
            self.cgroup_li.append(cgroup(self.ssh_client, container_id))

    def run_in_memory_analytics(self):
        driver_memory_size = int(self.name.split(":")[1])
        executor_memory_size = int(self.name.split(":")[2])
        start_time = time.time()
        cmd = "/usr/bin/time docker exec -t in-memory-analytics /root/entrypoint.sh /data/ml-latest /data/myratings.csv "\
                  "--driver-memory %dg --executor-memory %dg"\
                  % (driver_memory_size, executor_memory_size)
        stdin, stdout, stderr = self.exec_command_nonblock(cmd)
        return { "channel": (stdin, stdout, stderr), "start_time": start_time }
