import csv
import math
import re

from .exceptions import InvalidMarksException, validate_marks

STUDENT_ID_PATTERN = r"^ST\d{3,6}$"
EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

def validate_student_id(student_id):
    """
    Validate Student ID.
    """

    if re.fullmatch(STUDENT_ID_PATTERN, student_id):
        return True

    return False

def validate_email(email):
    """
    Validate Email Address.
    """

    if re.fullmatch(EMAIL_PATTERN, email):
        return True

    return False

def calculate_statistics(marks):
    """
    Calculate statistics using the math module.
    """

    if not marks:
        return {
            "average": 0,
            "highest": 0,
            "lowest": 0,
            "total": 0,
            "sqrt_average": 0
        }

    average = sum(marks) / len(marks)

    return {
        "average": round(average, 2),
        "highest": max(marks),
        "lowest": min(marks),
        "total": sum(marks),
        "sqrt_average": round(math.sqrt(average), 2)
    }

def calculate_grade(average):

    if average >= 90:
        return "A+"

    elif average >= 80:
        return "A"

    elif average >= 70:
        return "B"

    elif average >= 60:
        return "C"

    elif average >= 40:
        return "D"

    return "F"

def get_result(marks):

    if min(marks) < 40:
        return "Fail"

    return "Pass"

def read_csv(file_path):
    """
    Read student records from CSV file.
    """

    students = []

    with open(file_path, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            marks = [
                float(row["subject1"]),
                float(row["subject2"]),
                float(row["subject3"]),
                float(row["subject4"]),
                float(row["subject5"]),
            ]

            validate_marks(*marks)

            average = sum(marks) / len(marks)

            row["average"] = round(average, 2)
            row["grade"] = calculate_grade(average)
            row["result"] = get_result(marks)

            students.append(row)

    return students

def sort_students_by_rank(student_list):
    """
    Sort students by average marks.
    """

    return sorted(
        student_list,
        key=lambda student: float(student["average"]),
        reverse=True
    )

def get_at_risk_students(student_list):
    """
    Students having average below 40.
    """

    return [
        student
        for student in student_list
        if float(student["average"]) < 40
    ]

def student_to_dict(student):

    marks = [
        student.subject1,
        student.subject2,
        student.subject3,
        student.subject4,
        student.subject5,
    ]

    average = sum(marks) / len(marks)

    return {
        "student_id": student.student_id,
        "name": student.name,
        "email": student.email,
        "department": student.department,
        "subject1": student.subject1,
        "subject2": student.subject2,
        "subject3": student.subject3,
        "subject4": student.subject4,
        "subject5": student.subject5,
        "average": round(average, 2),
        "grade": calculate_grade(average),
        "result": get_result(marks),
    }