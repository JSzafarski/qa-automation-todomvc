import sqlite3
from datetime import datetime

def initialise_database():
    """
       It's important to initialise the table before we can append data to it.
       This function Initialises the database by creating a table for test results
       (if it doesn't already exist).

        Table: log_test_results
        - id: Auto-incrementing primary key
        - timestamp: logged at runtime (ISO format)
        - todo_text: The text of the string passed during the test
        - result: 'pass' or 'fail'
    """
    conn = sqlite3.connect("log_test_results.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time_stamp TEXT,
            todo_input TEXT,
            outcome TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_result(todo_input, outcome):
    """
       This function saves the result of a test run into the db file.
       Args:
        todo_input (str): string item that was used as an input.
        outcome (str): The outcome of the test.
    """
    conn = sqlite3.connect("log_test_results.db") #connect to the database to update it
    c = conn.cursor()
    c.execute(''' 
        INSERT INTO test_results (timestamp, todo_input, outcome)
        VALUES (?, ?, ?) 
    ''', (datetime.now().isoformat(), todo_input, outcome))
    conn.commit()
    conn.close() # close the table