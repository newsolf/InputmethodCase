# -*- coding:UTF-8 -*-
# auth：NeWolf
# date 202107029

import pyautogui
import random
import time


def keep():
    pyautogui.FAILSAFE = False
    while True:
        x = random.randint(-200, 200)
        y = random.randint(-200, 200)
        print('x = %d , y = %d' % (x, y))
        pyautogui.moveRel(x, y)
        time.sleep(1)


def one():
    print('\n'.join([' '.join(["%2s x%2s = %2s" % (j, i, i * j) for j in range(1, i + 1)]) for i in range(1, 10)]))


def print_love():
    print('\n'.join([''.join([('NeWolf'[(x - y) % len('NeWolf')] if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (
                x * 0.05) ** 2 * (y * 0.1) ** 3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(30, -30, -1)]))


def print_tortoise():
    print('\n'.join([''.join(['*' if abs(
        (lambda a: lambda z, c, n: a(a, z, c, n))(lambda s, z, c, n: z if n == 0 else s(s, z * z + c, c, n - 1))(0,
                                                                                                                 0.02 * x + 0.05j * y,
                                                                                                                 40)) < 2 else ' '
                              for x in range(-80, 20)]) for y in range(-20, 20)]))


if __name__ == '__main__':
    # keep()
    # one()
    # print_love()
    print_tortoise()

