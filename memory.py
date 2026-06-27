import sqlite3

def get_config(customer_id):
    return {
        "configurable": {
            "thread_id": customer_id
        }
    }


# --------------------------------------------------
# SQLite Database Connection
# --------------------------------------------------

conn = sqlite3.connect(
    "memory.db",
    check_same_thread=False
)

cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS conversations(

id INTEGER PRIMARY KEY AUTOINCREMENT,

customer_id TEXT,

customer_name TEXT,

query TEXT,

response TEXT

)
""")

conn.commit()


# --------------------------------------------------
# Save Conversation
# --------------------------------------------------

def save_conversation(
        customer_id,
        customer_name,
        query,
        response
):

    cursor.execute(
        """
        INSERT INTO conversations
        (
            customer_id,
            customer_name,
            query,
            response
        )
        VALUES (?,?,?,?)
        """,
        (
            customer_id,
            customer_name,
            query,
            response
        )
    )

    conn.commit()


# --------------------------------------------------
# Retrieve Previous Issue
# --------------------------------------------------

def get_previous_issue(customer_id):

    cursor.execute(
        """
        SELECT query

        FROM conversations

        WHERE customer_id = ?

        ORDER BY id DESC

        LIMIT 2
        """,
        (customer_id,)
    )

    rows = cursor.fetchall()

    if len(rows) >= 2:
        return rows[1][0]

    elif len(rows) == 1:
        return rows[0][0]

    else:
        return "No previous issue found."


# --------------------------------------------------
# Retrieve Previous Response (Optional)
# --------------------------------------------------

def get_previous_response(customer_id):

    cursor.execute(
        """
        SELECT response

        FROM conversations

        WHERE customer_id = ?

        ORDER BY id DESC

        LIMIT 2
        """,
        (customer_id,)
    )

    rows = cursor.fetchall()

    if len(rows) >= 2:
        return rows[1][0]

    elif len(rows) == 1:
        return rows[0][0]

    else:
        return "No previous response found."