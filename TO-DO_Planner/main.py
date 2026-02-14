from db import init_db
import welcome
import sys


init_db()


def main():
    # ensure the application runs continuously until the welcome page returns a False value, in which case the application closes
    running = True
    while running:
        state = welcome.print_welcome()
        if state == "welcome":
            continue
        else:
            running = False
    sys.exit()


main()
