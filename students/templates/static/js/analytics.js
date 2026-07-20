document.addEventListener("DOMContentLoaded", function () {

    const totalStudents = Number(document.getElementById("totalStudents").value);
    const passedStudents = Number(document.getElementById("passedStudents").value);
    const failedStudents = Number(document.getElementById("failedStudents").value);
    const riskStudents = Number(document.getElementById("riskStudents").value);

    // Pie Chart

    const pieCtx = document.getElementById("pieChart");

    new Chart(pieCtx, {

        type: "pie",

        data: {

            labels: ["Passed", "Failed"],

            datasets: [{

                data: [passedStudents, failedStudents],

                backgroundColor: [

                    "#198754",
                    "#dc3545"

                ]

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

    // Bar Chart

    const barCtx = document.getElementById("barChart");

    new Chart(barCtx, {

        type: "bar",

        data: {

            labels: [

                "Students",
                "Passed",
                "Failed",
                "At Risk"

            ],

            datasets: [{

                label: "Student Statistics",

                data: [

                    totalStudents,
                    passedStudents,
                    failedStudents,
                    riskStudents

                ],

                backgroundColor: [

                    "#0d6efd",
                    "#198754",
                    "#dc3545",
                    "#ffc107"

                ],

                borderWidth: 1

            }]

        },

        options: {

            responsive: true,

            scales: {

                y: {

                    beginAtZero: true

                }

            }

        }

    });

});