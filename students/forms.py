from django import forms

from .models import Student
from .utils import (
    validate_student_id,
    validate_email,
)
from .exceptions import (
    validate_marks,
    InvalidMarksException,
)


class FacultyLoginForm(forms.Form):

    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Username"
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Password"
            }
        )
    )


class StudentForm(forms.ModelForm):

    class Meta:

        model = Student

        fields = [
            "student_id",
            "name",
            "email",
            "department",
            "subject1",
            "subject2",
            "subject3",
            "subject4",
            "subject5",
        ]

        widgets = {

            "student_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Student ID"
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Student Name"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email Address"
                }
            ),

            "department": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Department"
                }
            ),

            "subject1": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100
                }
            ),

            "subject2": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100
                }
            ),

            "subject3": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100
                }
            ),

            "subject4": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100
                }
            ),

            "subject5": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100
                }
            ),
        }

    def clean_student_id(self):

        student_id = self.cleaned_data["student_id"]

        if not validate_student_id(student_id):
            raise forms.ValidationError(
                "Student ID must be like ST101 or ST2024."
            )

        return student_id

    def clean_email(self):

        email = self.cleaned_data["email"]

        if not validate_email(email):
            raise forms.ValidationError(
                "Enter a valid email address."
            )

        return email

    def clean(self):

        cleaned_data = super().clean()

        try:

            marks = [

                cleaned_data.get("subject1", 0),

                cleaned_data.get("subject2", 0),

                cleaned_data.get("subject3", 0),

                cleaned_data.get("subject4", 0),

                cleaned_data.get("subject5", 0),

            ]

            validate_marks(*marks)

        except InvalidMarksException as e:

            raise forms.ValidationError(str(e))

        return cleaned_data


class CSVUploadForm(forms.Form):

    csv_file = forms.FileField(
        label="Select CSV File",
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "accept": ".csv"
            }
        )
    )

    def clean_csv_file(self):

        file = self.cleaned_data["csv_file"]

        if not file.name.endswith(".csv"):
            raise forms.ValidationError(
                "Only CSV files are allowed."
            )

        return file