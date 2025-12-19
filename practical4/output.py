import curses

def draw_menu(stdscr, selected_idx, menu_items):
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    stdscr.addstr(1, 1, "Student Management System (Use Up/Down + Enter)")
    
    for idx, item in enumerate(menu_items):
        x = w//2 - len(item)//2
        y = h//2 - len(menu_items)//2 + idx
        if idx == selected_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, item)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, item)
    stdscr.refresh()

def print_message(stdscr, r, c, message):
    stdscr.addstr(r, c, message)

def wait_key(stdscr):
    stdscr.getch()

def list_items(stdscr, items, title):
    stdscr.clear()
    stdscr.addstr(2, 2, f"--- {title} ---")
    for idx, item in enumerate(items):
        stdscr.addstr(4+idx, 4, str(item))
    stdscr.addstr(6+len(items), 2, "Press any key to return...")
    stdscr.getch()