import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os
import pickle
import zipfile
import threading
import time
from domains import Student, Course, MarkManager

class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System (PW9)")
        self.root.geometry("600x400")

        self.students = []
        self.courses = []
        self.mark_manager = MarkManager()
      
        self.load_data()

        self.create_widgets()
    
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        btn_add_student = tk.Button(frame, text="Add Student", width=20, command=self.add_student)
        btn_add_student.grid(row=0, column=0, padx=10, pady=5)

        btn_add_course = tk.Button(frame, text="Add Course", width=20, command=self.add_course)
        btn_add_course.grid(row=0, column=1, padx=10, pady=5)

        btn_input_marks = tk.Button(frame, text="Input Marks", width=20, command=self.input_marks)
        btn_input_marks.grid(row=1, column=0, padx=10, pady=5)

        btn_list_students = tk.Button(frame, text="List Students (GPA Sorted)", width=20, command=self.list_students)
        btn_list_students.grid(row=1, column=1, padx=10, pady=5)

        btn_list_courses = tk.Button(frame, text="List Courses", width=20, command=self.list_courses)
        btn_list_courses.grid(row=2, column=0, padx=10, pady=5)

        btn_save = tk.Button(frame, text="Save (Background)", width=20, command=self.background_save)
        btn_save.grid(row=2, column=1, padx=10, pady=5)

        self.output_text = tk.Text(self.root, height=15, width=70)
        self.output_text.pack(pady=10)

    def load_data(self):
        if os.path.exists('students.dat'):
            try:
                with zipfile.ZipFile('students.dat', 'r') as zf:
                    zf.extractall()
                if os.path.exists('students.pkl'):
                    with open('students.pkl', 'rb') as f: self.students = pickle.load(f)
                    os.remove('students.pkl')
                if os.path.exists('courses.pkl'):
                    with open('courses.pkl', 'rb') as f: self.courses = pickle.load(f)
                    os.remove('courses.pkl')
                if os.path.exists('marks.pkl'):
                    with open('marks.pkl', 'rb') as f: self.mark_manager = pickle.load(f)
                    os.remove('marks.pkl')
            except Exception:
                pass

    def background_save(self):
        if self.status_var.get() == "Saving...":
            messagebox.showwarning("Warning", "Save already in progress!")
            return

        def save_task():
            self.status_var.set("Saving...")
            try:
                time.sleep(2) 
                with open('students.pkl', 'wb') as f: pickle.dump(self.students, f)
                with open('courses.pkl', 'wb') as f: pickle.dump(self.courses, f)
                with open('marks.pkl', 'wb') as f: pickle.dump(self.mark_manager, f)

                with zipfile.ZipFile('students.dat', 'w', zipfile.ZIP_DEFLATED) as zf:
                    zf.write('students.pkl')
                    zf.write('courses.pkl')
                    zf.write('marks.pkl')
                
                if os.path.exists('students.pkl'): os.remove('students.pkl')
                if os.path.exists('courses.pkl'): os.remove('courses.pkl')
                if os.path.exists('marks.pkl'): os.remove('marks.pkl')
                
                self.status_var.set("Save Complete!")
                time.sleep(2)
                self.status_var.set("Ready")
            except Exception as e:
                self.status_var.set(f"Error: {e}")

        t = threading.Thread(target=save_task)
        t.start()


    def add_student(self):
        top = tk.Toplevel(self.root)
        top.title("Add Student")
        
        tk.Label(top, text="ID:").grid(row=0, column=0)
        e_id = tk.Entry(top)
        e_id.grid(row=0, column=1)
        
        tk.Label(top, text="Name:").grid(row=1, column=0)
        e_name = tk.Entry(top)
        e_name.grid(row=1, column=1)
        
        tk.Label(top, text="DOB:").grid(row=2, column=0)
        e_dob = tk.Entry(top)
        e_dob.grid(row=2, column=1)

        def save():
            sid, name, dob = e_id.get(), e_name.get(), e_dob.get()
            if sid and name:
                self.students.append(Student(sid, name, dob))
                messagebox.showinfo("Success", "Student added!")
                top.destroy()
            else:
                messagebox.showerror("Error", "ID and Name required")

        tk.Button(top, text="Save", command=save).grid(row=3, columnspan=2)

    def add_course(self):
        top = tk.Toplevel(self.root)
        top.title("Add Course")
        
        tk.Label(top, text="ID:").grid(row=0, column=0)
        e_id = tk.Entry(top)
        e_id.grid(row=0, column=1)
        
        tk.Label(top, text="Name:").grid(row=1, column=0)
        e_name = tk.Entry(top)
        e_name.grid(row=1, column=1)
        
        tk.Label(top, text="Credits:").grid(row=2, column=0)
        e_cred = tk.Entry(top)
        e_cred.grid(row=2, column=1)

        def save():
            cid, name, cred = e_id.get(), e_name.get(), e_cred.get()
            try:
                cred_val = float(cred)
                self.courses.append(Course(cid, name, cred_val))
                messagebox.showinfo("Success", "Course added!")
                top.destroy()
            except ValueError:
                messagebox.showerror("Error", "Credits must be a number")

        tk.Button(top, text="Save", command=save).grid(row=3, columnspan=2)

    def input_marks(self):
        if not self.courses or not self.students:
            messagebox.showerror("Error", "Need students and courses first!")
            return
            
        cid = simpledialog.askstring("Input", "Enter Course ID:")
        course = next((c for c in self.courses if c.get_id() == cid), None)
        
        if not course:
            messagebox.showerror("Error", "Course not found")
            return
        
        for s in self.students:
            score_str = simpledialog.askstring("Mark", f"Enter mark for {s.get_name()}:")
            if score_str:
                try:
                    val = float(score_str)
                    import math
                    val = math.floor(val * 10) / 10
                    self.mark_manager.add_mark(cid, s.get_id(), val)
                except ValueError:
                    pass
        messagebox.showinfo("Info", "Marks entry finished.")

    def list_students(self):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "--- Student List (GPA Sorted) ---\n")
        
        for s in self.students:
            self.mark_manager.calculate_average_gpa(s, self.courses)
        
        sorted_students = sorted(self.students, key=lambda x: x.get_gpa(), reverse=True)
        
        for s in sorted_students:
            self.output_text.insert(tk.END, str(s) + "\n")

    def list_courses(self):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "--- Course List ---\n")
        for c in self.courses:
            self.output_text.insert(tk.END, str(c) + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()