from django.db import models


class Student(models.Model):

    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)

    subject1 = models.FloatField(default=0)
    subject2 = models.FloatField(default=0)
    subject3 = models.FloatField(default=0)
    subject4 = models.FloatField(default=0)
    subject5 = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["student_id"]

    def total_marks(self):
        return (
            self.subject1 +
            self.subject2 +
            self.subject3 +
            self.subject4 +
            self.subject5
        )

    def average_marks(self):
        return round(self.total_marks() / 5, 2)

    def highest_mark(self):
        return max(
            self.subject1,
            self.subject2,
            self.subject3,
            self.subject4,
            self.subject5,
        )

    def lowest_mark(self):
        return min(
            self.subject1,
            self.subject2,
            self.subject3,
            self.subject4,
            self.subject5,
        )

    def grade(self):
        avg = self.average_marks()

        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 40:
            return "D"
        else:
            return "F"

    def result(self):
        marks = [
            self.subject1,
            self.subject2,
            self.subject3,
            self.subject4,
            self.subject5,
        ]

        if min(marks) < 40:
            return "Fail"
        return "Pass"

    def is_at_risk(self):
        return self.average_marks() < 40

    def __str__(self):
        return f"{self.student_id} - {self.name}"


class Report:
    """
    Report class (OOP)

    Generates a report dictionary for a student.
    """

    def __init__(self, student):
        self.student = student

    def generate(self):
        return {
            "Student ID": self.student.student_id,
            "Name": self.student.name,
            "Department": self.student.department,
            "Email": self.student.email,
            "Total": self.student.total_marks(),
            "Average": self.student.average_marks(),
            "Highest": self.student.highest_mark(),
            "Lowest": self.student.lowest_mark(),
            "Grade": self.student.grade(),
            "Result": self.student.result(),
        }