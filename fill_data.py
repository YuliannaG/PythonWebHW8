from datetime import datetime
import faker
from random import randint, choice
import sqlite3

NUMBER_GROUPS = 3
NUMBER_STUDENTS = 30
NUMBER_TEACHERS = 3
NUMBER_GRADES = 5
NUMBER_SUBJECTS = 5


def generate_fake_data(number_students, number_teachers, number_subjects, number_grades, number_groups) -> tuple():
    my_students = []
    my_teachers = []
    my_subjects = ['math', 'english', 'science', 'arts', 'gym']
    my_groups = []
    my_grades = []
    fake_data = faker.Faker()
    for _ in range(number_students):
        my_students.append(fake_data.name())
    for _ in range(number_teachers):
        my_teachers.append(fake_data.name())
    for i in range(number_groups+1):
        if i > 0: my_groups.append(i)
    for i in range(number_grades+1):
        if i > 0: my_grades.append(i)
    return my_subjects, my_teachers, my_students, my_grades, my_groups


def prepare_data(my_subjects, my_teachers, my_students, my_grades, my_groups) -> tuple():
    for_grades = []
    for gr in my_grades:
        for_grades.append((gr,))

    for_groups = []
    for gr in my_groups:
        for_groups.append((gr,))

    for_subjects = []
    for subject in my_subjects:
        for_subjects.append((subject, randint(1, NUMBER_TEACHERS)))

    for_students = []
    for st in my_students:
        for_students.append((st, randint(1, NUMBER_GROUPS)))

    for_teachers = []
    for te in my_teachers:
        for_teachers.append((te, ))

    for_records = []
    for st in range(1, NUMBER_STUDENTS + 1):
        for _ in range(0, 21):
            record_date = datetime(2022, 5, randint(10, 28)).date()
            for_records.append((record_date, st, randint(1, NUMBER_GRADES), randint(1, NUMBER_SUBJECTS)))

    return for_subjects, for_teachers, for_students, for_grades, for_groups, for_records


def insert_data_to_db(for_subjects, for_teachers, for_students, for_grades, for_groups, for_records) -> None:
    with sqlite3.connect('university.db') as con:
        cur = con.cursor()

        sql_to_groups = """INSERT INTO groups(name)
                                          VALUES (?)"""
        cur.executemany(sql_to_groups, for_groups)

        sql_to_grades = """INSERT INTO grades(name)
                                          VALUES (?)"""
        cur.executemany(sql_to_grades, for_grades)

        sql_to_teachers = """INSERT INTO teachers(name)
                                                 VALUES (?)"""
        cur.executemany(sql_to_teachers, for_teachers)

        sql_to_subjects = """INSERT INTO subjects(name, teacher_id)
                                  VALUES (?, ?)"""
        cur.executemany(sql_to_subjects, for_subjects)

        sql_to_students = """INSERT INTO students(name, group_id)
                                  VALUES (?, ?)"""
        cur.executemany(sql_to_students, for_students)

        sql_to_records = """INSERT INTO records(record_date, student_id, grade_id, subject_id)
                                 VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_records, for_records)

        con.commit()


if __name__ == "__main__":
    my_subjects, my_teachers, my_students, my_grades, my_groups = generate_fake_data(NUMBER_STUDENTS, NUMBER_TEACHERS, NUMBER_SUBJECTS, NUMBER_GRADES, NUMBER_GROUPS)
    my_subjects, my_teachers, my_students, my_grades, my_groups, my_records = prepare_data(my_subjects, my_teachers, my_students, my_grades, my_groups)
    insert_data_to_db(my_subjects, my_teachers, my_students, my_grades, my_groups, my_records)