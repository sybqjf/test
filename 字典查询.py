import socket
import threading

BUFSIZE = 65535


def read_keyboard(sock):
    while True:
        word = input('')
        sock.send(word.encode("gbk"))
        if word == "quit":
            sock.close()


def read_from_server(sock):
    while True:
        try:
            mesg = sock.recv(BUFSIZE)
            print(mesg.decode("gbk"))
        except Exception as e:
            print(e)
            break


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except Exception as e:
        print(e)
        exit()
    print("connected!")

    keyInputThread = threading.Thread(target=read_keyboard, args=(sock,))
    keyInputThread.start()

    net_recv_thread = threading.Thread(target=read_from_server, args=(sock,))
    net_recv_thread.start()



