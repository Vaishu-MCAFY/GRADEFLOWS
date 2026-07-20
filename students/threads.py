import threading
import csv
import os
from datetime import datetime

from .models import Report


class ReportGeneratorThread(threading.Thread):
    """
    Thread class for generating a report for a single student.
    """

    def __init__(self, student, output_folder="media/reports"):
        super().__init__()
        self.student = student
        self.output_folder = output_folder

    def run(self):
        """
        Generate a CSV report for one student.
        """

        # Create Report object
        report = Report(self.student)

        # Get report data
        data = report.generate()

        # Create output folder if it doesn't exist
        os.makedirs(self.output_folder, exist_ok=True)

        # File name
        filename = os.path.join(
            self.output_folder,
            f"{self.student.student_id}_report.csv"
        )

        # Write report
        with open(filename, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow(["Field", "Value"])

            for key, value in data.items():
                writer.writerow([key, value])

        print(f"Report generated: {filename}")

def generate_bulk_reports(student_list):
    """
    Generate reports concurrently using threading.
    """

    threads = []

    # Create threads
    for student in student_list:

        thread = ReportGeneratorThread(student)

        threads.append(thread)

        thread.start()

    # Wait until all threads complete
    for thread in threads:
        thread.join()

    print("\nAll reports generated successfully.")

    return True

def generate_dashboard_report(statistics,
                              filename="media/dashboard_summary.csv"):
    """
    Generate dashboard statistics report.
    """

    os.makedirs("media", exist_ok=True)

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(["GradeFlow Dashboard Summary"])
        writer.writerow(["Generated On", datetime.now()])

        writer.writerow([])

        for key, value in statistics.items():

            if isinstance(value, dict):

                writer.writerow([key])

                for k, v in value.items():
                    writer.writerow([k, v])

            else:
                writer.writerow([key, value])

    print(f"Dashboard report saved to {filename}")

    return filename