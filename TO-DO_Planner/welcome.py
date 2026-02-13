# This module handles all the application logic, as well as what the user interacts with

import subprocess
import os
from enum import Enum
from users import (
    verify_user,
    get_user_goal,
    check_user_reg,
    create_user,
    add_user_goal,
    delete_goal,
    update_goal,
)
from datetime import datetime


# Using enums to clean up the user input choice logic in subsequent functions
class MainNav(Enum):
    login = 0
    register = 1
    quit = 2


class UserNav(Enum):
    retry = 0
    back = 1


class UserPageNav(Enum):
    add = 0
    remove = 1
    update = 2
    logout = 3


# Clean the console each time a user moves to a new function, ensuring a clean UX
def clear_console():
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True)


# This is the welcome page function, it offers users helpful commands to navigate through the application, all menus can return the user to this page
def print_welcome():
    clear_console()
    choosing = True
    while choosing:
        choice = input("""
        Welcome to your CLI TO-DO manager!
        Already have a profile? type 'login'
        New user? type 'register'
        Leaving? type 'quit'
        """).lower()
        # I chose to use Enum + match case pairs to clean up the function logic
        match choice:
            case MainNav.login:
                choosing = False
                login()
            case MainNav.register:
                choosing = False
                register()
            case MainNav.quit:
                choosing = False
    return choosing


# This is the login page function, users can navigate to hear from the welcome page, and will redirect them to the user page if login is successful
def login():
    clear_console()
    auth = False
    while not auth:
        username = input("""
        Enter your user name:
        """)
        password = input("""
        Enter your password:
        """)

        # Check to see if the entered username or password combo is in the database. Also stores the return values of the function
        check_user = verify_user(username, password)

        # verify_user returns a dictionary of a str: bool pair, assign the bool to auth to break the loop and move to user page
        auth = check_user["Verification status"]

        # If verification fails, alert the user and prompt them for further action
        if not auth:
            cont_check = input("""
            Username or password incorrect.
            Are you certain you have registered?
            type 'retry' to try again
            type 'back' to return to the Welcome menu
            """).lower()

            match cont_check:
                case UserNav.retry:
                    auth = True
                    login()
                case UserNav.back:
                    auth = True
                    print_welcome()
                case _:
                    print("Please enter a valid option")
    # User verified, pass the correct information to the user_page function
    user_page(username, check_user["id"])


# This is the new user registration page function, users can navigate here from the welcome page and move to the user_page once registered
def register():
    clear_console()
    user_exist = True
    while user_exist:
        username = input("Enter new username:\n")
        if check_user_reg(username):
            password = input("Enter new password:\n")
            user_data = create_user(username, password)
            input("""
            User successfully registered!
            Press Enter to continue
            """)
            user_exist = False
            user_page(username, user_data["id"])
        else:
            print("Username already exists!")
            response = input("""
            type 'retry' to try a different username
            type 'back' to return to the Welcome menu
            """).lower()

            # If the user typed in a username that already exists, give them the option to leave the registration function to login, or recursively call registration until they succeed
            match response:
                case UserNav.retry:
                    register()
                case UserNav.back:
                    print_welcome()
                case _:
                    print("Please enter a valid option")


# This is the user page function, this is where users can view their stored goals, add new ones, or mark old ones as finished
def user_page(username: str, user_id: int):
    clear_console()
    choosing = True
    while choosing:
        print(f"""
        Welcome {username}!
        Here are your current goals:
        """)
        user_goal_data = get_user_goal(user_id)
        if not user_goal_data["data"]:
            print(f"/n{user_goal_data['message']}")
        else:
            print(f"/n{user_goal_data['data']}")
        choice = input("""
        What would you like to do?
        Add new goal: type 'add'
        Remove goal: type 'remove'
        Change goal status to Completed: type 'update'
        Logout: type 'logout'
        """).lower()

        match choice:
            case UserPageNav.add:
                goal = input("What is your goal?/n")
                date_str = input("""
                When is it due?
                Input format: YYYY-MM-DD
                """)
                priority = int(
                    input("""
                What is the priority level of the goal:
                1-4 1 being highest priority, 4 being the lowest.
                Default = 1
                """)
                )
                min_req_time = int(
                    input("""
                What is the minimum required time in days you need to finish this goal?
                Low priority tasks will be moved to the top of the list if the minimum required time for completion is approaching
                Default = 7
                """)
                )
                # convert the string date to a useable date format for storage in the database
                split_dat = date_str.split("-")
                duedate = datetime(
                    int(split_dat[0]), int(split_dat[1]), int(split_dat[2])
                )
                status = add_user_goal(
                    user_id, goal, duedate, priority, min_req_time)
                input(status["message"] + "/nPress enter to continue")
                user_page(username, user_id)

            case UserPageNav.remove:
                if not user_goal_data["data"]:
                    print("Nothing to remove! Add a goal first.")
                else:
                    id_to_remove = int(
                        input("Type the goal id you want to remove:/n"))
                    status = delete_goal(user_id, id_to_remove)
                    print(status["message"] + "/nPress Enter to continue")
                    user_page(username, user_id)

            case UserPageNav.update:
                if not user_goal_data["data"]:
                    print("Nothing to update! Add a goal first.")
                else:
                    id_to_update = int(
                        input("Type the goal id you want to mark as completed:/n")
                    )
                    status = update_goal(user_id, id_to_update)
                    input(status["message"] + "/nPress Enter to continue")
                    user_page(username, user_id)

            case UserPageNav.logout:
                choosing = False
                print_welcome()
