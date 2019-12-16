import errno
import json
import operator as op
import socket
import sys
import time
from functools import reduce

import RPi.GPIO as GPIO
from select import select


def enable_motors(l_en, r_en):
    global l_enable, r_enable
    l_enable, r_enable = l_en, r_en
    left_motor.ChangeDutyCycle(throttle * l_en)
    right_motor.ChangeDutyCycle(throttle * r_en)


def mul(iterable):
    return reduce(op.mul, iterable, 1)


HOST = 'l1va-mobile-platform.herokuapp.com'  # The server's hostname or IP address
PORT = 27719  # The port used by the server

throttle = 0
prev_throttle = 0

left_dir = 8
left_pwm = 10
right_dir = 12
right_pwm = 16
turret_dir = 18
turret_pwm = 22

l_enable = 0
r_enable = 0

all_keys = {'up', 'down', 'left', 'right'}

forward = {'up'}
l_forward = {'up', 'left'}
r_forward = {'up', 'right'}
backward = {'down'}
l_backward = {'down', 'left'}
r_backward = {'down', 'right'}
l_force = {'left'}
r_force = {'right'}
throttle_up = 'shift'
throttle_down = 'ctrl'

GPIO.setmode(GPIO.BOARD)
GPIO.setup([left_dir, left_pwm, right_dir, right_pwm, turret_dir, turret_pwm], GPIO.OUT, initial=GPIO.LOW)

left_motor = GPIO.PWM(left_pwm, 200)
right_motor = GPIO.PWM(right_pwm, 200)

left_motor.start(0)
right_motor.start(0)

GPIO.setup([left_dir, left_pwm, right_dir, right_pwm, turret_dir, turret_pwm], GPIO.OUT, initial=GPIO.LOW)

keys = {'up': False,
        'down': False,
        'left': False,
        'right': False,
        'shift': False,
        'ctrl': False}


def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        global keys, throttle, prev_throttle
        s.connect((HOST, PORT))
        while True:
            if len(sum(select([s], [], [], 0.01), [])) != 0:
                length = int.from_bytes(s.recv(4), byteorder='big')
                keys = json.loads(s.recv(length))
                s.send(int(throttle).to_bytes(4, byteorder='big'))

                if mul([keys[x] for x in r_forward]) and not mul([keys[x] for x in (all_keys - r_forward)]):
                    print('r_forward')
                    GPIO.output([left_dir, right_dir], GPIO.HIGH)
                    enable_motors(0.5, 1)

                elif reduce(op.mul, [keys[x] for x in l_forward], 1) and not mul(
                        [keys[x] for x in (all_keys - l_forward)]):
                    print('l_forward')
                    GPIO.output([left_dir, right_dir], GPIO.HIGH)
                    enable_motors(1, 0.5)

                elif mul([keys[x] for x in forward]) and not mul([keys[x] for x in (all_keys - forward)]):
                    print('forward')
                    GPIO.output([left_dir, right_dir], GPIO.HIGH)
                    enable_motors(1, 1)

                elif mul([keys[x] for x in r_backward]) and not mul([keys[x] for x in (all_keys - r_backward)]):
                    print('r_backward')
                    GPIO.output([left_dir, right_dir], GPIO.LOW)
                    enable_motors(0.5, 1)

                elif mul([keys[x] for x in l_backward]) and not mul([keys[x] for x in (all_keys - l_backward)]):
                    print('l_backward')
                    GPIO.output([left_dir, right_dir], GPIO.LOW)
                    enable_motors(1, 0.5)

                elif mul([keys[x] for x in backward]) and not mul([keys[x] for x in (all_keys - backward)]):
                    print('backward')
                    GPIO.output([left_dir, right_dir], GPIO.LOW)
                    enable_motors(1, 1)

                elif mul([keys[x] for x in l_force]) and not mul([keys[x] for x in (all_keys - l_force)]):
                    print('l_force')
                    GPIO.output([left_dir, right_dir], [GPIO.LOW, GPIO.HIGH])
                    enable_motors(1, 1)

                elif mul([keys[x] for x in r_force]) and not mul([keys[x] for x in (all_keys - r_force)]):
                    print('r_force')
                    GPIO.output([left_dir, right_dir], [GPIO.HIGH, GPIO.LOW])
                    enable_motors(1, 1)

                if mul(keys[x] for x in all_keys):
                    enable_motors(l_enable, r_enable)

                if not sum(keys.values()):
                    GPIO.output([left_dir, right_dir], GPIO.LOW)
                    enable_motors(0, 0)

            time.sleep(0.02)

            if keys[throttle_up]:
                throttle = max(0, throttle - 1)
            if keys[throttle_down]:
                throttle = min(100, throttle + 1)
            if keys[throttle_up] or keys[throttle_down]:
                if throttle != prev_throttle and throttle % 5 == 0:
                    print('Throttle: {}%'.format(throttle))
                prev_throttle = throttle
                enable_motors(l_enable, r_enable)


if __name__ == '__main__':
    run()
