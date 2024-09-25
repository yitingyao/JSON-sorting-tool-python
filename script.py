import json
import os

NUM_STUDENTS = 1000
SUBJECTS = ["math", "science", "history", "english", "geography"]  

def load_report_card(directory, student_number):
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, f"{student_number}.json")
    path = os.path.join(base_path, file_path)

    try:
        with open(path, "r") as file:
            report_card = json.load(file)
    except FileNotFoundError:
        return {}

    return report_card


def load_report_cards(directory, num_students):
    report_cards = []

    for student_number in range(num_students):
        report_card = load_report_card(directory, student_number)
        if report_card:  # Ensure only valid report cards are appended
            report_cards.append(report_card)

    return report_cards


def add_student_averages(report_cards, subjects):
    for report_card in report_cards:
        sum_of_marks = 0

        for key, value in report_card.items():
            if key.lower() not in subjects:  # Case-insensitive check for subjects
                continue

            sum_of_marks += value

        average = sum_of_marks / len(subjects)
        # Add a new key to the report card with the average
        report_card["average"] = average


def get_average_student_grade(report_cards):
    sum_of_averages = 0

    for report_card in report_cards:
        sum_of_averages += report_card["average"]

    return sum_of_averages / len(report_cards)


def get_subject_averages(report_cards, subjects):
    subject_averages = {subject: 0 for subject in subjects}

    for report_card in report_cards:
        for subject in subjects:
            mark = report_card.get(subject.capitalize(), report_card.get(subject))  
            subject_averages[subject] += mark

    for subject in subjects:
        subject_averages[subject] /= len(report_cards)

    return subject_averages


def get_grade_level_averages(report_cards):
    grade_level_averages = {grade: [] for grade in range(1, 9)}

    for report_card in report_cards:
        grade = report_card["grade"]
        average = report_card["average"]

        grade_level_averages[grade].append(average)

    for grade in grade_level_averages:
        grade_level_averages[grade] = sum(grade_level_averages[grade]) / len(
            grade_level_averages[grade]
        )

    return grade_level_averages


def get_best_students_per_subject(report_cards, subjects):
    best_students = {subject: {"id": None, "mark": -1} for subject in subjects}

    for report_card in report_cards:
        for subject in subjects:
            mark = report_card.get(subject.capitalize(), report_card.get(subject))  
            if mark > best_students[subject]["mark"]:
                best_students[subject] = {"id": report_card["id"], "mark": mark}

    return best_students


# Main execution
report_cards = load_report_cards("JSON-files", NUM_STUDENTS)
add_student_averages(report_cards, SUBJECTS)

average_student_grade = round(get_average_student_grade(report_cards), 2)

subject_averages = get_subject_averages(report_cards, SUBJECTS)
sorted_subject_averages = sorted(subject_averages.items(), key=lambda x: x[1])
hardest_subject = sorted_subject_averages[0][0].capitalize()  # Capitalize for output
easiest_subject = sorted_subject_averages[-1][0].capitalize()  
grade_level_averages = get_grade_level_averages(report_cards)
sorted_grade_level_averages = sorted(
    grade_level_averages.items(), key=lambda x: x[1])
best_grade_level = sorted_grade_level_averages[-1][0]
worst_grade_level = sorted_grade_level_averages[0][0]

students_sorted_by_grade = sorted(report_cards, key=lambda x: x["average"])
best_student = students_sorted_by_grade[-1]["id"]
worst_student = students_sorted_by_grade[0]["id"]

# Get best students per subject
best_students_per_subject = get_best_students_per_subject(report_cards, SUBJECTS)

# Store results in an array (list)
results = [
    f"Average Student Grade: {average_student_grade}",
    f"Hardest Subject: {hardest_subject}",  
    f"Easiest Subject: {easiest_subject}",  
    f"Best Performing Grade: {best_grade_level}",
    f"Worst Performing Grade: {worst_grade_level}",
    f"Best Student ID: {best_student}",
    f"Worst Student ID: {worst_student}",
]

# Add best students per subject to the results
results.append("\nBest Students Per Subject:")
for subject, student_info in best_students_per_subject.items():
    results.append(f"{subject.capitalize()}: Student {student_info['id']} (Mark: {student_info['mark']})")  # Capitalize for output

# Print results to console
for line in results:
    print(line)

# Save results to a file
with open("results.txt", "w") as file:
    for line in results:
        file.write(line + "\n")
