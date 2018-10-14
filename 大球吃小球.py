import pygame
import random
import math


# 生成随机颜色
def random_color(): return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


#  判断是否碰撞，并使大球吃掉小球(小球消失，大球变大)
def eat(ball1, ball2):
    x1, y1 = ball1['pos']
    x2, y2 = ball2['pos']
    x_distance = x1 - x2
    y_distance = y1 - y2
    distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
    if distance < ball1['r'] + ball2['r']:
        if ball1['r'] > ball2['r']:
            ball1['r'] = ball2['r'] + ball1['r']
            all_balls.remove(ball2)
        else:
            ball2['r'] = ball2['r'] + ball1['r']
            all_balls.remove(ball1)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    screen.fill((255, 255, 255))
    pygame.display.flip()

    # all_balls中保存多个球
    # 每个球要保存：半径、圆心坐标、颜色、x速度、y速度
    all_balls = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 点一下鼠标创建一个球
                ball = {
                        'r': random.randint(10, 20), # 随机大小\
                        'pos': event.pos, # 设置圆心为当前鼠标点击的坐标
                        'color': random_color(),
                        'x_speed': random.randint(-1, 1), # 随机方向
                        'y_speed': random.randint(-1, 1)
                }
                # 保存球
                all_balls.append(ball)
        # 刷新界面
        screen.fill((255, 255, 255))
        for ball_dict in all_balls:
            # 取出原理的x,y坐标以及他们的速度
            x, y = ball_dict['pos']
            x_speed = ball_dict['x_speed']
            y_speed = ball_dict['y_speed']
            if x >= 800:  # 设置边界并更改移动方向
                x = 800
                x_speed = -1
                ball_dict['x_speed'] = x_speed
            if x < 0:
                x = 0
                x_speed = 1
                ball_dict['x_speed'] = x_speed
            if y >= 600:
                y = 600
                y_speed = -1
                ball_dict['y_speed'] = y_speed
            if y < 0:
                y = 0
                y_speed = 1
                ball_dict['y_speed'] = y_speed
            x += x_speed
            y += y_speed
            pygame.draw.circle(screen, ball_dict['color'], (x, y), ball_dict['r'])
            # 更新球对应的坐标
            ball_dict['pos'] = x, y
        pygame.display.update()
        # 碰撞
        for ball1 in all_balls:
            for ball2 in all_balls:
                if ball1 == ball2:
                    continue
                eat(ball1, ball2)












