import csv
import math

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import StudentSerializer
from .threads import (
    generate_bulk_reports,
    generate_dashboard_report,
)

from .models import Student
from .forms import (
    FacultyLoginForm,
    StudentForm,
    CSVUploadForm,
)

from .db import (
    dashboard_statistics,
)

from .utils import (
    validate_student_id,
    validate_email,
)

from .exceptions import InvalidMarksException
from .threads import generate_bulk_reports
def faculty_login(request):
    """
    Faculty Login Page
    """

    if request.user.is_authenticated:
        return redirect("dashboard")

    form = FacultyLoginForm()

    if request.method == "POST":

        form = FacultyLoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                messages.success(
                    request,
                    "Login Successful."
                )

                return redirect("dashboard")

            else:

                messages.error(
                    request,
                    "Invalid Username or Password."
                )

    return render(
        request,
        "login.html",
        {
            "form": form
        }
    )

@login_required(login_url="login")
def faculty_logout(request):
    """
    Logout Faculty
    """

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("login")

@login_required(login_url="login")
def dashboard(request):
    """
    Faculty Dashboard
    """

    students = Student.objects.all()

    total_students = students.count()

    if total_students > 0:

        topper = max(
            students,
            key=lambda student: student.average_marks()
        )

        averages = [
            student.average_marks()
            for student in students
        ]

        class_average = round(
            sum(averages) / len(averages),
            2
        )

        failed_students = len([
            student
            for student in students
            if student.result() == "Fail"
        ])

        at_risk_students = len([
            student
            for student in students
            if student.is_at_risk()
        ])

        pass_percentage = round(
            ((total_students - failed_students) / total_students) * 100,
            2
        )

    else:

        topper = None
        class_average = 0
        failed_students = 0
        at_risk_students = 0
        pass_percentage = 0

    context = {

        "total_students": total_students,

        "topper": topper,

        "average_marks": class_average,

        "failed_students": failed_students,

        "at_risk_students": at_risk_students,

        "pass_percentage": pass_percentage,
    }

    return render(
        request,
        "dashboard.html",
        context
    )
@login_required(login_url="login")
def student_list(request):
    """
    Display all students with search and department filter.
    """

    students = Student.objects.all().order_by("student_id")

    search = request.GET.get("search", "")
    department = request.GET.get("department", "")

    if search:
        students = students.filter(
            student_id__icontains=search
        ) | students.filter(
            name__icontains=search
        ) | students.filter(
            email__icontains=search
        )
    if department:
        students = students.filter(department=department)

    departments = (
        Student.objects.values_list(
            "department",
            flat=True
        )
        .distinct()
        .order_by("department")
    )

    context = {
        "students": students,
        "departments": departments,
        "search": search,
        "selected_department": department,
    }

    return render(
        request,
        "student_list.html",
        context
    )

@login_required(login_url="login")
def add_student(request):
    """
    Add a new student.
    """

    if request.method == "POST":

        form = StudentForm(request.POST)

        if form.is_valid():

            student = form.save()

            messages.success(
                request,
                f"{student.name} added successfully."
            )

            return redirect("student_list")

        else:

            messages.error(
                request,
                "Please correct the errors below."
            )

    else:

        form = StudentForm()

    return render(
        request,
        "student_form.html",
        {
            "form": form,
            "title": "Add Student",
            "button": "Save Student",
        }
    )
@login_required(login_url="login")
def update_student(request, pk):
    """
    Update student details.
    """

    student = Student.objects.get(pk=pk)

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Student updated successfully."
            )

            return redirect("student_list")

        else:

            messages.error(
                request,
                "Please correct the errors below."
            )

    else:

        form = StudentForm(instance=student)

    return render(
        request,
        "student_form.html",
        {
            "form": form,
            "title": "Update Student",
            "button": "Update Student",
        }
    )
@login_required(login_url="login")
def delete_student(request, pk):
    """
    Delete a student.
    """

    student = Student.objects.get(pk=pk)

    if request.method == "POST":

        student_name = student.name

        student.delete()

        messages.success(
            request,
            f"{student_name} deleted successfully."
        )

        return redirect("student_list")

    return render(
        request,
        "student_confirm_delete.html",
        {
            "student": student,
        }
    )

@login_required(login_url="login")
def upload_csv(request):
    """
    Upload student records from CSV.
    """

    form = CSVUploadForm()

    if request.method == "POST":

        form = CSVUploadForm(request.POST, request.FILES)

        if form.is_valid():

            csv_file = request.FILES["csv_file"]

            decoded_file = csv_file.read().decode("utf-8").splitlines()

            reader = csv.DictReader(decoded_file)

            count = 0

            for row in reader:

                Student.objects.create(

                    student_id=row["student_id"],

                    name=row["name"],

                    email=row["email"],

                    department=row["department"],

                    subject1=float(row["subject1"]),

                    subject2=float(row["subject2"]),

                    subject3=float(row["subject3"]),

                    subject4=float(row["subject4"]),

                    subject5=float(row["subject5"]),
                )

                count += 1

            messages.success(
                request,
                f"{count} students uploaded successfully."
            )

            return redirect("student_list")

    return render(
        request,
        "upload_csv.html",
        {
            "form": form
        }
    )

@login_required(login_url="login")
def individual_report(request, pk):
    """
    Show report for a single student.
    """

    student = Student.objects.get(pk=pk)

    context = {

        "student": student,

        "total": student.total_marks(),

        "average": student.average_marks(),

        "highest": student.highest_mark(),

        "lowest": student.lowest_mark(),

        "grade": student.grade(),

        "result": student.result(),
    }

    return render(
        request,
        "reports.html",
        context
    )
@login_required(login_url="login")
def bulk_reports(request):
    """
    Generate reports for all students using threading.
    """

    students = Student.objects.all()

    generate_bulk_reports(students)

    messages.success(
        request,
        "Bulk reports generated successfully."
    )

    return redirect("dashboard")

@login_required(login_url="login")
def analytics(request):
    """
    Analytics Dashboard.
    """

    students = Student.objects.all()

    total_students = students.count()

    passed = len([
        s for s in students
        if s.result() == "Pass"
    ])

    failed = len([
        s for s in students
        if s.result() == "Fail"
    ])

    at_risk = len([
        s for s in students
        if s.is_at_risk()
    ])

    topper = None

    if total_students > 0:

        topper = max(
            students,
            key=lambda x: x.average_marks()
        )

    statistics = {

        "total_students": total_students,

        "passed_students": passed,

        "failed_students": failed,

        "at_risk_students": at_risk,

        "topper": topper.name if topper else "N/A",
    }

    generate_dashboard_report(statistics)

    return render(
        request,
        "analytics.html",
        statistics
    )

@api_view(["GET"])
def student_api(request):
    """
    Export all students as JSON.
    """

    students = Student.objects.all()

    serializer = StudentSerializer(
        students,
        many=True
    )

    return Response(serializer.data)

@api_view(["GET"])
def student_detail_api(request, pk):
    """
    Export one student as JSON.
    """

    student = Student.objects.get(pk=pk)

    serializer = StudentSerializer(student)

    return Response(serializer.data)