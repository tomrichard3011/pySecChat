import curses
import threading
import time
from curses.textpad import Textbox

stdscr = curses.initscr()
stdscr.keypad(True)


def enter_is_terminate(x):
    if x == 10:
        return 7
    else:
        return x


def print_to_screen(output_win):
    for i in range(10):
        time.sleep(2)
        # take note of where cursor is at
        y, x = curses.getsyx()

        # move cursor to location to write new message
        output_win.addstr(("new message " + str(i) + "\n"))
        output_win.refresh()

        # place cursor back where it was.
        curses.setsyx(y, x)
        curses.doupdate()


def draw_menu(stdscr):
    # set up output window boundaries
    output_uly = (int(stdscr.getbegyx()[0]))
    output_ulx = (int(stdscr.getbegyx()[1]))
    output_lry = (int(stdscr.getmaxyx()[0] * 0.7))
    output_lrx = (int(stdscr.getmaxyx()[1]))
    output_inner_height = (output_lry - output_uly)
    output_inner_width = (output_lrx - output_ulx)

    # set up input window boundaries
    input_uly = (int(stdscr.getmaxyx()[0] * 0.7 + 1))
    input_ulx = (int(stdscr.getbegyx()[1]))
    input_lry = (int(stdscr.getmaxyx()[0]))
    input_lrx = (int(stdscr.getmaxyx()[1]))
    input_inner_height = (input_lry - input_uly + 1)
    input_inner_width = (input_lrx - input_ulx)

    # draw window border
    output_win = curses.newwin(output_inner_height, output_inner_width, output_uly, output_ulx)
    input_win = curses.newwin(input_inner_height, input_inner_width, input_uly - 1, input_ulx)
    output_win.border()
    input_win.border()

    # create window for text to appear
    output_win_sub = output_win.derwin(output_inner_height - 2, output_inner_width - 2, 1, 1)
    input_win_sub = input_win.derwin((input_inner_height - 2), (input_inner_width - 2), 1, 1)

    # set scrolling on output box
    output_win_sub.scrollok(True)
    output_win_sub.idlok(True)

    # create Textbox object to allow input
    input_box = Textbox(input_win_sub)

    # refresh screen to update all windows
    output_win.refresh()
    input_win.refresh()

    i = 0
    new_thread = threading.Thread(target=print_to_screen, args=(output_win_sub,))
    new_thread.start()

    while True:
        # set text box area
        # enter_is_terminate changes "enter" key to send message, instead of emacs key combo; ctrl-G
        input_box.edit(enter_is_terminate)
        # write message to output box
        message = input_box.gather()
        output_win_sub.addstr(message)

        # clear screen and refresh
        output_win_sub.refresh()
        input_win_sub.clear()


curses.wrapper(draw_menu)
