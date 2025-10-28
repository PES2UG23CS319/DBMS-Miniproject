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
            
# --- Helper Functions (for populating dropdowns) ---

def fetch_students_by_role(role):
    """Fetches students with a specific role."""
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT student_id, name FROM Student WHERE role = %s ORDER BY name", (role,))
        return cursor.fetchall()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error fetching students: {e}")
        return []
    finally:
        if conn: conn.close()

def fetch_all_subjects():
    """Fetches all subjects."""
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT subject_id, subject_name FROM Subject ORDER BY subject_name")
        return cursor.fetchall()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error fetching subjects: {e}")
        return []
    finally:
        if conn: conn.close()

# --- Team Management Functions ---

def fetch_teams():
    """Fetches all teams with their mentor's name."""
    conn = get_db_connection()
    if not conn: return []
    query = """
    SELECT t.team_id, t.team_name, s.name as mentor_name, t.creation_date 
    FROM Team t 
    LEFT JOIN Student s ON t.mentor_id = s.student_id
    ORDER BY t.team_name
    """
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error fetching teams: {e}")
        return []
    finally:
        if conn: conn.close()

def fetch_team_members(team_id):
    """Fetches all members (mentors and mentees) for a specific team."""
    conn = get_db_connection()
    if not conn: return []
    query = """
    SELECT s.student_id, s.name, tm.role 
    FROM TeamMember tm 
    JOIN Student s ON tm.student_id = s.student_id 
    WHERE tm.team_id = %s
    """
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (team_id,))
        return cursor.fetchall()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error fetching team members: {e}")
        return []
    finally:
        if conn: conn.close()

def create_team(team_name, mentor_id, mentee_ids_list):
    """Creates a new team and adds a mentor and mentees."""
    conn = get_db_connection()
    if not conn: return False
    
    try:
        cursor = conn.cursor()
        # 1. Create the team
        cursor.execute(
            "INSERT INTO Team (team_name, mentor_id, creation_date) VALUES (%s, %s, CURDATE())",
            (team_name, mentor_id)
        )
        team_id = cursor.lastrowid
        
        # 2. Add the mentor to TeamMember
        cursor.execute(
            "INSERT INTO TeamMember (team_id, student_id, role) VALUES (%s, %s, 'mentor')",
            (team_id, mentor_id)
        )
        
        # 3. Add all mentees to TeamMember
        mentee_data = [(team_id, mentee_id, 'mentee') for mentee_id in mentee_ids_list]
        if mentee_data:
            cursor.executemany(
                "INSERT INTO TeamMember (team_id, student_id, role) VALUES (%s, %s, %s)",
                mentee_data
            )
        
        conn.commit()
        return True
    except mysql.connector.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Error creating team: {e}")
        return False
    finally:
        if conn: conn.close()

def add_member_to_team(team_id, student_id, role):
    """Adds a single new member to a team."""
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO TeamMember (team_id, student_id, role) VALUES (%s, %s, %s)",
            (team_id, student_id, role)
        )
        conn.commit()
        return True
    except mysql.connector.Error as e:
        conn.rollback()
        # Handle duplicate entry gracefully
        if e.errno == 1062: # Duplicate key
             messagebox.showwarning("Warning", "This student is already in the team.")
        else:
            messagebox.showerror("Database Error", f"Error adding member: {e}")
        return False
    finally:
        if conn: conn.close()

def delete_team(team_id):
    """Deletes a team. TeamMembers are deleted by ON DELETE CASCADE."""
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Team WHERE team_id = %s", (team_id,))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Error deleting team: {e}")
        return False
    finally:
        if conn: conn.close()

# --- Mentorship Session Management Functions ---

def fetch_sessions():
    """Fetches all mentorship sessions with subject names."""
    conn = get_db_connection()
    if not conn: return []
    query = """
    SELECT ms.session_id, s.subject_name, ms.date_time, ms.duration, ms.status 
    FROM MentorshipSession ms 
    LEFT JOIN Subject s ON ms.subject_id = s.subject_id 
    ORDER BY ms.date_time DESC
    """
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error fetching sessions: {e}")
        return []
    finally:
        if conn: conn.close()

def fetch_session_participants(session_id):
    """Fetches all participants for a specific session."""
    conn = get_db_connection()
    if not conn: return []
    query = """
    SELECT s.student_id, s.name, sp.role 
    FROM SessionParticipant sp 
    JOIN Student s ON sp.student_id = s.student_id 
    WHERE sp.session_id = %s
    """
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (session_id,))
        return cursor.fetchall()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error fetching participants: {e}")
        return []
    finally:
        if conn: conn.close()

def schedule_session(subject_id, date_time, duration, mentor_id, mentee_ids_str):
    """Calls the AddMentorshipSession stored procedure."""
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        args = (subject_id, date_time, duration, mentor_id, mentee_ids_str)
        cursor.callproc('AddMentorshipSession', args)
        conn.commit()
        return True
    except mysql.connector.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Error scheduling session: {e}")
        return False
    finally:
        if conn: conn.close()

def update_session_status(session_id, status):
    """Updates the status of a session."""
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE MentorshipSession SET status = %s WHERE session_id = %s",
            (status, session_id)
        )
        conn.commit()
        return True
    except mysql.connector.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Error updating status: {e}")
        return False
    finally:
        if conn: conn.close()

def cancel_session(session_id):
    """Deletes a session. Participants/Feedback are deleted by ON DELETE CASCADE."""
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM MentorshipSession WHERE session_id = %s", (session_id,))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"Error cancelling session: {e}")
        return False
    finally:
        if conn: conn.close()
