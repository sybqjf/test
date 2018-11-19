import socket
import threading

endict = dict()


def init_dict():
    fp = open('新东方红宝书.txt', 'r', encoding='utf8')
    for line in fp:
        words = line.split('   ')
        if len(words) == 2:
            key, value = words
            endict[key] = value.replace("\n", "")
    fp.close()


def lookup_word(word):
    if word in endict:
        return "{} : {}".format(word, endict[word])
    else:
        return "找不到单词{}".format(word)


def serve_client(sc):
    while True:
        try:
            data = sc.recv(1024)
            if not data:
                break
            word = data.decode("gbk", errors="ignore")
            if word == "quit":
                break
            result = lookup_word(word)
            print(word, result)
            sc.sendall((result+'\r\n').encode("gbk"))
        except Exception as e:
            print(e)
            break
    sc.close()


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    init_dict()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    print('Listening at', sock.getsockname())
    while True:
        sc, address = sock.accept()
        print('Connected by {}'.format(address))
        serve_client_thread = threading.Thread(target=serve_client, args=(sc,))
        serve_client_thread.start()
    sock.close()



