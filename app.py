import tkinter as tk
from tkinter import ttk, messagebox
import db_manager  # Import our new backend file

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Peer Tutoring Management")
        self.geometry("1000x700")

        self.student_form_vars = {
            "name": tk.StringVar(),
            "email": tk.StringVar(),
            "ph_no": tk.StringVar(),
            "dept": tk.StringVar(),
            "year": tk.StringVar(),
            "role": tk.StringVar(value="mentee") # Default value
        }
        self.selected_student_id = None

        self.create_widgets()
        self.populate_student_list()

    def create_widgets(self):
        # --- Main Layout ---
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Top Frame: Student Table ---
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "name", "email", "phone", "dept", "year", "role")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        # Define headings
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("dept", text="Department")
        self.tree.heading("year", text="Year")
        self.tree.heading("role", text="Role")

        # Set column widths
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("name", width=150)
        self.tree.column("email", width=200)
        self.tree.column("phone", width=100)
        self.tree.column("dept", width=80)
        self.tree.column("year", width=50, anchor="center")
        self.tree.column("role", width=80)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # --- Bind click event ---
        # This will call 'on_student_select' when a row is clicked
        self.tree.bind("<<TreeviewSelect>>", self.on_student_select)

        # --- Bottom Frame: Student Form ---
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
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)

        # --- Status Bar ---
        self.status_label = ttk.Label(self, text="Ready", relief=tk.SUNKEN, anchor="w")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    # --- GUI Functions ---

    def populate_student_list(self):
        """Fetches student data and populates the tree."""
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        # Fetch new data
        students = db_manager.fetch_students()
        if students:
            for student in students:
                self.tree.insert("", tk.END, values=(
                    student['student_id'],
                    student['name'],
                    student['email'],
                    student['ph_no'],
                    student['dept'],
                    student['year'],
                    student['role']
                ))
            self.status_label.config(text=f"Loaded {len(students)} students.")
        else:
            self.status_label.config(text="No students found.")

    def on_student_select(self, event):
        """Called when a user clicks a row. Fills the form with data."""
        try:
            selected_item = self.tree.selection()[0]
            student = self.tree.item(selected_item, "values")
            
            self.selected_student_id = student[0]
            self.student_form_vars["name"].set(student[1])
            self.student_form_vars["email"].set(student[2])
            self.student_form_vars["ph_no"].set(student[3])
            self.student_form_vars["dept"].set(student[4])
            self.student_form_vars["year"].set(student[5])
            self.student_form_vars["role"].set(student[6])
            
            self.status_label.config(text=f"Selected student ID: {self.selected_student_id}")
        except IndexError:
            # Clicked on empty space
            pass

    def clear_form(self):
        """Clears all form fields."""
        for var in self.student_form_vars.values():
            var.set("")
        self.student_form_vars["role"].set("mentee") # Reset to default
        self.selected_student_id = None
        self.status_label.config(text="Form cleared. Ready.")

    def handle_add_student(self):
        """Gathers form data and calls the db_manager to add a student."""
        data = {key: var.get() for key, var in self.student_form_vars.items()}
        
        if not data["name"] or not data["email"]:
            messagebox.showwarning("Validation Error", "Name and Email are required.")
            return

        if db_manager.add_student(data):
            self.status_label.config(text="Student added successfully!")
            self.populate_student_list()
            self.clear_form()
        else:
            self.status_label.config(text="Failed to add student.")

    def handle_update_student(self):
        """Gathers form data and calls the db_manager to update."""
        if self.selected_student_id is None:
            messagebox.showwarning("Update Error", "Please select a student from the list to update.")
            return
            
        data = {key: var.get() for key, var in self.student_form_vars.items()}
        data["student_id"] = self.selected_student_id

        if db_manager.update_student(data):
            self.status_label.config(text="Student updated successfully!")
            self.populate_student_list()
            self.clear_form()
        else:
            self.status_label.config(text="Failed to update student.")

    def handle_delete_student(self):
        """Calls the db_manager to delete the selected student."""
        if self.selected_student_id is None:
            messagebox.showwarning("Delete Error", "Please select a student from the list to delete.")
            return
            
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student ID {self.selected_student_id}?"):
            if db_manager.delete_student(self.selected_student_id):
                self.status_label.config(text="Student deleted successfully!")
                self.populate_student_list()
                self.clear_form()
            else:
                self.status_label.config(text="Failed to delete student.")

# --- Run the App ---
if __name__ == "__main__":
    app = App()
    app.mainloop()