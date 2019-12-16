#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import socket
import sys
import time
from multiprocessing import Process

import pipes

PORT = 27719
#IP = '192.168.0.104'


def socket_server(pipe, pipe_throttle):
    print('socket server is set up and running')
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', PORT))
            s.listen(5)
            while True:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    try:
                        while True:
                            data = pipe.recv()
                            print(data)
                            conn.send(len(data).to_bytes(4, byteorder='big'))
                            conn.send(data)
                            throttle = int.from_bytes(conn.recv(4), byteorder='big')
                            pipe_throttle.send(throttle)
                    except ConnectionError as e:
                        conn.close()
                        pipe_throttle.send(0)
                        print(e.errno)
    except Exception as e:
        time.sleep(1)
        print(e)
        socket_server(pipe, pipe_throttle)
        print('oops')

def main_():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'robot.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    pipes.init()
    process = Process(target=socket_server, args=(pipes.pipe_child, pipes.pipe_throttle_child))
    process.start()
    main_()
