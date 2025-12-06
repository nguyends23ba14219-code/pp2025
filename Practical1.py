def number_of_students():
    n = int(input("Enter the number of students: "))
    return n


def info_of_students(n):
    students = []
    for i in range(n):
        sid = input("Enter ID of student: ")
        name = input("Enter name of student: ")
        dob = input("Enter date of birth: ")
        students.append({"ID": sid, "Name": name, "DoB": dob})
    return students


def number_of_course():
    m = int(input("Enter the number of courses: "))
    return m


def course_info(m):
    courses = []
    for i in range(m):
        cid = input("Enter ID of course: ")
        name = input("Enter name of course: ")
        courses.append({"ID": cid, "Name": name})
    return courses


def input_mark(students, courses, mark):
    print("Available courses:")
    for c in courses:
        print(f"{c['ID']}: {c['Name']}")

    cid = input("Enter ID of course: ")

    if not any(c["ID"] == cid for c in courses):
        print("Course not found.")
        return mark

    if cid not in mark:
        mark[cid] = {}

    print("Input marks for students:")
    for stu in students:
        score = float(input(f"Enter mark for {stu['Name']}: "))
        mark[cid][stu["ID"]] = score

    return mark


def list_course(courses):
    print("List of courses:")
    for c in courses:
        print(f"{c['ID']} : {c['Name']}")


def list_students(students):
    print("List of students:")
    for stu in students:
        print(f"{stu['ID']} : {stu['Name']} : {stu['DoB']}")


def show_mark(mark, students, courses):
    print("Available courses:")
    for c in courses:
        print(f"{c['ID']} : {c['Name']}")

    cid = input("Enter ID of course: ")

    if cid not in mark:
        print("No marks available for this course.")
        return

    print(f"Marks for course {cid}:")
    course_mark = mark[cid]
    for stu in students:
        sid = stu["ID"]
        if sid in course_mark:
            print(f"{stu['Name']} ({sid}) : {course_mark[sid]}")


def main():
    n = number_of_students()
    students = info_of_students(n)

    m = number_of_course()
    courses = course_info(m)

    mark = {}

    while True:
        print("\nMenu:")
        print("1. List of students")
        print("2. List of courses")
        print("3. Input mark")
        print("4. Show mark for a course")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            list_students(students)
        elif choice == '2':
            list_course(courses)
        elif choice == '3':
            mark = input_mark(students, courses, mark)
        elif choice == '4':
            show_mark(mark, students, courses)
        elif choice == '5':
            break


if __name__ == "__main__":
    main()
