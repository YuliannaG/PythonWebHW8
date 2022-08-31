import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect('university.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql1 = """
SELECT s.name,ROUND(AVG(r.grade_id), 2) 
FROM records as r
LEFT JOIN grades as g ON r.grade_id = g.id
LEFT JOIN students as s ON r.student_id = s.id
GROUP BY s.name
ORDER BY ROUND(AVG(r.grade_id), 2) DESC
LIMIT 5;
"""

sql2 = """
SELECT * FROM(    
    SELECT sb.name as subject, s.name as student_name, ROUND(AVG(r.grade_id), 2) as average_grade, row_number() over (partition by subject_id order by ROUND(AVG(r.grade_id), 2) desc) as student_rank
    FROM records as r
        LEFT JOIN grades as g ON r.grade_id = g.id
        LEFT JOIN students as s ON r.student_id = s.id
        LEFT JOIN subjects as sb ON r.subject_id = sb.id
    GROUP BY sb.name, s.name) 
where student_rank <= 1;
"""

sql3 = """
SELECT s.group_id, sb.name as subject, ROUND(AVG(r.grade_id), 2) as average_grade
FROM records as r
    LEFT JOIN grades as g ON r.grade_id = g.id
    LEFT JOIN (students LEFT JOIN groups as gr ON students.group_id = gr.id) as s ON r.student_id = s.id
    LEFT JOIN subjects as sb ON r.subject_id = sb.id
GROUP BY s.group_id, sb.name;
"""

sql4 = """
SELECT ROUND(AVG(r.grade_id), 2) as average_grade
FROM records as r
    LEFT JOIN grades as g ON r.grade_id = g.id;
"""

sql5 = """
SELECT t.name,s.name 
FROM subjects as s
LEFT JOIN teachers as t ON s.teacher_id = t.id
ORDER BY t.name;
"""

sql6 = """
SELECT g.name, s.name 
FROM students as s
LEFT JOIN groups as g ON s.group_id = g.id
ORDER BY g.name;
"""

sql7 = """
SELECT gr.name as student_group, s.name as student, sb.name as subject, g.name as grade
FROM records as r
    LEFT JOIN grades as g ON r.grade_id = g.id
    LEFT JOIN (students LEFT JOIN groups as gr ON students.group_id = gr.id) as s ON r.student_id = s.id
    LEFT JOIN subjects as sb ON r.subject_id = sb.id
WHERE sb.name = 'math'
ORDER BY gr.name, s.name;
"""

sql8 = """
SELECT groups.name as student_group, s.name as student, sb.name as subject, g.name as grade, r.record_date
FROM records as r
    LEFT JOIN grades as g ON r.grade_id = g.id
    LEFT JOIN (students LEFT JOIN groups ON students.group_id = groups.id) as s ON r.student_id = s.id
    LEFT JOIN subjects as sb ON r.subject_id = sb.id
    INNER JOIN (
        SELECT students.group_id as group_id, r.subject_id as subject_id, MAX(r.record_date) as MaxDate
        FROM records as r
        LEFT JOIN students ON r.student_id = students.id 
        WHERE r.subject_id = 1
   			AND students.group_id = 1
   		GROUP BY students.group_id
        ) as rd ON r.record_date = rd.MaxDate AND s.group_id = rd.group_id AND r.subject_id = rd.subject_id;
"""

sql9 = """
SELECT DISTINCT s.name as student, sb.name as subject
FROM records as r
    LEFT JOIN students as s ON r.student_id = s.id
    LEFT JOIN subjects as sb ON r.subject_id = sb.id
WHERE s.name = 'Luis Rollins';
"""

sql10 = """
SELECT DISTINCT s.name as student, sb.name as subject, teachers.name as teacher
FROM records as r
    LEFT JOIN students as s ON r.student_id = s.id
    LEFT JOIN (subjects LEFT JOIN teachers ON subjects.teacher_id = teachers.id) as sb ON r.subject_id = sb.id
WHERE s.name = 'Luis Rollins'
    AND teachers.name = 'Brett Webb';
"""

sql11 = """
SELECT DISTINCT s.name as student, teachers.name as teacher, ROUND(AVG(r.grade_id), 2) as average_grade
FROM records as r
    LEFT JOIN students as s ON r.student_id = s.id
    LEFT JOIN (subjects LEFT JOIN teachers ON subjects.teacher_id = teachers.id) as sb ON r.subject_id = sb.id
WHERE s.name = 'Luis Rollins'
    AND teachers.name = 'Brett Webb'
"""

sql12 = """
SELECT DISTINCT teachers.name as teacher, ROUND(AVG(r.grade_id), 2) as average_grade
FROM records as r
    LEFT JOIN (subjects LEFT JOIN teachers ON subjects.teacher_id = teachers.id) as sb ON r.subject_id = sb.id
WHERE teachers.name = 'Brett Webb'
"""

tasks = {1: '5 студентов с наибольшим средним баллом по всем предметам',
         2: '1 студент с наивысшим средним баллом по одному предмету',
         3: 'средний балл в группе по одному предмету',
         4: 'Средний балл в потоке',
         5: 'Какие курсы читает преподаватель',
         6: 'Список студентов в группе',
         7: 'Оценки студентов в группе по предмету',
         8: 'Оценки студентов в конкретной группе по конкретному предмету на последнем занятии',
         9: 'Список курсов, которые посещает конкретный студент',
         10: 'Список курсов, которые конкретному студенту читает конкретный преподаватель',
         11: 'Средний балл, который конкретный преподаватель ставит конкретному студенту',
         12: 'Средний балл, который ставит конкретный преподаватель'}

if __name__ == "__main__":
    for n in range(1, 13):
        print(f'{n}. {tasks[n]}')
        print(eval(f'execute_query(sql{n})'))

