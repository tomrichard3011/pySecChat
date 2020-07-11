import curses
import threading
import queue
from curses.textpad import Textbox
import time


# change text editor controls so that enter sends messages
def enter_is_terminate(x):
    if x == 10:
        return 7
    else:
        return x


class ui:
    def __init__(self, input_q: queue.SimpleQueue, output_q: queue.SimpleQueue):
        # define queues for input and output
        self.input_q = input_q
        self.output_q = output_q

        # initiate curses screen
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.doupdate()

    # prints to output window
    def print_to_screen(self, output_win):
        while 1:
            if not self.output_q.empty():
                # take note of where cursor is at
                y, x = curses.getsyx()

                # get latest message from output_q
                msg = self.output_q.get()
                # msg = 'message'
                output_win.addstr(msg.rstrip() + "\n")
                output_win.refresh()

                # place cursor back where it was.
                curses.setsyx(y, x)
                curses.doupdate()
            time.sleep(.2)

    def textbox_init(self, input_win, output_win):
        # create Textbox object to allow input
        input_box = Textbox(input_win)

        while 1:
            # set text box area
            # enter_is_terminate changes "enter" key to send message, instead of emacs key combo; ctrl-G
            input_box.edit(enter_is_terminate)

            # write message to input_q
            message = input_box.gather().rstrip()
            if message == 'q':
                break

            # add message to input_q
            self.input_q.put(message + '\n')

            # clear screen and refresh
            output_win.refresh()
            input_win.clear()
            input_win.refresh()
            curses.doupdate()

    def ui_menu(self):
        # set up output window boundaries
        output_uly = (int(self.stdscr.getbegyx()[0]))
        output_ulx = (int(self.stdscr.getbegyx()[1]))
        output_lry = (int(self.stdscr.getmaxyx()[0] * 0.7))
        output_lrx = (int(self.stdscr.getmaxyx()[1]))
        output_inner_height = (output_lry - output_uly)
        output_inner_width = (output_lrx - output_ulx)

        # set up input window boundaries
        input_uly = (int(self.stdscr.getmaxyx()[0] * 0.7 + 1))
        input_ulx = (int(self.stdscr.getbegyx()[1]))
        input_lry = (int(self.stdscr.getmaxyx()[0]))
        input_lrx = (int(self.stdscr.getmaxyx()[1]))
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

        # refresh screen to update all windows
        output_win.refresh()
        input_win.refresh()

        return output_win_sub, input_win_sub

    def run(self, stdscr):
        output_win, input_win = self.ui_menu()

        # create new thread to handle incoming output
        output_thread = threading.Thread(target=self.print_to_screen, args=(output_win,))
        output_thread.daemon = True
        output_thread.start()

        # generate textbox inside input window and continuously accept input
        self.textbox_init(input_win, output_win)

        # exit sequence
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
