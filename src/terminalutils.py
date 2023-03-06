"""Make a description."""

import math
from src.fileutils import configs


def text_colored(color, text):
    """Make a description."""
    color_list = {'reset': '\033[0m',
                  'bold': '\033[01m',
                  'disable': '\033[02m',
                  'underline': '\033[04m',
                  'reverse': '\033[07m',
                  'strikethrough': '\033[09m',
                  'invisible': '\033[08m',

                  'black': '\033[30m',
                  'red': '\033[31m',
                  'green': '\033[32m',
                  'orange': '\033[33m',
                  'blue': '\033[34m',
                  'purple': '\033[35m',
                  'cyan': '\033[36m',
                  'lightgrey': '\033[37m',
                  'darkgrey': '\033[90m',
                  'lightred': '\033[91m',
                  'lightgreen': '\033[92m',
                  'yellow': '\033[93m',
                  'lightblue': '\033[94m',
                  'pink': '\033[95m',
                  'lightcyan': '\033[96m',

                  'bgblack': '\033[40m',
                  'bgred': '\033[41m',
                  'bggreen': '\033[42m',
                  'bgorange': '\033[43m',
                  'bgblue': '\033[44m',
                  'bgpurple': '\033[45m',
                  'bgcyan': '\033[46m',
                  'bglightgrey': '\033[47m'}

    return f"{color_list[color]}{text}{color_list['reset']}"


def clear_line():
    """Make a description."""
    clrl = '\r' + ' '*200 + '\r'
    return clrl


def get_progress_bar(value, base, gui=False):
    """Make a description."""
    progress = 100
    if base > 1:
        progress = int(100*value/(base-1))
    bar_size = int(progress/4)
    bar_c = '='*bar_size
    progress_bar = ""
    if gui:
        progress_bar = bar_c
        progress_bar += str(progress)+"%"
        progress_bar += bar_c
    else:
        progress_bar = text_colored('orange', bar_c)
        progress_bar += text_colored('green', str(progress)+"%")
        progress_bar += text_colored('orange', bar_c)
    back_string = '\b'*(bar_size+2+bar_size)
    if progress >= 10:
        back_string += '\b'
    return progress_bar + back_string

def print_verbose_progressbar(value, base, gui=False):
    """Make a description."""
    if configs["verbose"]:
        print(get_progress_bar(value, base, gui=gui), end='', flush=True)
        
def print_verbose_msg(color, msg, gui=False):
    """Make Description."""
    if configs["verbose"]:
        if gui:
            print(msg, end='', flush=True)
        else:
            print_txt = text_colored(color, msg)
            print(print_txt, end='', flush=True)
