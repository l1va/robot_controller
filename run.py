import socket
import subprocess
from multiprocessing import Process, Pipe

pipe_child, pipe_parent = Pipe()
pipe_parent.send('lolkkek')

PORT = 27719


def socket_server(pipe):
    print('socket server is set up and running')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((socket.gethostname(), PORT))
        s.listen(5)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = pipe.recv()
                conn.sendall(bytes(data, encoding='utf-8'))


if __name__ == '__main__':
    process = Process(target=socket_server, args=(pipe_child,))
    process.start()
    p = subprocess.Popen(["python", "manage.py", "runserver"], shell=True)
