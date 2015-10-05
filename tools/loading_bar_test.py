#! /usr/bin/python3

import time
import sys

if __name__ == '__main__':

    toolbar_width = 40

    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    # return to start of line, after '['
    sys.stdout.write("\b" * (toolbar_width + 1))

    for i in range(toolbar_width):
        # do real work here
        time.sleep(0.1)

        # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("\n")
