from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)

db = client[settings.MONGO_DB_NAME]

students_collection = db["students"]
def add_student(student_data):
    """
    Insert a new student document into MongoDB.
    """
    return students_collection.insert_one(student_data)
def get_all_students():
    """
    Return all students.
    """
    return list(
        students_collection.find(
            {},
            {"_id": 0}  # Hide MongoDB ObjectId
        )
    )
def get_student(student_id):
    """
    Find a student using student_id.
    """
    return students_collection.find_one(
        {"student_id": student_id},
        {"_id": 0}
    )
def update_student(student_id, updated_data):
    """
    Update student details.
    """
    return students_collection.update_one(
        {"student_id": student_id},
        {"$set": updated_data}
    )

def delete_student(student_id):
    """
    Delete a student.
    """
    return students_collection.delete_one(
        {"student_id": student_id}
    )

def search_students(keyword):
    """
    Search by name or department.
    """
    return list(
        students_collection.find(
            {
                "$or": [
                    {"name": {"$regex": keyword, "$options": "i"}},
                    {"department": {"$regex": keyword, "$options": "i"}}
                ]
            },
            {"_id": 0}
        )
    )

def class_average():
    """
    Calculate average marks using MongoDB aggregation.
    """

    pipeline = [
        {
            "$project": {
                "average": {
                    "$avg": [
                        "$subject1",
                        "$subject2",
                        "$subject3",
                        "$subject4",
                        "$subject5"
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "class_average": {
                    "$avg": "$average"
                }
            }
        }
    ]

    result = list(students_collection.aggregate(pipeline))

    if result:
        return round(result[0]["class_average"], 2)

    return 0

def dashboard_statistics():

    students = get_all_students()

    total_students = len(students)

    if total_students == 0:
        return {
            "total_students": 0,
            "average_marks": 0,
            "topper": None,
            "failed_students": 0,
            "pass_percentage": 0,
        }

    topper = max(
        students,
        key=lambda s: (
            s["subject1"] +
            s["subject2"] +
            s["subject3"] +
            s["subject4"] +
            s["subject5"]
        )
    )

    failed = 0

    for s in students:

        marks = [
            s["subject1"],
            s["subject2"],
            s["subject3"],
            s["subject4"],
            s["subject5"],
        ]

        if min(marks) < 40:
            failed += 1

    pass_percentage = round(
        ((total_students - failed) / total_students) * 100,
        2
    )

    return {
        "total_students": total_students,
        "average_marks": class_average(),
        "topper": topper,
        "failed_students": failed,
        "pass_percentage": pass_percentage,
    }