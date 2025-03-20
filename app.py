from flask import Flask, request, render_template
import json
import os
import uuid
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

FILENAME = "tasks.json"
PRIORITY_MAP = {"High": 3, "Medium": 2, "Low": 1}

# Ensure months are sorted correctly
MONTHS_ORDER = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
}

def load_tasks():
    """Loads tasks from JSON file and ensures all tasks have an ID."""
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            tasks = json.load(file)

        # Assign an ID to any old tasks that don't have one
        for task in tasks:
            if "id" not in task:
                task["id"] = str(uuid.uuid4())

        save_tasks(tasks)  # Save any updated tasks
        return tasks
    return []

def save_tasks(tasks):
    """Saves the current task list to a JSON file."""
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=4)

@app.route("/")
def home():
    """Serves the HTML page."""
    return render_template("index.html")

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    """Handles fetching and adding tasks."""
    if request.method == "GET":
        return get_tasks()

    elif request.method == "POST":
        data = request.json
        if not all(k in data for k in ("description", "due_date", "priority")):
            return json.dumps({"error": "Missing fields"}), 400, {"Content-Type": "application/json"}

        try:
            datetime.strptime(data["due_date"], "%Y-%m-%d")  # Validate date format
        except ValueError:
            return json.dumps({"error": "Invalid date format. Use YYYY-MM-DD."}), 400, {"Content-Type": "application/json"}

        tasks = load_tasks()
        task_id = str(uuid.uuid4())  # Generate unique ID
        new_task = {
            "id": task_id,
            "description": data["description"],
            "due_date": data["due_date"],
            "priority": data["priority"]
        }
        tasks.append(new_task)
        save_tasks(tasks)
        return json.dumps({"message": "Task added successfully", "id": task_id}), 201, {"Content-Type": "application/json"}

@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Returns tasks grouped by month, sorted by date then priority."""
    tasks = load_tasks()

    grouped_tasks = defaultdict(list)
    for task in tasks:
        try:
            task_date = datetime.strptime(task["due_date"], "%Y-%m-%d")
        except ValueError:
            continue  # Skip invalid dates
        month_year = task_date.strftime("%B %Y")
        grouped_tasks[month_year].append(task)

    # Sort tasks within each month (by date first, then priority)
    for month_year in grouped_tasks:
        grouped_tasks[month_year] = sorted(
            grouped_tasks[month_year],
            key=lambda x: (x["due_date"], -PRIORITY_MAP[x["priority"]])
        )

    # Ensure months are sorted numerically
    def month_year_key(month_year):
        month, year = month_year.split(" ")
        return (int(year), MONTHS_ORDER.get(month, 0))  # Sort by year first, then by month order

    sorted_grouped_tasks = dict(sorted(
        grouped_tasks.items(),
        key=lambda x: month_year_key(x[0])
    ))

    return json.dumps(sorted_grouped_tasks), 200, {"Content-Type": "application/json"}

@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Deletes a task using its unique ID."""
    tasks = load_tasks()
    updated_tasks = [task for task in tasks if task["id"] != task_id]

    if len(updated_tasks) == len(tasks):  # Task not found
        return json.dumps({"error": "Task not found"}), 400, {"Content-Type": "application/json"}

    save_tasks(updated_tasks)
    return json.dumps({"message": "Task deleted successfully"}), 200, {"Content-Type": "application/json"}

if __name__ == "__main__":
    app.run(debug=True)
