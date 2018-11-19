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
import random


def play_game(conn, address):
    rule = "骰子游戏规则如下：\n" \
           "ya tc <数量> <coin|silver|gold> 押头彩(两数顺序及点数均正确)       一赔三十五\n" \
           "ya dc <数量> <coin|silver|gold> 押大彩(两数点数正确)               一赔十七\n" \
           "ya kp <数量> <coin|silver|gold> 押空盘(两数不同且均为偶数)         一赔五\n" \
           "ya qx <数量> <coin|silver|gold> 押七星(两数之和为七)               一赔五\n" \
           "ya dd <数量> <coin|silver|gold> 押单对(两数均为奇数)               一赔三\n" \
           "ya sx <数量> <coin|silver|gold> 押散星(两数之和为三、五、九、十一) 一赔二\n"\
           "每盘按从上到下的顺序只出现一种点型(头彩和大彩可同时出现)，其他情况都算庄家赢。"

    conn.send(rule.encode('utf-8'))
    while True:
        msg = "新开盘！预叫头彩!\n"
        conn.send(msg.encode('utf-8'))
        num1 = random.randint(1, 6)
        num2 = random.randint(1, 6)
        msg = "头彩骰号是 {}、{}！\n输入你压的值：\n".format(num1, num2)
        conn.send(msg.encode('utf-8'))
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        data = data.split(' ')
        try:
            bet = data[1]
            amount = int(data[2])
            unit = data[3]
            if unit == 'coin' or unit == 'silver' or unit == 'gold':
                pass
            else:
                conn.send("请输入正确的单位!\n".encode('utf-8'))
                continue
        except:
            conn.send("请输入正确的格式！\n".encode('utf-8'))
            continue

        a = random.randint(1, 6)
        b = random.randint(1, 6)

        if a == num1 and b == num2:
            result = 'tc'
            f = '头彩'
            odds = 35
        elif (a+b) == (num1+num2) and a == num2:
            result = 'dc'
            f = '大彩'
            odds = 17
        elif a != b and a % 2 == 0 and b % 2 == 0:
            result = 'kp'
            f = '空盘'
            odds = 5
        elif (a+b) == 7:
            result = 'qx'
            f = '七星'
            odds = 5
        elif (a % 2) != 0 and (b % 2) != 0:
            result = 'dd'
            f = '单对'
            odds = 3
        elif (a+b) == 3 or (a+b) == 5 or (a+b) == 9 or (a+b) == 11:
            result = 'sx'
            f = '散星'
            odds = 2
        else:
            result = '其他'

        if bet == result:
            money = odds*amount
            conn.send("{}、{}……{}\n你赢了{} {}!\n".format(a, b, f, money, unit).encode('utf-8'))
        else:
            conn.send("{}、{}……{}\n你输了 {} {}!\n".format(a, b, f, amount, unit).encode('utf-8'))
    conn.close()
    print("断开连接")
    return


def main():
    host_port = 880
    host_address = '127.0.0.1'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host_address, host_port))
    s.listen(3)
    print("{}:{} is listening...".format(host_address, host_port))

    while True:
        conn, address = s.accept()
        print("accept connection from ", address)
        new_conn = threading.Thread(target=play_game, args=(conn, address))
        new_conn.start()


if __name__ == '__main__':
    main()


