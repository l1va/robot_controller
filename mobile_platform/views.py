import json
import os

from django.http import HttpResponse
from django.shortcuts import render

from pipes import pipe_parent, pipe_throttle_parent


def home(request):
    return render(request, 'mobile_platform/home.html')


def command(request):
    pipe_parent.send(request.body)
    return HttpResponse(str(pipe_throttle_parent.recv()))
