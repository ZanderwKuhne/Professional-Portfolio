# This module is used to handle all user related database functions,
# they are used in the welcome.py module, which houses the apllication logic

import bcrypt
from db import get_connection
from datetime import date, datetime, timedelta


# Create the user in the database using sql queries
def create_user(name: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_pw = pass_hash(password)

    cursor.execute(
        """INSERT INTO users (name, pass) VALUES (?, ?)""",
        (
            name,
            hashed_pw,
        ),
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    # return relevant data to be used in subsequent functions in welcome.py
    return {"id": user_id, "name": name}


# Create user goal entries in the database using sql queries
def add_user_goal(
    user_id: int,
    goal: str,
    due_date: date,
    priority=1,
    min_time=7,
    status="Incomplete",
):
    conn = get_connection()
    cursor = conn.cursor()
    now = date.today()
    deadline = due_date

    cursor.execute(
        """
        INSERT INTO goals (user_id, goal, priority, date_added, deadline, min_time, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            goal,
            priority,
            now,
            deadline,
            min_time,
            status,
        ),
    )

    conn.commit()
    conn.close()

    return {"message": "Goal Added!"}


# Retrieve relevant data from database to display to the user
def get_user_goal(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, goal, date_added, deadline, priority, min_time, status
        FROM goals
        WHERE user_id = ?
        """,
        (user_id,),
    )

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {"message": "Looks like you haven't set any goals yet!", "data": []}
    return {"user_id": user_id, "data": [dict(row) for row in rows]}


def sort_goals(goal_list: list):
    initial_sort = sorted(goal_list, key=lambda x: x["priority"])
    sorted_goals = sorted(
        initial_sort,
        key=lambda x: not (
            date.fromisoformat(x["deadline"]) - date.today()
            <= timedelta(days=x["min_time"] + 1)
            and x["status"] == "Incomplete"
        ),
    )
    sort_completed = sorted(sorted_goals, key=lambda x: x["status"] == "Completed")
    return sort_completed


# Verify if the received user information is correct, compare input password with stored hash password, return data based on verification status
def verify_user(name: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, pass
        FROM users
        WHERE name = ?
        """,
        (name,),
    )

    row = cursor.fetchone()
    conn.close()
    if not row:
        return {"Verification status": False}

    stored_hash = row["pass"]
    if hash_pass_check(stored_hash, password):
        return {"Verification status": True, "id": row["id"]}
    return {"Verification status": False}


# Function used when registering new user, if the name passed as an argument is already in the database, return False, else return True
def check_user_reg(name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name
        FROM users
        WHERE name = ?
        """,
        (name,),
    )

    row = cursor.fetchone()
    conn.close()
    if not row:
        return True
    return False


# Function used for deleting user goals
def delete_goal(user_id: int, data_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM goals
        WHERE id = ? AND user_id = ?
        """,
        (data_id, user_id),
    )

    row = cursor.fetchone()

    if row is None:
        conn.close()
        return {
            "message": "Selected goal not stored or does not belong to current user"
        }

    cursor.execute(
        """
        DELETE FROM goals
        WHERE id = ? AND user_id = ?
        """,
        (data_id, user_id),
    )

    conn.commit()
    conn.close()

    return {"message": "Goal successfully removed!"}


# Function for updating user goals when they are finished.
def update_goal(user_id: int, data_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM goals
        WHERE id = ? AND user_id = ?
        """,
        (data_id, user_id),
    )

    row = cursor.fetchone()

    if row is None:
        conn.close()
        return {
            "message": "Selected goal not stored or does not belong to current user"
        }

    cursor.execute(
        """
    UPDATE goals
    SET status = 'Completed'
    WHERE id = ? AND user_id = ?
    """,
        (data_id, user_id),
    )

    conn.commit()
    conn.close()

    return {"message": "Goal successfully updated!"}


# Ensure entered date is a valid format
def valid_date(date_string, default_date=date.today()):
    try:
        check_date = datetime.strptime(date_string, "%Y-%m-%d")
        return check_date.date()
    except ValueError as e:
        print(f"{e}: {date_string} Using default")
        return default_date


# Store input password as hashed string using bcrypt
def pass_hash(password: str):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(14)).decode("utf-8")
    return hashed


# Check if stored hash password matches user input password for verification
def hash_pass_check(hash_pw: str, input_pw: str):
    if bcrypt.checkpw(input_pw.encode("utf-8"), hash_pw.encode("utf-8")):
        return True
    return False
