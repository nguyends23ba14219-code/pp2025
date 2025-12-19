import math
import numpy as np

class MarkManager:
    def __init__(self):
        self.__marks = {}

    def add_mark(self, course_id, student_id, score):
        if course_id not in self.__marks:
            self.__marks[course_id] = {}
        self.__marks[course_id][student_id] = score

    def calculate_average_gpa(self, student, courses):
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