import curses
import input as ui_in
import output as ui_out
from domains import Student, Course, MarkManager

def main(stdscr):
    # Curses Setup
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
        ui_out.draw_menu(stdscr, current_row, menu_items)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            
            if current_row == 0:
                stdscr.clear()
                num = ui_in.get_int(stdscr, 2, 2, "Number of students: ")
                if num:
                    for i in range(num):
                        sid = ui_in.get_str(stdscr, 4+i*3, 2, "ID: ")
                        name = ui_in.get_str(stdscr, 5+i*3, 2, "Name: ")
                        dob = ui_in.get_str(stdscr, 6+i*3, 2, "DOB: ")
                        students.append(Student(sid, name, dob))
                    ui_out.print_message(stdscr, 10+num*3, 2, "Added! Press key...")
                else:
                    ui_out.print_message(stdscr, 4, 2, "Invalid input. Press key...")
                ui_out.wait_key(stdscr)

            elif current_row == 1: 
                stdscr.clear()
                num = ui_in.get_int(stdscr, 2, 2, "Number of courses: ")
                if num:
                    for i in range(num):
                        cid = ui_in.get_str(stdscr, 4+i*3, 2, "ID: ")
                        name = ui_in.get_str(stdscr, 5+i*3, 2, "Name: ")
                        cred = ui_in.get_float(stdscr, 6+i*3, 2, "Credits: ")
                        if cred:
                            courses.append(Course(cid, name, cred))
                    ui_out.print_message(stdscr, 10+num*3, 2, "Added! Press key...")
                else:
                    ui_out.print_message(stdscr, 4, 2, "Invalid input. Press key...")
                ui_out.wait_key(stdscr)

            elif current_row == 2: 
                stdscr.clear()
                if not courses or not students:
                    ui_out.print_message(stdscr, 2, 2, "No data. Press key...")
                    ui_out.wait_key(stdscr)
                    continue

                ui_out.print_message(stdscr, 2, 2, "Available Courses:")
                for idx, c in enumerate(courses):
                    ui_out.print_message(stdscr, 3+idx, 4, str(c))
                
                cid_in = ui_in.get_str(stdscr, 5+len(courses), 2, "Enter Course ID: ")
                selected_course = next((c for c in courses if c.get_id() == cid_in), None)
                
                if selected_course:
                    row = 7 + len(courses)
                    for s in students:
                        score = ui_in.get_rounded_mark(stdscr, row, 2, f"Mark for {s.get_name()}: ")
                        if score is not None:
                            mark_manager.add_mark(cid_in, s.get_id(), score)
                            row += 1
                    ui_out.print_message(stdscr, row+1, 2, "Saved. Press key...")
                else:
                    ui_out.print_message(stdscr, 7+len(courses), 2, "Not found. Press key...")
                ui_out.wait_key(stdscr)

            elif current_row == 3: 
                
                for s in students:
                    mark_manager.calculate_average_gpa(s, courses)
               
                students.sort(key=lambda x: x.get_gpa(), reverse=True)
                ui_out.list_items(stdscr, students, "Student List (Sorted by GPA)")

            elif current_row == 4: 
                ui_out.list_items(stdscr, courses, "Course List")

            elif current_row == 5: 
                break

if __name__ == "__main__":
    curses.wrapper(main)