class Student:
    def __init__(self):
        self.__id = ""
        self.__name = ""
        self.__dob = ""

    def input(self):
        self.__id = input("Enter student ID: ")
        self.__name = input("Enter student name: ")
        self.__dob = input("Enter date of birth: ")

    def list(self):
        print(f"{self.__id} - {self.__name} - {self.__dob}")

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

class Course:
    def __init__(self):
        self.__id = ""
        self.__name = ""

    def input(self):
        self.__id = input("Enter course ID: ")
        self.__name = input("Enter course name: ")

    def list(self):
        print(f"{self.__id} - {self.__name}")

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

class MarkManager:
    def __init__(self):
        self.__marks = {}  

    def input(self, students, courses):
        print("Available courses:")
        for c in courses:
            c.list()

        cid = input("Enter course ID to input marks: ")

        if cid not in [c.get_id() for c in courses]:
            print("Course not found!")
            return

        if cid not in self.__marks:
            self.__marks[cid] = {}

        print("Enter marks for each student:")
        for s in students:
            score = float(input(f"Enter mark for {s.get_name()}: "))
            self.__marks[cid][s.get_id()] = score

    def list(self, students, courses):
        print("Available courses:")
        for c in courses:
            c.list()

        cid = input("Enter course ID to show marks: ")

        if cid not in self.__marks:
            print("No marks recorded for this course.")
            return

        print(f"Marks for course {cid}:")
        for s in students:
            sid = s.get_id()
            if sid in self.__marks[cid]:
                print(f"{s.get_name()} ({sid}) : {self.__marks[cid][sid]}")

def main():
    students = []
    courses = []
    mark_manager = MarkManager()

    n = int(input("Enter number of students: "))
    for _ in range(n):
        stu = Student()
        stu.input()
        students.append(stu)

    m = int(input("Enter number of courses: "))
    for _ in range(m):
        c = Course()
        c.input()
        courses.append(c)

    while True:
        print("\n===== MENU =====")
        print("1. List students")
        print("2. List courses")
        print("3. Input marks")
        print("4. Show marks")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            print("\nList of Students:")
            for s in students:
                s.list()

        elif choice == '2':
            print("\nList of Courses:")
            for c in courses:
                c.list()

        elif choice == '3':
            mark_manager.input(students, courses)

        elif choice == '4':
            mark_manager.list(students, courses)

        elif choice == '5':
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
