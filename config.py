#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from multiprocessing import Process
import manage
import pipes
import datetime

def start_pipes(server):
    print("started at", datetime.datetime.now())
    pipes.init()
    process = Process(target=manage.socket_server, args=(pipes.pipe_child, pipes.pipe_throttle_child))
    process.start()
    print("ended at", datetime.datetime.now())

# Server Hooks

on_starting = start_pipes