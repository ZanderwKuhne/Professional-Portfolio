# Added cleanup module to ensure database integrity
from db import get_connection
import bcrypt


def delete_empty():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM users
    WHERE name = '' OR pass = ''
    """)

    conn.commit()
    conn.close()


def migrate_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, pass FROM users")
    users = cursor.fetchall()

    updated = 0

    for user in users:
        user_id = user["id"]
        password = user["pass"]

        if password.startswith("$2b$"):
            continue

        hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(14)).decode(
            "utf-8"
        )

        cursor.execute("UPDATE users SET pass = ? WHERE id = ?",
                       (hash, user_id))

        updated += 1

    conn.commit()
    conn.close()
    print(f"Migration complete. Updated {updated} users.")


if __name__ == "__main__":
    delete_empty()
    migrate_users()
