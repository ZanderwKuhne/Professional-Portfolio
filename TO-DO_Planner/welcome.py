# This module handles all the application logic, as well as what the user interacts with

import subprocess
import os
from users import (
    verify_user,
    get_user_goal,
    check_user_reg,
    create_user,
    add_user_goal,
    delete_goal,
    update_goal,
    sort_goals,
    valid_date,
)
from datetime import datetime


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
        1. Login
        2. Register
        3. Quit
        """).lower()
        # I chose to use Enum + match case pairs to clean up the function logic
        match choice:
            case "1":
                choosing = False
                return login()
            case "2":
                choosing = False
                return register()
            case "3":
                choosing = False
            case _:
                print("Please enter a valid option")
    return choosing


# This is the login page function, users can navigate to hear from the welcome page, and will redirect them to the user page if login is successful
def login():
    clear_console()
    (valid_date,)
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
            1. Retry
            2. Back
            """).lower()

            match cont_check:
                case "1":
                    continue
                case "2":
                    return "welcome"
                case _:
                    print("Please enter a valid option")
        # User verified, pass the correct information to the user_page function
        return user_page(username, check_user["id"])


# This is the new user registration page function, users can navigate here from the welcome page and move to the user_page once registered
def register():
    clear_console()
    while True:
        username = input(
            "Enter new username:\nUsername length minimum of 4 characters\n"
        )
        if check_user_reg(username):
            password = input(
                "Enter new password:\nPassword length minimum of 6 characters\n"
            )
            if not username or not password:
                print("Username or password cannot be empty.")
                continue
            if len(username) < 5 or len(password) < 6:
                print("Username or password too short")
                continue
            user_data = create_user(username, password)
            input("""
            User successfully registered!
            Press Enter to continue
            """)
            return user_page(username, user_data["id"])
        else:
            print("Username already exists!")
            response = input("""
            1. Retry
            2. Back
            """).lower()

            # If the user typed in a username that already exists, give them the option to leave the registration function to login, or recursively call registration until they succeed
            match response:
                case "1":
                    continue
                case "2":
                    return "welcome"
                case _:
                    print("Please enter a valid option")


# This is the user page function, this is where users can view their stored goals, add new ones, or mark old ones as finished
def user_page(username: str, user_id: int):
    clear_console()
    while True:
        print(f"""
        Welcome {username}!
        Here are your current goals:
        """)
        user_goal_data = get_user_goal(user_id)
        if not user_goal_data["data"]:
            print(f"\n{user_goal_data['message']}")
        else:
            sorted = sort_goals(user_goal_data["data"])
            for goal_item in sorted:
                for key, goal in goal_item.items():
                    print(key + ": " + str(goal))
                print("\n-------------------------------\n")
        choice = input("""
        What would you like to do?
        1. Add goal
        2. Remove goal
        3. Update goal
        4. Logout
        """).lower()

        match choice:
            case "1":
                goal = input("What is your goal?\n")
                date_str = input("""
                When is it due?
                Input format: YYYY-MM-DD
                """).strip()

                priority = input("""
                What is the priority level of the goal:
                1-4 1 being highest priority, 4 being the lowest.
                Default = 1
                """).strip()

                min_req_time = input("""
                What is the minimum required time in days you need to finish this goal?
                Low priority tasks will be moved to the top of the list if the minimum required time for completion is approaching
                Default = 7
                """).strip()

                # convert the string date to a useable date format for storage in the database
                duedate = valid_date(date_str)
                if not priority:
                    priority = 1
                if not min_req_time:
                    min_req_time = 7
                status = add_user_goal(
                    user_id, goal, duedate, int(priority), int(min_req_time)
                )
                input(status["message"] + "\nPress enter to continue")
                clear_console()
                continue

            case "2":
                if not user_goal_data["data"]:
                    print("Nothing to remove! Add a goal first.")
                    continue
                else:
                    id_to_remove = int(
                        input("Type the goal id you want to remove:\n"))
                    status = delete_goal(user_id, id_to_remove)
                    print(status["message"] + "\nPress Enter to continue")
                    clear_console()
                    continue

            case "3":
                if not user_goal_data["data"]:
                    print("Nothing to update! Add a goal first.")
                    continue
                else:
                    id_to_update = int(
                        input("Type the goal id you want to mark as completed:\n")
                    )
                    status = update_goal(user_id, id_to_update)
                    input(status["message"] + "\nPress Enter to continue")
                    clear_console()
                    continue

            case "4":
                return "welcome"

            case _:
                print("Please enter a valid option")
