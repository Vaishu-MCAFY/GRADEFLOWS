from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.faculty_login,
        name="login"
    ),

    path(
        "logout/",
        views.faculty_logout,
        name="logout"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "students/",
        views.student_list,
        name="student_list"
    ),

    path(
        "students/add/",
        views.add_student,
        name="add_student"
    ),

    path(
        "students/edit/<int:pk>/",
        views.update_student,
        name="update_student"
    ),

    path(
        "students/delete/<int:pk>/",
        views.delete_student,
        name="delete_student"
    ),

    path(
        "upload/",
        views.upload_csv,
        name="upload_csv"
    ),
    path(
        "reports/<int:pk>/",
        views.individual_report,
        name="individual_report"
    ),

    path(
        "reports/bulk/",
        views.bulk_reports,
        name="bulk_reports"
    ),
    path(
        "analytics/",
        views.analytics,
        name="analytics"
    ),
    path(
        "api/students/",
        views.student_api,
        name="student_api"
    ),

    path(
        "api/students/<int:pk>/",
        views.student_detail_api,
        name="student_detail_api"
    ),

]
