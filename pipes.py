from multiprocessing import Pipe

pipe_child, pipe_parent = None, None
pipe_throttle_child, pipe_throttle_parent = None, None


def init():
    global pipe_child, pipe_parent
    global pipe_throttle_child, pipe_throttle_parent
    pipe_parent, pipe_child = Pipe()
    pipe_throttle_child, pipe_throttle_parent = Pipe()
