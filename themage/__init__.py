import sys
import os
import msvcrt
import win32console
import time

def fg_color(color):
    color = color.upper()
    return eval(f'win32console.FOREGROUND_{color}')

def bg_color(color):
    color = color.upper()
    return eval(f'win32console.BACKGROUND_{color}')

FG_COLOR = {
    'RED': fg_color('red'),
    'BLUE': fg_color('blue'),
    'GREEN': fg_color('green'),
    'YELLOW': (fg_color('red') | fg_color('green')),
    'MAGENTA': (fg_color('red') | fg_color('blue')),
    'CYAN': (fg_color('blue') | fg_color('green')),
    'WHITE': (fg_color('red') | fg_color('green') | fg_color('blue')),
    'BLACK': 0
}

BG_COLOR = {
    'RED': bg_color('red'),
    'BLUE': bg_color('blue'),
    'GREEN': bg_color('green'),
    'YELLOW': (bg_color('red') | bg_color('green')),
    'MAGENTA': (bg_color('red') | bg_color('blue')),
    'CYAN': (bg_color('blue') | bg_color('green')),
    'WHITE': (bg_color('red') | bg_color('green') | bg_color('blue')),
    'BLACK': 0
}

class Screen:

    def __init__(self):
        self.stdout = win32console.CreateConsoleScreenBuffer()
        self.stdout.SetConsoleActiveScreenBuffer()
        self.fg_color = FG_COLOR['WHITE']
        self.bg_color = BG_COLOR['BLACK']
        self.cursor_x = 0
        self.cursor_y = 0
        cursor_size = self.stdout.GetConsoleCursorInfo()[0]
        self.stdout.SetConsoleCursorInfo(cursor_size, False)

    def write(self, string, color = None, x = None, y = None):
        if x is not None:
            pos = win32console.PyCOORDType(x, self.cursor_y)
            self.cursor_x = x
        elif y is not None:
            pos = win32console.PyCOORDType(self.cursor_x, y)
            self.cursor_y = y
        elif (x, y) != (None, None):
            pos = win32console.PyCOORDType(x, y)
            self.cursor_x, self.cursor_y = x, y
        else:
            pos = win32console.PyCOORDType(self.cursor_x, self.cursor_y)
        if color is None:
            pass
        else:
            self.fg_color = FG_COLOR[color.upper()]
            self.change_color()
        self.stdout.SetConsoleCursorPosition(pos)
        self.stdout.WriteConsole(string)

    def move_cursor(self, x, y):
        pos = win32console.PyCOORDType(x, y)
        self.cursor_x, self.cursor_y = x, y
        self.stdout.SetConsoleCursorPosition(pos)

    def change_color(self):
        self.stdout.SetConsoleTextAttribute(self.fg_color+self.bg_color)

    def clear(self):
        self.change_color()
        info = self.stdout.GetConsoleScreenBufferInfo()['Window']
        width = info.Right - info.Left + 1
        height = info.Bottom - info.Top + 1
        box_size = width * height
        self.stdout.FillConsoleOutputAttribute(0, box_size, win32console.PyCOORDType(0, 0))
        self.stdout.FillConsoleOutputCharacter(' ', box_size, win32console.PyCOORDType(0, 0))
        self.stdout.FlushConsoleInputBuffer()

    def get_key(self):
        key = msvcrt.getch()
        if ord(key) == 224 or 0:
            key = msvcrt.getch()
            if key == b'K':
                return 'LEFT_ARROW'
            elif key == b'P':
                return 'DOWN_ARROW'
            elif key == b'M':
                return 'RIGHT_ARROW'
            elif key == b'H':
                return 'UP_ARROW'
            else:
                return 0
        else:
            return key.decode('UTF-8')

    def __end__(self):
        self.stdout.Close()


def wrapper(func):
    screen = Screen()
    try:
        func(screen)
    finally:
        del screen


class Game:

    def __init__(self):
        wrapper(self.start)

    def start(self, screen):
        keys = ''
        while True:
            key = screen.get_key()
            if key == '\n':
                keys = ''
                screen.clear()
            elif key == '\b':
                keys = keys[:-1]
                screen.clear()
            else:
                keys = keys+key
                screen.clear()
            screen.write(keys)



Game()
