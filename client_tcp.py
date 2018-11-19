#  我真诚地保证：
#  我自己独立地完成了整个程序从分析、设计到编码的所有工作。
#  如果在上述过程中，我遇到了什么困难而求教于人，那么，我将在程序实习报告中
#  详细地列举我所遇到的问题，以及别人给我的提示。
#  在此，我感谢 XXX, …, XXX对我的启发和帮助。下面的报告中，我还会具体地提到
#  他们在各个方法对我的帮助。
#  我的程序里中凡是引用到其他程序或文档之处，
#  例如教材、课堂笔记、网上的源代码以及其他参考书上的代码段,
#  我都已经在程序的注释里很清楚地注明了引用的出处。
#  我从未没抄袭过别人的程序，也没有盗用别人的程序，
#  不管是修改式的抄袭还是原封不动的抄袭。
#  我编写这个程序，从来没有想过要去破坏或妨碍其他计算机系统的正常运转。
#  <学生姓名> 苏益彬


import socket
import threading


def recieve(s):
    while True:
        data = s.recv(1024).decode('utf-8')
        print(data)


def send(s):
    while True:
        msg = input("")
        s.send(msg.encode('utf-8'))


def main():
    host_name = '127.0.0.1'
    host_port = 880
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host_name, host_port))
    t1 = threading.Thread(target=recieve, args=(s,))
    t1.start()
    t2 = threading.Thread(target=send, args=(s,))
    t2.start()


if __name__ == '__main__':
    main()
