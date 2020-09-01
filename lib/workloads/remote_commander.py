#!/usr/bin/env python3

"""
   remote_commander.py

    Created on: Nov. 23, 2018
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import paramiko

class remote_commander:
    ssh_client = None

    def __init__(self, ssh_client):
        self.ssh_client = ssh_client

    def exec_command_nonblock(self, cmd):
        print(cmd)
        return self.ssh_client.exec_command(cmd)

    def exec_command_block(self, cmd):
        print(cmd)
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        stdout.channel.recv_exit_status()
        stdout_lines = "".join(stdout.readlines())
        stderr_lines = "".join(stderr.readlines())
        return stdout_lines, stderr_lines
