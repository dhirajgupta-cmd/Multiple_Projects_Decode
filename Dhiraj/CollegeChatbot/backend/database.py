import sqlite3

def init_db():
    conn = sqlite3.connect('college.db')
    cursor = conn.cursor()

    # Create courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')

    # Create deadlines table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deadlines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment TEXT NOT NULL,
            due_date TEXT NOT NULL
        )
    ''')

    # Insert sample data (only if tables are empty)
    cursor.execute('SELECT COUNT(*) FROM courses')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO courses (name, description) VALUES (?, ?)', [
            ('Computer Science', 'Covers programming, algorithms, and data structures.'),
            ('Electronics', 'Focuses on circuits, signals, and embedded systems.'),
            ('Mechanical Engineering', 'Includes mechanics, thermodynamics, and design.')
        ])

    cursor.execute('SELECT COUNT(*) FROM deadlines')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO deadlines (assignment, due_date) VALUES (?, ?)', [
            ('Assignment 1', '2025-05-10'),
            ('Project Submission', '2025-06-15')
        ])

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")