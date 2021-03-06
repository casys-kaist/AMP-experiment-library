#!/usr/bin/env python3

"""
   exptools.py

    Created on: Apr. 11, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import datetime
import os
import paramiko

from lib.workloads.cloudsuite import *
from lib.workloads.graph500 import *
from lib.workloads.npb import *
from lib.workloads.speccpu2017 import *
from lib.workloads.page_migration_policy_preference_synthetic_bench import *
from lib.workloads.page_hotness_tracking_overhead_synthetic_bench import *

def get_ssh_client(ip, port, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ip, port, username, password)
    return ssh_client

def exec_command_block(ssh_client, cmd):
    print(cmd)
    stdin, stdout,stderr = ssh_client.exec_command(cmd)
    stdout.channel.recv_exit_status()
    stdoutlines = "".join(stdout.readlines())
    stderrlines = "".join(stderr.readlines())

def exec_command_nonblock(ssh_client, cmd):
    print(cmd)
    return ssh_client.exec_command(cmd)

def stop_all_containers(ssh_client):
    exec_command_block(ssh_client, "docker stop $(docker ps -a -q)")

def rm_all_containers(ssh_client):
    exec_command_block(ssh_client, "docker rm $(docker ps -a -q)")

def delete_dangling_volumes(ssh_client):
    exec_command_block(ssh_client, "docker volume ls -qf dangling=true | xargs -r docker volume rm")

def remove_networks(ssh_client):
    exec_command_block(ssh_client, "docker network rm $(docker network ls | grep 'bridge' | awk '/ / { print $1 }')")

def reset_docker(ssh_client):
    stop_all_containers(ssh_client)
    rm_all_containers(ssh_client)
    delete_dangling_volumes(ssh_client)
    remove_networks(ssh_client)

def setup_exp_directory(result_dir, expname):
    now = datetime.datetime.now()
    result_path = "/%s/%s-%s" % (result_dir, expname, now.strftime("%Y%m%d-%H%M%S"))
    os.makedirs(result_path)
    return result_path

def get_workload(ssh_client, workload_type, workload_name):
    if workload_type == "cloudsuite":
        workload = cloudsuite(ssh_client, workload_name)
    elif workload_type == "graph500":
        workload = graph500(ssh_client, workload_name)
    elif workload_type == "npb":
        workload = npb(ssh_client, workload_name)
    elif workload_type == "speccpu2017":
        workload = speccpu2017(ssh_client, workload_name)
    elif workload_type == "page_migration_policy_preference_synthetic_bench":
        workload = page_migration_policy_preference_synthetic_bench(ssh_client, workload_name)
    elif workload_type == "page_hotness_tracking_overhead_synthetic_bench":
        workload = page_hotness_tracking_overhead_synthetic_bench(ssh_client, workload_name)
    return workload

def pause_docker_process(ssh_client, container_id):
    cmd = "docker_process_pauser.py -container_id %s" % (container_id)
    print(cmd)
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    stdout.channel.recv_exit_status()
