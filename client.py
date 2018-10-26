import socket
import threading


def send(s):
    while True:
        data = input('msg>>')
        address = ('127.0.0.1', 8888)
        s.sendto(data.encode('utf-8)'), address)


def accept(s):
    while True:
        data, address = s.recvfrom(1024)
        print(data.decode('utf-8'))


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', 9999))
    t1 = threading.Thread(target=send, args=(s,))
    t2 = threading.Thread(target=accept, args=(s,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
