import curses, time
from curses.textpad import Textbox, rectangle
stdscr = curses.initscr()
stdscr.keypad(True)


def enter_is_terminate(x):
    if x == 10:
        return 7
    else:
        return x

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
    output_win_sub = output_win.derwin(output_inner_height - 1, output_inner_width - 2, 1, 1)
    input_win_sub = input_win.derwin((input_inner_height - 2), (input_inner_width - 2), 1, 1)
    input_box = Textbox(input_win_sub)

    output_win.refresh()
    input_win.refresh()
    input_win_sub.refresh()

    i = 0
    while True:
        # set text box area
        # enter_is_terminate changes "enter" key to send message, instead of emacs key combo; ctrl-G
        input_box.edit(enter_is_terminate)
        # write message to output box
        message = input_box.gather()
        output_win_sub.addstr(i, 0, message)


        # clear screen and refresh
        output_win_sub.refresh()
        input_win_sub.clear()

        if i >= output_inner_height - 3:
            i = 0
        else:
            i += 1


curses.wrapper(draw_menu)
