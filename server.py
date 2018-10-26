import socket

all_users = {}
online_users = {}


def register(s, data, address):
    global all_users
    msg_list = data.decode('utf-8').split(' ')
    name = msg_list[1]
    if name in all_users:
        s.sendto("用户名已存在，请重新输入".encode('utf-8'), address)
    else:
        s.sendto("注册成功".encode('utf-8'), address)
        print("{}注册成功".format(name))
        all_users[name] = address
    return


def login(s, data, address):
    global all_users, online_users
    msg_list = data.decode('utf-8').split(' ')
    name = msg_list[1]
    if name in all_users:
        online_users[name] = address
        s.sendto("登录成功".encode('utf-8'), address)
        print('当前在线用户：')
        for i in online_users:
            print(i)
        for j in online_users:
            if j != name:
                s.sendto("{}进入聊天室".format(name).encode('utf-8'), online_users[j])
    else:
        s.sendto("用户不存在".encode('utf-8'), address)
    return


def pchat(s, data, address):
    global online_users
    for i in online_users:
        if address == online_users[i]:
            name = i
            break
    msg_list = data.decode('utf-8').split(' ')
    data = ' '.join(msg_list[1:])
    msg = "{}:{}".format(name, data).encode('utf-8')
    for user in online_users:
        if user != name:
            s.sendto(msg, online_users[user])
    return


def cchat(s, data, address):
    global online_users
    msg_list = data.decode('utf-8').split(' ')
    for i in online_users:
        if msg_list[1] == i:
            address1 = online_users[i]
            break

    for j in online_users:
        if address == online_users[j]:
            name = j
            break
    msg_list = data.decode('utf-8').split(' ')
    data = ' '.join(msg_list[2:])
    msg = "{}私聊你说：{}".format(name, data).encode('utf-8')
    s.sendto(msg, address1)


def server(s):
    while True:
        data, address = s.recvfrom(1024)
        msg_list = data.decode('utf-8').split(' ')
        flag = msg_list[0]
        if flag == 'R':
            register(s, data, address)
        if flag == 'L':
            login(s, data, address)
        if flag == 'PC':
            pchat(s, data, address)
        if flag == 'CC':
            cchat(s, data, address)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = '127.0.0.1'
    port = 8888
    s.bind((host, port))
    print("等待连接....")
    server(s)









