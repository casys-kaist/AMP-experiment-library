#!/usr/bin/env python3

"""
   page_migration_policy_preference_synthetic_bench.py

    Created on: Dec. 8, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import time
from lib.workloads.docker_workload import *
from lib.workloads.cgroup import *

class page_migration_policy_preference_synthetic_bench(docker_workload):
    docker_image_name = "page_migration_policy_preference_synthetic_bench"
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
        if "mix" in workload_name:
            return self.run_mix()
        elif "lru_favor" == workload_name:
            return self.run_lru_favor()
        elif "lfu_favor" == workload_name:
            return self.run_lfu_favor()
        elif "random_favor" == workload_name:
            return self.run_random_favor()

    def run_mix(self):
        splitted_name = self.name.split("mix+")
        cmd = "/usr/bin/time docker exec -t %s python3 /root/src/mix.py %s"\
                % (self.container_name, splitted_name[1])
        print(cmd)
        start_time = time.time()
        stdin, stdout, stderr = self.exec_command_nonblock(cmd)
        return { "channel": (stdin, stdout, stderr), "start_time": start_time }

    def run_lru_favor(self):
        splitted_name = self.name.split(":")
        num_pages = int(splitted_name[1])
        num_working_set_partitions = int(splitted_name[2])
        working_set_access_duration = int(splitted_name[3])
        num_iterations = int(splitted_name[4])
        cmd = "/usr/bin/time docker exec -t %s /root/src/lru_favor "\
                "--num_pages %d "\
                "--num_working_set_partitions %d "\
                "--working_set_access_duration %d "\
                "--num_iterations %d"\
                % (self.container_name,
                        num_pages,
                        num_working_set_partitions,
                        working_set_access_duration,
                        num_iterations)
        print(cmd)
        start_time = time.time()
        stdin, stdout, stderr = self.exec_command_nonblock(cmd)
        return { "channel": (stdin, stdout, stderr), "start_time": start_time }

    def run_lfu_favor(self):
        splitted_name = self.name.split(":")
        num_pages = int(splitted_name[1])
        hot_working_set_ratio = float(splitted_name[2])
        num_iterations = int(splitted_name[3])
        cmd = "/usr/bin/time docker exec -t %s /root/src/lfu_favor "\
                "--num_pages %d "\
                "--hot_working_set_ratio %f "\
                "--num_iterations %d"\
                % (self.container_name,
                        num_pages,
                        hot_working_set_ratio,
                        num_iterations)
        print(cmd)
        start_time = time.time()
        stdin, stdout, stderr = self.exec_command_nonblock(cmd)
        return { "channel": (stdin, stdout, stderr), "start_time": start_time }

    def run_random_favor(self):
        splitted_name = self.name.split(":")
        num_pages = int(splitted_name[1])
        num_iterations = int(splitted_name[2])
        cmd = "/usr/bin/time docker exec -t %s /root/src/random_favor "\
                "--num_pages %d --num_iterations %d"\
                % (self.container_name, num_pages, num_iterations)
        print(cmd)
        start_time = time.time()
        stdin, stdout, stderr = self.exec_command_nonblock(cmd)
        return { "channel": (stdin, stdout, stderr), "start_time": start_time }
