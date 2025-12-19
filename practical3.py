import math
import numpy as np
import curses

class Student:
    def __init__(self, s_id, name, dob):
        self.__id = s_id
        self.__name = name
        self.__dob = dob
        self.__gpa = 0.0

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def set_gpa(self, gpa):
        self.__gpa = gpa

    def get_gpa(self):
        return self.__gpa

    def __str__(self):
        return f"ID: {self.__id} | Name: {self.__name} | DoB: {self.__dob} | GPA: {self.__gpa:.2f}"

class Course:
    def __init__(self, c_id, name, credits):
        self.__id = c_id
        self.__name = name
        self.__credits = credits

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_credits(self):
        return self.__credits

    def __str__(self):
        return f"ID: {self.__id} | Name: {self.__name} | Credits: {self.__credits}"

class MarkManager:
    def __init__(self):
        self.__marks = {}

    def add_mark(self, course_id, student_id, score):
        if course_id not in self.__marks:
            self.__marks[course_id] = {}
        self.__marks[course_id][student_id] = score

    def get_marks_for_course(self, course_id):
        return self.__marks.get(course_id, {})

    def calculate_average_gpa(self, student, courses):
        """
        Calculates GPA using numpy for weighted sum.
        """
        total_scores = []
        total_credits = []

        for course in courses:
            cid = course.get_id()
            marks_in_course = self.__marks.get(cid, {})
            
            if student.get_id() in marks_in_course:
                score = marks_in_course[student.get_id()]
                credit = course.get_credits()
                
                total_scores.append(score)
                total_credits.append(credit)

        if len(total_scores) > 0:
            np_scores = np.array(total_scores)
            np_credits = np.array(total_credits)
            gpa = np.average(np_scores, weights=np_credits)
            student.set_gpa(gpa)
        else:
            student.set_gpa(0.0)


def get_input(stdscr, r, c, prompt):
    """
    Helper to get string input in curses.
    """
    stdscr.addstr(r, c, prompt)
    curses.echo() 
    input_bytes = stdscr.getstr(r, c + len(prompt), 20)
    curses.noecho()
    return input_bytes.decode('utf-8')

def draw_menu(stdscr, selected_idx, menu_items):
    h, w = stdscr.getmaxyx()
    for idx, item in enumerate(menu_items):
        x = w//2 - len(item)//2
        y = h//2 - len(menu_items)//2 + idx
        if idx == selected_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, item)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, item)
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0) 
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) 

    students = []
    courses = []
    mark_manager = MarkManager()

    menu_items = [
        "1. Add Students",
        "2. Add Courses",
        "3. Input Marks",
        "4. List Students (Sorted by GPA)",
        "5. List Courses",
        "6. Exit"
    ]
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(1, 1, "Student Management System (Use Up/Down + Enter)")
        
        draw_menu(stdscr, current_row, menu_items)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
                
            if current_row == 0:
                stdscr.clear()
                try:
                    num_s = int(get_input(stdscr, 2, 2, "Number of students: "))
                    for i in range(num_s):
                        sid = get_input(stdscr, 4+i*3, 2, "ID: ")
                        name = get_input(stdscr, 5+i*3, 2, "Name: ")
                        dob = get_input(stdscr, 6+i*3, 2, "DOB: ")
                        students.append(Student(sid, name, dob))
                    stdscr.addstr(10+num_s*3, 2, "Students added! Press any key...")
                except ValueError:
                    stdscr.addstr(4, 2, "Invalid number. Press any key...")
                stdscr.getch()

            elif current_row == 1:
                stdscr.clear()
                try:
                    num_c = int(get_input(stdscr, 2, 2, "Number of courses: "))
                    for i in range(num_c):
                        cid = get_input(stdscr, 4+i*3, 2, "ID: ")
                        name = get_input(stdscr, 5+i*3, 2, "Name: ")
                        cred = float(get_input(stdscr, 6+i*3, 2, "Credits: ")) 
                        courses.append(Course(cid, name, cred))
                    stdscr.addstr(10+num_c*3, 2, "Courses added! Press any key...")
                except ValueError:
                    stdscr.addstr(4, 2, "Invalid input. Press any key...")
                stdscr.getch()

            elif current_row == 2:
                stdscr.clear()
                if not courses or not students:
                    stdscr.addstr(2, 2, "Please add students and courses first. Press any key...")
                    stdscr.getch()
                    continue

                stdscr.addstr(2, 2, "Available Courses:")
                for idx, c in enumerate(courses):
                    stdscr.addstr(3+idx, 4, c.__str__())
                
                cid_in = get_input(stdscr, 5+len(courses), 2, "Enter Course ID: ")
                
                selected_course = next((c for c in courses if c.get_id() == cid_in), None)
                
                if selected_course:
                    stdscr.addstr(7+len(courses), 2, f"Entering marks for {selected_course.get_name()}")
                    row_offset = 9 + len(courses)
                    
                    for s in students:
                        raw_score_str = get_input(stdscr, row_offset, 2, f"Mark for {s.get_name()}: ")
                        try:
                            val = float(raw_score_str)
    
                            processed_score = math.floor(val * 10) / 10
                            mark_manager.add_mark(cid_in, s.get_id(), processed_score)
                            row_offset += 1
                        except ValueError:
                            pass 
                    stdscr.addstr(row_offset + 1, 2, "Marks saved. Press any key...")
                else:
                    stdscr.addstr(7+len(courses), 2, "Course not found. Press any key...")
                stdscr.getch()

            elif current_row == 3: 
                stdscr.clear()
                stdscr.addstr(2, 2, "--- Student List (Sorted by GPA Descending) ---")
            
                for s in students:
                    mark_manager.calculate_average_gpa(s, courses)
                
                students.sort(key=lambda x: x.get_gpa(), reverse=True)

                for idx, s in enumerate(students):
                    stdscr.addstr(4+idx, 4, str(s))
                
                stdscr.addstr(6+len(students), 2, "Press any key to return...")
                stdscr.getch()

            elif current_row == 4: 
                stdscr.clear()
                stdscr.addstr(2, 2, "--- Course List ---")
                for idx, c in enumerate(courses):
                    stdscr.addstr(4+idx, 4, str(c))
                stdscr.addstr(6+len(courses), 2, "Press any key to return...")
                stdscr.getch()

            elif current_row == 5: 
                break

if __name__ == "__main__":
    curses.wrapper(main)