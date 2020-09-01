#!/usr/bin/env python3

"""
   stats.py

    Created on: Jul. 16, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

def record_std(std, stdfile):
    filename = stdfile.name
    if "stdout.txt" in filename:
        stdout = std
        if stdout.channel.recv_ready():
            line = stdout.channel.recv(32768).decode("utf-8")
            stdfile.write(line)
    elif "stderr.txt" in filename:
        stderr = std
        if stderr.channel.recv_stderr_ready():
            line = stderr.channel.recv_stderr(32768).decode("utf-8")
            stdfile.write(line)

def exit_condition(stdout):
    return stdout.channel.exit_status_ready()

def record_stats_per_cgroup(result_dir, signature, cgroup_li, stat_name):
    for idx, cgroup in enumerate(cgroup_li):
        with open("%s/%s_%d.%s.txt" % (result_dir, signature, idx, stat_name), "a") as f:
            f.write(cgroup.get_str(stat_name))
