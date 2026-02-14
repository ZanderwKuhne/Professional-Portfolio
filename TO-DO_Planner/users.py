# This module is used to handle all user related database functions,
# they are used in the welcome.py module, which houses the apllication logic

from db import get_connection
from datetime import datetime, timezone


# Create the user in the database using sql queries
def create_user(name: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO users (name, pass) VALUES (?, ?)""",
        (
            name,
            password,
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
    due_date: datetime,
    priority=1,
    min_time=7,
    status="Incomplete",
):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc)
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
            now.isoformat(),
            deadline.isoformat(),
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
        SELECT id, goal, deadline, min_time, status
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


# Verify if the received user information is correct, return data based on verification status
def verify_user(name: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, pass
        FROM users
        WHERE name = ? AND pass = ?
        """,
        (
            name,
            password,
        ),
    )

    row = cursor.fetchone()
    conn.close()
    if not row:
        return {"Verification status": False}
    return {"Verification status": True, "id": row["id"]}


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
