import tkinter as tk
from tkinter import ttk, messagebox, Listbox
import db_manager  # Import our backend file

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Peer Tutoring Management System")
        self.geometry("1200x800") # Made window larger

        # --- Create Tabs ---
        self.notebook = ttk.Notebook(self)
        
        self.tab_students = ttk.Frame(self.notebook, padding=10)
        self.tab_teams = ttk.Frame(self.notebook, padding=10)
        self.tab_sessions = ttk.Frame(self.notebook, padding=10)
        
        self.notebook.add(self.tab_students, text="🎓 Student Management")
        self.notebook.add(self.tab_teams, text="👥 Team Management")
        self.notebook.add(self.tab_sessions, text="📘 Session Management")
        
        self.notebook.pack(fill=tk.BOTH, expand=True)

     # ... notebook.pack() ...

        # --- Status Bar ---
        # CREATE THE STATUS BAR *BEFORE* THE TABS
        self.status_label = ttk.Label(self, text="Ready", relief=tk.SUNKEN, anchor="w")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # --- Create each tab's content ---
        # Now these functions can safely use self.status_label
        self.create_student_tab()
        self.create_team_tab()
        self.create_session_tab()

    # ===================================================================
    # --- 1. STUDENT MANAGEMENT TAB ---
    # ===================================================================
    
    def create_student_tab(self):
        # --- Form Variables ---
        self.student_form_vars = {
            "name": tk.StringVar(), "email": tk.StringVar(),
            "ph_no": tk.StringVar(), "dept": tk.StringVar(),
            "year": tk.StringVar(), "role": tk.StringVar(value="mentee")
        }
        self.selected_student_id = None
        
        # --- Layout ---
        main_frame = ttk.Frame(self.tab_students)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # --- Student Table ---
        columns = ("id", "name", "email", "phone", "dept", "year", "role")
        self.student_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns: self.student_tree.heading(col, text=col.title())
        # Set column widths
        self.student_tree.column("id", width=40, anchor="center")
        self.student_tree.column("name", width=150)
        self.student_tree.column("email", width=200)
        self.student_tree.column("phone", width=100)
        self.student_tree.column("dept", width=80)
        self.student_tree.column("year", width=50, anchor="center")
        self.student_tree.column("role", width=80)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.student_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.student_tree.bind("<<TreeviewSelect>>", self.on_student_select)

        # --- Student Form ---
        form_frame = ttk.LabelFrame(main_frame, text="Student Form", padding=15)
        form_frame.pack(fill=tk.X, pady=10)
        # Form fields
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.student_form_vars["name"], width=40).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.student_form_vars["email"], width=40).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.student_form_vars["ph_no"], width=40).grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Dept:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.student_form_vars["dept"], width=20).grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(form_frame, text="Year:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.student_form_vars["year"], width=20).grid(row=1, column=3, padx=5, pady=5)
        ttk.Label(form_frame, text="Role:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        ttk.Combobox(form_frame, textvariable=self.student_form_vars["role"], values=["mentee", "mentor"]).grid(row=2, column=3, padx=5, pady=5)

        # --- Button Frame ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="Add Student", command=self.handle_add_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Student", command=self.handle_update_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Student", command=self.handle_delete_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_student_form).pack(side=tk.LEFT, padx=5)
        
        # --- Initial Load ---
        self.populate_student_list()

    def populate_student_list(self):
        for row in self.student_tree.get_children(): self.student_tree.delete(row)
        students = db_manager.fetch_students()
        if students:
            for student in students:
                self.student_tree.insert("", tk.END, values=(
                    student['student_id'], student['name'], student['email'],
                    student['ph_no'], student['dept'], student['year'], student['role']
                ))
            self.status_label.config(text=f"Loaded {len(students)} students.")
        else: self.status_label.config(text="No students found.")

    def on_student_select(self, event):
        try:
            selected_item = self.student_tree.selection()[0]
            student = self.student_tree.item(selected_item, "values")
            self.selected_student_id = student[0]
            self.student_form_vars["name"].set(student[1])
            self.student_form_vars["email"].set(student[2])
            self.student_form_vars["ph_no"].set(student[3])
            self.student_form_vars["dept"].set(student[4])
            self.student_form_vars["year"].set(student[5])
            self.student_form_vars["role"].set(student[6])
            self.status_label.config(text=f"Selected student ID: {self.selected_student_id}")
        except IndexError: pass

    def clear_student_form(self):
        for var in self.student_form_vars.values(): var.set("")
        self.student_form_vars["role"].set("mentee")
        self.selected_student_id = None
        self.student_tree.selection_remove(self.student_tree.selection())
        self.status_label.config(text="Form cleared.")

    def handle_add_student(self):
        data = {key: var.get() for key, var in self.student_form_vars.items()}
        if not data["name"] or not data["email"]:
            messagebox.showwarning("Validation Error", "Name and Email are required.")
            return
        if db_manager.add_student(data):
            self.status_label.config(text="Student added!")
            self.populate_student_list()
            self.clear_student_form()
            self.refresh_team_data() # Refresh team tab data
        else: self.status_label.config(text="Failed to add student.")

    def handle_update_student(self):
        if self.selected_student_id is None:
            messagebox.showwarning("Update Error", "Please select a student to update.")
            return
        data = {key: var.get() for key, var in self.student_form_vars.items()}
        data["student_id"] = self.selected_student_id
        if db_manager.update_student(data):
            self.status_label.config(text="Student updated!")
            self.populate_student_list()
            self.clear_student_form()
            self.refresh_team_data() # Refresh team tab data
        else: self.status_label.config(text="Failed to update student.")

    def handle_delete_student(self):
        if self.selected_student_id is None:
            messagebox.showwarning("Delete Error", "Please select a student to delete.")
            return
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student ID {self.selected_student_id}?"):
            if db_manager.delete_student(self.selected_student_id):
                self.status_label.config(text="Student deleted!")
                self.populate_student_list()
                self.clear_student_form()
                self.refresh_team_data() # Refresh team tab data
            else: self.status_label.config(text="Failed to delete student.")

    # ===================================================================
    # --- 2. TEAM MANAGEMENT TAB ---
    # ===================================================================

    def create_team_tab(self):
        # --- Form Variables ---
        self.team_name_var = tk.StringVar()
        self.team_mentor_var = tk.StringVar()
        self.selected_team_id = None
        
        # --- Store data for dropdowns ---
        self.mentor_data = []
        self.mentee_data = []

        # --- Layout ---
        main_frame = ttk.Frame(self.tab_teams)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- Top Frame: Team List & Members List ---
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left: Team List
        team_list_frame = ttk.LabelFrame(list_frame, text="All Teams")
        team_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        team_cols = ("id", "name", "mentor", "created")
        self.team_tree = ttk.Treeview(team_list_frame, columns=team_cols, show="headings")
        self.team_tree.heading("id", text="ID")
        self.team_tree.heading("name", text="Team Name")
        self.team_tree.heading("mentor", text="Mentor")
        self.team_tree.heading("created", text="Created On")
        self.team_tree.column("id", width=40, anchor="center")
        self.team_tree.pack(fill=tk.BOTH, expand=True)
        self.team_tree.bind("<<TreeviewSelect>>", self.on_team_select)

        # Right: Team Members
        member_list_frame = ttk.LabelFrame(list_frame, text="Team Members")
        member_list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        member_cols = ("id", "name", "role")
        self.member_tree = ttk.Treeview(member_list_frame, columns=member_cols, show="headings")
        self.member_tree.heading("id", text="ID")
        self.member_tree.heading("name", text="Name")
        self.member_tree.heading("role", text="Role")
        self.member_tree.column("id", width=40, anchor="center")
        self.member_tree.pack(fill=tk.BOTH, expand=True)

        # --- Bottom Frame: Forms ---
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=10)

        # Left: Create Team
        create_team_frame = ttk.LabelFrame(form_frame, text="Create New Team", padding=10)
        create_team_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        ttk.Label(create_team_frame, text="Team Name:").grid(row=0, column=0, sticky="w")
        ttk.Entry(create_team_frame, textvariable=self.team_name_var, width=30).grid(row=0, column=1, pady=5)
        
        ttk.Label(create_team_frame, text="Select Mentor:").grid(row=1, column=0, sticky="w")
        self.team_mentor_combo = ttk.Combobox(create_team_frame, textvariable=self.team_mentor_var, width=28, state="readonly")
        self.team_mentor_combo.grid(row=1, column=1, pady=5)

        ttk.Label(create_team_frame, text="Select Mentees (Ctrl+Click):").grid(row=2, column=0, sticky="w")
        self.team_mentee_list = Listbox(create_team_frame, selectmode=tk.MULTIPLE, exportselection=False, height=5)
        self.team_mentee_list.grid(row=2, column=1, pady=5)
        
        ttk.Button(create_team_frame, text="Create Team", command=self.handle_create_team).grid(row=3, column=0, columnspan=2, pady=10)

        # Right: Add/Delete
        actions_frame = ttk.LabelFrame(form_frame, text="Team Actions", padding=10)
        actions_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Label(actions_frame, text="Note: Select a team from the list.").pack(pady=5)
        ttk.Button(actions_frame, text="Delete Selected Team", command=self.handle_delete_team).pack(fill=tk.X, pady=5)
        
        # --- Initial Load ---
        self.refresh_team_data()

    def refresh_team_data(self):
        """Helper to reload all data for the team tab."""
        # Store mentors and mentees
        self.mentor_data = db_manager.fetch_students_by_role('mentor')
        self.mentee_data = db_manager.fetch_students_by_role('mentee')
        
        # Populate dropdowns
        self.team_mentor_combo['values'] = [m['name'] for m in self.mentor_data]
        
        # Populate listbox
        self.team_mentee_list.delete(0, tk.END)
        for mentee in self.mentee_data:
            self.team_mentee_list.insert(tk.END, mentee['name'])
        
        # Populate team list
        self.populate_team_list()
        
        # Clear member list
        for row in self.member_tree.get_children(): self.member_tree.delete(row)

    def populate_team_list(self):
        for row in self.team_tree.get_children(): self.team_tree.delete(row)
        teams = db_manager.fetch_teams()
        if teams:
            for team in teams:
                self.team_tree.insert("", tk.END, values=(
                    team['team_id'], team['team_name'], 
                    team['mentor_name'], team['creation_date']
                ))

    def on_team_select(self, event):
        """When team is selected, show its members."""
        try:
            selected_item = self.team_tree.selection()[0]
            team_values = self.team_tree.item(selected_item, "values")
            self.selected_team_id = team_values[0]
            self.status_label.config(text=f"Selected team ID: {self.selected_team_id}")
            
            # Populate member list
            for row in self.member_tree.get_children(): self.member_tree.delete(row)
            members = db_manager.fetch_team_members(self.selected_team_id)
            for member in members:
                self.member_tree.insert("", tk.END, values=(
                    member['student_id'], member['name'], member['role']
                ))
        except IndexError: pass

    def handle_create_team(self):
        team_name = self.team_name_var.get()
        mentor_name = self.team_mentor_var.get()
        
        if not team_name or not mentor_name:
            messagebox.showwarning("Validation Error", "Team Name and Mentor are required.")
            return

        # Get mentor ID from name
        mentor_id = None
        for mentor in self.mentor_data:
            if mentor['name'] == mentor_name:
                mentor_id = mentor['student_id']
                break
        
        # Get mentee IDs from listbox selection
        selected_indices = self.team_mentee_list.curselection()
        mentee_ids = [self.mentee_data[i]['student_id'] for i in selected_indices]
        
        if db_manager.create_team(team_name, mentor_id, mentee_ids):
            self.status_label.config(text="Team created successfully!")
            self.refresh_team_data()
            self.team_name_var.set("")
            self.team_mentor_var.set("")
        else:
            self.status_label.config(text="Failed to create team.")

    def handle_delete_team(self):
        if self.selected_team_id is None:
            messagebox.showwarning("Delete Error", "Please select a team to delete.")
            return
            
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this team?"):
            if db_manager.delete_team(self.selected_team_id):
                self.status_label.config(text="Team deleted!")
                self.refresh_team_data()
                self.selected_team_id = None
            else:
                self.status_label.config(text="Failed to delete team.")

    # ===================================================================
    # --- 3. SESSION MANAGEMENT TAB ---
    # ===================================================================

    def create_session_tab(self):
        # --- Form Variables ---
        self.session_subject_var = tk.StringVar()
        self.session_datetime_var = tk.StringVar(value="YYYY-MM-DD HH:MM:SS")
        self.session_duration_var = tk.StringVar(value="60")
        self.session_mentor_var = tk.StringVar()
        self.session_status_var = tk.StringVar()
        self.selected_session_id = None

        # --- Store data for dropdowns ---
        self.subject_data = []
        # We can re-use self.mentor_data and self.mentee_data

        # --- Layout ---
        main_frame = ttk.Frame(self.tab_sessions)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- Top Frame: Session List & Participants List ---
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left: Session List
        session_list_frame = ttk.LabelFrame(list_frame, text="All Sessions")
        session_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        session_cols = ("id", "subject", "datetime", "duration", "status")
        self.session_tree = ttk.Treeview(session_list_frame, columns=session_cols, show="headings")
        self.session_tree.heading("id", text="ID")
        self.session_tree.heading("subject", text="Subject")
        self.session_tree.heading("datetime", text="Date & Time")
        self.session_tree.heading("duration", text="Duration (min)")
        self.session_tree.heading("status", text="Status")
        self.session_tree.column("id", width=40, anchor="center")
        self.session_tree.column("datetime", width=150)
        self.session_tree.pack(fill=tk.BOTH, expand=True)
        self.session_tree.bind("<<TreeviewSelect>>", self.on_session_select)

        # Right: Session Participants
        participant_list_frame = ttk.LabelFrame(list_frame, text="Session Participants")
        participant_list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        participant_cols = ("id", "name", "role")
        self.participant_tree = ttk.Treeview(participant_list_frame, columns=participant_cols, show="headings")
        self.participant_tree.heading("id", text="ID")
        self.participant_tree.heading("name", text="Name")
        self.participant_tree.heading("role", text="Role")
        self.participant_tree.column("id", width=40, anchor="center")
        self.participant_tree.pack(fill=tk.BOTH, expand=True)

        # --- Bottom Frame: Forms ---
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=10)

        # Left: Create Session
        create_session_frame = ttk.LabelFrame(form_frame, text="Schedule New Session", padding=10)
        create_session_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, anchor="n")

        ttk.Label(create_session_frame, text="Subject:").grid(row=0, column=0, sticky="w", pady=2)
        self.session_subject_combo = ttk.Combobox(create_session_frame, textvariable=self.session_subject_var, width=28, state="readonly")
        self.session_subject_combo.grid(row=0, column=1, pady=2)
        
        ttk.Label(create_session_frame, text="Date/Time:").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Entry(create_session_frame, textvariable=self.session_datetime_var, width=30).grid(row=1, column=1, pady=2)
        
        ttk.Label(create_session_frame, text="Duration (min):").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Entry(create_session_frame, textvariable=self.session_duration_var, width=30).grid(row=2, column=1, pady=2)

        ttk.Label(create_session_frame, text="Select Mentor:").grid(row=3, column=0, sticky="w", pady=2)
        self.session_mentor_combo = ttk.Combobox(create_session_frame, textvariable=self.session_mentor_var, width=28, state="readonly")
        self.session_mentor_combo.grid(row=3, column=1, pady=2)

        ttk.Label(create_session_frame, text="Select Mentees (Ctrl+Click):").grid(row=4, column=0, sticky="nw", pady=2)
        self.session_mentee_list = Listbox(create_session_frame, selectmode=tk.MULTIPLE, exportselection=False, height=5)
        self.session_mentee_list.grid(row=4, column=1, pady=2)
        
        ttk.Button(create_session_frame, text="Schedule Session", command=self.handle_schedule_session).grid(row=5, column=0, columnspan=2, pady=10)

        # Right: Session Actions
        actions_frame = ttk.LabelFrame(form_frame, text="Session Actions", padding=10)
        actions_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, anchor="n")
        
        ttk.Label(actions_frame, text="Select a session from the list.").pack(pady=5)
        ttk.Label(actions_frame, text="Set Status:").pack(pady=(10,0))
        self.session_status_combo = ttk.Combobox(actions_frame, textvariable=self.session_status_var, values=["scheduled", "completed", "cancelled"], state="readonly")
        self.session_status_combo.pack(pady=5, fill=tk.X)
        ttk.Button(actions_frame, text="Update Status", command=self.handle_update_status).pack(fill=tk.X, pady=5)
        
        ttk.Button(actions_frame, text="Cancel (Delete) Session", command=self.handle_cancel_session).pack(fill=tk.X, pady=(15, 5))
        
        # --- Initial Load ---
        self.refresh_session_data()

    def refresh_session_data(self):
        """Helper to reload all data for the session tab."""
        # Store data
        self.subject_data = db_manager.fetch_all_subjects()
        # We re-use mentor/mentee data from team tab, but refresh just in case
        self.mentor_data = db_manager.fetch_students_by_role('mentor')
        self.mentee_data = db_manager.fetch_students_by_role('mentee')

        # Populate dropdowns
        self.session_subject_combo['values'] = [s['subject_name'] for s in self.subject_data]
        self.session_mentor_combo['values'] = [m['name'] for m in self.mentor_data]
        
        # Populate listbox
        self.session_mentee_list.delete(0, tk.END)
        for mentee in self.mentee_data:
            self.session_mentee_list.insert(tk.END, mentee['name'])
        
        # Populate session list
        self.populate_session_list()
        
        # Clear participant list
        for row in self.participant_tree.get_children(): self.participant_tree.delete(row)
    
    def populate_session_list(self):
        for row in self.session_tree.get_children(): self.session_tree.delete(row)
        sessions = db_manager.fetch_sessions()
        if sessions:
            for session in sessions:
                self.session_tree.insert("", tk.END, values=(
                    session['session_id'], session['subject_name'], 
                    session['date_time'], session['duration'], session['status']
                ))
    
    def on_session_select(self, event):
        """When session is selected, show its participants and status."""
        try:
            selected_item = self.session_tree.selection()[0]
            session_values = self.session_tree.item(selected_item, "values")
            self.selected_session_id = session_values[0]
            self.session_status_var.set(session_values[4])
            self.status_label.config(text=f"Selected session ID: {self.selected_session_id}")
            
            # Populate participant list
            for row in self.participant_tree.get_children(): self.participant_tree.delete(row)
            participants = db_manager.fetch_session_participants(self.selected_session_id)
            for p in participants:
                self.participant_tree.insert("", tk.END, values=(
                    p['student_id'], p['name'], p['role']
                ))
        except IndexError: pass

    def handle_schedule_session(self):
        subject_name = self.session_subject_var.get()
        date_time = self.session_datetime_var.get()
        duration = self.session_duration_var.get()
        mentor_name = self.session_mentor_var.get()
        
        if not all([subject_name, date_time, duration, mentor_name]):
            messagebox.showwarning("Validation Error", "All fields are required.")
            return

        # Get Subject ID
        subject_id = next(s['subject_id'] for s in self.subject_data if s['subject_name'] == subject_name)
        # Get Mentor ID
        mentor_id = next(m['student_id'] for m in self.mentor_data if m['name'] == mentor_name)
        # Get Mentee IDs
        selected_indices = self.session_mentee_list.curselection()
        mentee_ids = [self.mentee_data[i]['student_id'] for i in selected_indices]
        # Convert list of IDs to comma-separated string for the stored procedure
        mentee_ids_str = ",".join(map(str, mentee_ids))

        if not mentee_ids_str:
             messagebox.showwarning("Validation Error", "At least one mentee must be selected.")
             return

        if db_manager.schedule_session(subject_id, date_time, int(duration), mentor_id, mentee_ids_str):
            self.status_label.config(text="Session scheduled successfully!")
            self.refresh_session_data()
        else:
            self.status_label.config(text="Failed to schedule session.")
            
    def handle_update_status(self):
        if self.selected_session_id is None:
            messagebox.showwarning("Update Error", "Please select a session to update.")
            return
        
        new_status = self.session_status_var.get()
        if not new_status:
            messagebox.showwarning("Update Error", "Please select a new status.")
            return

        if db_manager.update_session_status(self.selected_session_id, new_status):
            self.status_label.config(text="Session status updated!")
            self.refresh_session_data()
            self.selected_session_id = None
            self.session_status_var.set("")
        else:
            self.status_label.config(text="Failed to update status.")

    def handle_cancel_session(self):
        if self.selected_session_id is None:
            messagebox.showwarning("Delete Error", "Please select a session to cancel.")
            return
            
        if messagebox.askyesno("Confirm Cancel", "Are you sure you want to cancel (delete) this session?"):
            if db_manager.cancel_session(self.selected_session_id):
                self.status_label.config(text="Session cancelled (deleted).")
                self.refresh_session_data()
                self.selected_session_id = None
                self.session_status_var.set("")
            else:
                self.status_label.config(text="Failed to cancel session.")

# --- Run the App ---
if __name__ == "__main__":
    app = App()
    app.mainloop()
