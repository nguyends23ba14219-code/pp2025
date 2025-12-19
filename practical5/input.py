import curses
import math

def get_str(stdscr, r, c, prompt):
    stdscr.addstr(r, c, prompt)
    curses.echo() 
    input_bytes = stdscr.getstr(r, c + len(prompt), 20)
    curses.noecho()
    return input_bytes.decode('utf-8')

def get_int(stdscr, r, c, prompt):
    s = get_str(stdscr, r, c, prompt)
    try:
        return int(s)
    except ValueError:
        return None

def get_float(stdscr, r, c, prompt):
    s = get_str(stdscr, r, c, prompt)
    try:
        return float(s)
    except ValueError:
        return None

def get_rounded_mark(stdscr, r, c, prompt):
    val = get_float(stdscr, r, c, prompt)
    if val is not None:
        return math.floor(val * 10) / 10
    return None