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

def time_to_seconds(time_str):
    elapsed_time = time_str.strip().split()[2].split("elapsed")[0]
    time_len = len(elapsed_time.split(":"))
    if time_len == 2: # min:sec
        elapsed_hour = 0
        elapsed_min = float(elapsed_time.split(":")[0])
        elapsed_sec = float(elapsed_time.split(":")[1])
    elif time_len == 3: # hour:min:sec
        elapsed_hour = float(elapsed_time.split(":")[0])
        elapsed_min = float(elapsed_time.split(":")[1])
        elapsed_sec = float(elapsed_time.split(":")[2])
    elapsed_seconds = elapsed_hour * 60 * 60 + elapsed_min * 60 + elapsed_sec
    return elapsed_seconds

speccpu2017_abbr_dict = {
            "605.mcf_s": "mcf",
            "631.deepsjeng_s": "deepsjeng",
            "603.bwaves_s": "bwaves",
            "607.cactuBSSN_s": "cactus",
            "619.lbm_s": "lbm",
            "628.pop2_s": "pop2",
        }

cloudsuite_abbr_dict = {
            "graph-analytics": "graph-analytics",
            "in-memory-analytics": "in-mem-analytics"
        }

others_abbr_dict = {
            "graph500:bfs:23:13": "graph500",
        }

def abbreviate_workload_name(workload_name):
    for abbr_dict in [speccpu2017_abbr_dict, cloudsuite_abbr_dict, others_abbr_dict]:
        if workload_name in abbr_dict.keys():
            return abbr_dict[workload_name]
    return workload_name
