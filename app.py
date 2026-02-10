from flask import Flask, render_template, request, redirect
import csv
import statistics

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_entry():
    day = request.form["day"]
    sleep = request.form["sleep"]
    study = request.form["study"]
    screen = request.form["screen"]

    with open("data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([day, sleep, study, screen])

    return redirect("/")

@app.route("/analysis")
def analysis():
    sleep_list = []
    study_list = []
    screen_list = []

    with open("data.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            sleep_list.append(float(row["sleep_hours"]))
            study_list.append(float(row["study_hours"]))
            screen_list.append(float(row["screen_time"]))

    if len(sleep_list) == 0:
        return "No data available yet. Add entries first!"

    avg_sleep = statistics.mean(sleep_list)
    avg_study = statistics.mean(study_list)
    avg_screen = statistics.mean(screen_list)

    return render_template(
        "analysis.html",
        avg_sleep=avg_sleep,
        avg_study=avg_study,
        avg_screen=avg_screen
    )

if __name__ == "__main__":
    app.run(debug=True)
