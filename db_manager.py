import mysql.connector
from tkinter import messagebox

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mkd@sql", # <-- IMPORTANT: CHANGE THIS
            database="PeerTutoring"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
        return None

# --- Student Management Functions ---

def fetch_students():
    """Fetches all students from the database."""
    conn = get_db_connection()
    if not conn:
        return []
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Student ORDER BY student_id")
        return cursor.fetchall()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error fetching students: {e}")
        return []
    finally:
        if conn:
            conn.close()

def add_student(data):
    """Adds a new student to the database. Data is a dictionary."""
    conn = get_db_connection()
    if not conn:
        return False
        
    query = """
    INSERT INTO Student (name, email, ph_no, role, dept, year) 
    VALUES (%(name)s, %(email)s, %(ph_no)s, %(role)s, %(dept)s, %(year)s)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        return True
    except mysql.connector.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Error adding student: {e}")
        return False
    finally:
        if conn:
            conn.close()

def update_student(data):
    """Updates an existing student. Data is a dictionary including student_id."""
    conn = get_db_connection()
    if not conn:
        return False
        
    query = """
    UPDATE Student 
    SET name=%(name)s, email=%(email)s, ph_no=%(ph_no)s, 
        role=%(role)s, dept=%(dept)s, year=%(year)s
    WHERE student_id = %(student_id)s
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        return True
    except mysql.connector.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Error updating student: {e}")
        return False
    finally:
        if conn:
            conn.close()

def delete_student(student_id):
    """Deletes a student from the database."""
    conn = get_db_connection()
    if not conn:
        return False
        
    query = "DELETE FROM Student WHERE student_id = %s"
    try:
        cursor = conn.cursor()
        cursor.execute(query, (student_id,))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Error deleting student: {e}")
        return False
    finally:
        if conn:
            conn.close()