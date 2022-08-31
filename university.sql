CREATE TABLE grades (
    id INTEGER PRIMARY KEY,
    name INT
);

CREATE TABLE groups (
    id INTEGER PRIMARY KEY,
    name INT
);

CREATE TABLE teachers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30)
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30),
    group_id INT,
    FOREIGN KEY (group_id) REFERENCES groups (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

CREATE TABLE subjects (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30),
    teacher_id INT,
    FOREIGN KEY (teacher_id) REFERENCES teachers (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

CREATE TABLE records (
    id INTEGER PRIMARY KEY,
    record_date DATE,
    student_id INT,
    grade_id INT,
    subject_id INT,
    FOREIGN KEY (student_id) REFERENCES students (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (grade_id) REFERENCES grades (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);
