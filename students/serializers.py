from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student Model
    """

    total_marks = serializers.SerializerMethodField()
    average_marks = serializers.SerializerMethodField()
    highest_mark = serializers.SerializerMethodField()
    lowest_mark = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()
    at_risk = serializers.SerializerMethodField()

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

            "total_marks",
            "average_marks",
            "highest_mark",
            "lowest_mark",
            "grade",
            "result",
            "at_risk",
        ]

    def get_total_marks(self, obj):
        return obj.total_marks()

    def get_average_marks(self, obj):
        return obj.average_marks()

    def get_highest_mark(self, obj):
        return obj.highest_mark()

    def get_lowest_mark(self, obj):
        return obj.lowest_mark()

    def get_grade(self, obj):
        return obj.grade()

    def get_result(self, obj):
        return obj.result()

    def get_at_risk(self, obj):
        return obj.is_at_risk()