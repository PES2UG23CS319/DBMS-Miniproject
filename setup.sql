CREATE DATABASE IF NOT EXISTS PeerTutoring;
USE PeerTutoring;

-- DROP DATABASE PeerTutoring;
-- TABLE DEFINITIONS

CREATE TABLE Student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    ph_no VARCHAR(15) UNIQUE,
    role ENUM('mentor', 'mentee') NOT NULL,
    dept VARCHAR(50),
    year INT CHECK (year BETWEEN 1 AND 4)
);

CREATE TABLE Subject (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE Team (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) UNIQUE NOT NULL,
    mentor_id INT,
    creation_date DATE,
    FOREIGN KEY (mentor_id) REFERENCES Student(student_id) 
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Junction Table: connects teams ↔ students
CREATE TABLE TeamMember (
    team_id INT,
    student_id INT,
    role ENUM('mentor','mentee') NOT NULL,
    PRIMARY KEY (team_id, student_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (student_id) REFERENCES Student(student_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Junction Table: connects students ↔ subjects
CREATE TABLE StudentSubject (
    student_id INT,
    subject_id INT,
    PRIMARY KEY (student_id, subject_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES Subject(subject_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE MentorshipSession (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT,
    date_time DATETIME,
    duration INT,
    status ENUM('scheduled','completed','cancelled') DEFAULT 'scheduled',
    FOREIGN KEY (subject_id) REFERENCES Subject(subject_id) 
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Junction Table: connects sessions ↔ students
CREATE TABLE SessionParticipant (
    session_id INT,
    student_id INT,
    role ENUM('mentor','mentee') NOT NULL,
    PRIMARY KEY (session_id, student_id),
    FOREIGN KEY (session_id) REFERENCES MentorshipSession(session_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (student_id) REFERENCES Student(student_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    anonymous BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (session_id) REFERENCES MentorshipSession(session_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- INSERTING DATA

-- Students
-- Students
-- STUDENTS
INSERT INTO Student (name, email, ph_no, role, dept, year) VALUES
('Maitreyi Vijay', 'maitreyi@univ.edu', '9876543210', 'mentor', 'CSE', 4),       
('Mahith Das', 'mahithk@univ.edu', '9876501234', 'mentee', 'CSE', 2),            
('Aditya Kumar', 'adityak@univ.edu', '9876505678', 'mentee', 'CSE', 1),         
('Divya Singh', 'divyasingh@univ.edu', '8976512345', 'mentor', 'ECE', 4),            
('Esha Patel', 'eshapatel@univ.edu', '7762523456', 'mentee', 'ECE', 2),               
('Ravi Sharma', 'ravisharma@univ.edu', '9123456789', 'mentor', 'Physics', 4),          
('Neha Reddy', 'nehareddy@univ.edu', '9234567890', 'mentor', 'Chemistry', 4),         
('Arjun Mehta', 'arjunmehta@univ.edu', '9345678901', 'mentor', 'Mathematics', 4),     
('Kavya Iyer', 'kavyaiyer@univ.edu', '9456789012', 'mentee', 'Mathematics', 1),      
('Suresh Rao', 'sureshr@univ.edu', '9567890123', 'mentee', 'Physics', 2),     
('Pooja Sharma', 'pooja@univ.edu', '9678901234', 'mentee', 'CSE', 3),
('Rahul Verma', 'rahulv@univ.edu', '9789012345', 'mentee', 'ECE', 1),
('Ananya Gupta', 'ananyag@univ.edu', '9890123456', 'mentee', 'Physics', 1),
('Karan Singh', 'karans@univ.edu', '9901234567', 'mentee', 'Chemistry', 3),
('Simran Kaur', 'simrank@univ.edu', '9912345678', 'mentee', 'Mathematics', 2);

-- SUBJECTS
INSERT INTO Subject (subject_name, description) VALUES
('Data Structures', 'Study of linear and non-linear data structures'),           
('Databases', 'Relational databases, SQL queries, normalization'),              
('Computer Networks', 'Networking protocols and communication'),                 
('Digital Electronics', 'Logic gates, sequential circuits, combinational circuits'),
('Microprocessors', 'Architecture and programming of microprocessors'),          
('Engineering Physics', 'Mechanics, waves, optics, and modern physics'),        
('Engineering Chemistry', 'Chemical bonding, electrochemistry, polymers, nanomaterials'), 
('Engineering Mathematics', 'Calculus, linear algebra, differential equations'); 

-- TEAMS


-- TEAMS
INSERT INTO Team (team_name, mentor_id, creation_date) VALUES
('CSE Mentors', 1, '2025-09-01'),
('ECE Mentors', 4, '2025-09-02'),
('Physics Mentors', 6, '2025-09-03'),
('Chemistry Mentors', 7, '2025-09-04'),
('Math Mentors', 8, '2025-09-05'),
('CSE Advanced Mentors', 1, '2025-09-06'),
('ECE Beginners', 4, '2025-09-07');



-- TEAM MEMBERS
INSERT INTO TeamMember (team_id, student_id, role) VALUES
-- CSE
(1, 1, 'mentor'),
(1, 2, 'mentee'),
(1, 3, 'mentee'),

-- ECE
(2, 4, 'mentor'),
(2, 5, 'mentee'),

-- Physics
(3, 6, 'mentor'),
(3, 10, 'mentee'),

-- Chemistry
(4, 7, 'mentor'),
(4, 5, 'mentee'),

-- Math
(5, 8, 'mentor'),
(5, 9, 'mentee'),
(5, 2, 'mentee'),

-- CSE Advanced
(6, 1, 'mentor'),
(6, 11, 'mentee'),

-- ECE Beginners
(7, 4, 'mentor'),
(7, 12, 'mentee');



-- STUDENT SUBJECTS
INSERT INTO StudentSubject (student_id, subject_id) VALUES
(1, 1),  -- Maitreyi teaches Data Structures
(2, 1),  -- Mahith learning DS
(3, 2),  -- Aditya learning Databases
(4, 4),  -- Divya teaches Digital Electronics
(5, 5),  -- Esha learning Microprocessors
(6, 6),  -- Ravi teaches Physics
(7, 7),  -- Neha teaches Chemistry
(8, 8),  -- Arjun teaches Math
(9, 8),  -- Kavya learning Math
(10, 6), -- Suresh learning Physics
(11, 1), -- Pooja learning Data Structures
(12, 4), -- Rahul learning Digital Electronics
(13, 6), -- Ananya learning Physics
(14, 7), -- Karan learning Chemistry
(15, 8); -- Simran learning Mathematics

 


-- MENTORSHIP SESSIONS
INSERT INTO MentorshipSession (subject_id, date_time, duration, status) VALUES
(1, '2025-09-10 10:00:00', 60, 'scheduled'),   -- DS session
(2, '2025-09-11 11:00:00', 45, 'completed'),   -- DB session
(4, '2025-09-12 14:00:00', 50, 'scheduled'),   -- Digital Electronics
(6, '2025-09-13 09:00:00', 40, 'completed'),   -- Physics
(7, '2025-09-14 16:00:00', 55, 'scheduled'),   -- Chemistry
(8, '2025-09-15 17:00:00', 60, 'completed'),  -- Math
(1, '2025-09-10 10:00:00', 60, 'scheduled'),
(2, '2025-09-11 11:00:00', 45, 'completed'),
(4, '2025-09-12 14:00:00', 50, 'scheduled'),
(6, '2025-09-13 09:00:00', 40, 'completed'),
(7, '2025-09-14 16:00:00', 55, 'scheduled'),
(8, '2025-09-15 17:00:00', 60, 'completed'),
(1, DATE_ADD(NOW(), INTERVAL 1 DAY), 60, 'scheduled'),
(4, DATE_ADD(NOW(), INTERVAL 2 DAY), 45, 'scheduled'),
(6, DATE_ADD(NOW(), INTERVAL 3 DAY), 50, 'scheduled'),
(7, DATE_ADD(NOW(), INTERVAL 4 DAY), 55, 'scheduled'),
(8, DATE_ADD(NOW(), INTERVAL 5 DAY), 60, 'scheduled');



-- SESSION PARTICIPANTS
INSERT INTO SessionParticipant (session_id, student_id, role) VALUES
-- Session 1: CSE DS
(1, 1, 'mentor'),
(1, 2, 'mentee'),

-- Session 2: Databases
(2, 1, 'mentor'),
(2, 3, 'mentee'),

-- Session 3: Digital Electronics
(3, 4, 'mentor'),
(3, 5, 'mentee'),

-- Session 4: Physics
(4, 6, 'mentor'),
(4, 10, 'mentee'),

-- Session 5: Chemistry
(5, 7, 'mentor'),
(5, 5, 'mentee'),

-- Session 6: Mathematics
(6, 8, 'mentor'),
(6, 9, 'mentee'),
(6, 2, 'mentee'),

-- Session 7: CSE Advanced
(7, 1, 'mentor'),
(7, 11, 'mentee'),

-- Session 8: ECE Beginners
(8, 4, 'mentor'),
(8, 12, 'mentee'),

-- Session 9: Physics Extended
(9, 6, 'mentor'),
(9, 13, 'mentee'),

-- Session 10: Chemistry Advanced
(10, 7, 'mentor'),
(10, 14, 'mentee'),

-- Session 11: Math Advanced
(11, 8, 'mentor'),
(11, 15, 'mentee');


-- FEEDBACK
INSERT INTO Feedback (session_id, rating, comment, anonymous) VALUES
(1, 5, 'Great explanation of linked lists!', FALSE),
(2, 4, 'Good session but needed more examples.', TRUE),
(3, 5, 'Really clear teaching style.', FALSE),
(4, 4, 'Helped me understand mechanics better.', FALSE),
(5, 3, 'Some parts were confusing.', TRUE),
(6, 5, 'Excellent Math mentor!', FALSE),
(1, 5, 'Great explanation of linked lists!', FALSE),
(2, 4, 'Good session but needed more examples.', TRUE),
(3, 5, 'Really clear teaching style.', FALSE),
(4, 4, 'Helped me understand mechanics better.', FALSE),
(5, 3, 'Some parts were confusing.', TRUE),
(6, 5, 'Excellent Math mentor!', FALSE),
(7, 5, 'DS session was very helpful!', FALSE),
(8, 4, 'Clear explanation of circuits.', TRUE),
(9, 5, 'Physics mentor is excellent!', FALSE),
(10, 4, 'Chemistry session clarified doubts.', TRUE),
(11, 5, 'Math mentor is great!', FALSE);

-- SHOW DATA

SHOW TABLES;
SELECT * FROM Student;

SELECT * FROM Subject;

SELECT * FROM Team;

SELECT * FROM TeamMember;

SELECT * FROM StudentSubject;

SELECT * FROM MentorshipSession;

SELECT * FROM SessionParticipant;

SELECT * FROM Feedback;


-- 1. Trigger
DELIMITER //

CREATE TRIGGER update_session_status
BEFORE UPDATE ON MentorshipSession
FOR EACH ROW
BEGIN
    IF NEW.status = 'scheduled' AND NEW.date_time < NOW() THEN
        SET NEW.status = 'completed';
    END IF;
END;
//

DELIMITER ;

-- Insert a session in the past
INSERT INTO MentorshipSession(subject_id, date_time, duration, status)
VALUES (1, '2025-01-01 10:00:00', 60, 'scheduled');

-- Update to trigger the BEFORE UPDATE
UPDATE MentorshipSession
SET duration = 90
WHERE session_id = LAST_INSERT_ID();

-- Check result
SELECT * FROM MentorshipSession
WHERE session_id = LAST_INSERT_ID();



-- 2. 
DELIMITER //

CREATE PROCEDURE AddMentorshipSession(
    IN p_subject_id INT,
    IN p_date_time DATETIME,
    IN p_duration INT,
    IN p_mentor_id INT,
    IN p_mentee_ids TEXT    -- comma-separated mentee IDs
)
BEGIN
    DECLARE last_session_id INT;
    DECLARE mentee_id INT;
    DECLARE i INT DEFAULT 1;
    DECLARE mentee_count INT;

    -- 1. Insert session
    INSERT INTO MentorshipSession(subject_id, date_time, duration)
    VALUES (p_subject_id, p_date_time, p_duration);

    SET last_session_id = LAST_INSERT_ID();

    -- 2. Add mentor
    INSERT INTO SessionParticipant(session_id, student_id, role)
    VALUES (last_session_id, p_mentor_id, 'mentor');

    -- 3. Add mentees
    SET mentee_count = (LENGTH(p_mentee_ids) - LENGTH(REPLACE(p_mentee_ids, ',', ''))) + 1;

    WHILE i <= mentee_count DO
        SET mentee_id = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_mentee_ids, ',', i), ',', -1) AS UNSIGNED);
        INSERT INTO SessionParticipant(session_id, student_id, role)
        VALUES (last_session_id, mentee_id, 'mentee');
        SET i = i + 1;
    END WHILE;
END;
//

DELIMITER ;

USE PeerTutoring;

-- Call the procedure to add a new session
CALL AddMentorshipSession(
    2,                      -- Subject ID (Databases)
    '2025-10-30 14:00:00',  -- Date/Time
    45,                     -- Duration
    1,                      -- Mentor ID (Maitreyi Vijay)
    '2,3'                   -- Mentee IDs (Mahith Das, Aditya Kumar)
);

-- Verify the session was created
SELECT * FROM MentorshipSession
ORDER BY session_id DESC
LIMIT 1;

-- Verify participants were added
SELECT * FROM SessionParticipant
WHERE session_id = (SELECT MAX(session_id) FROM MentorshipSession);


-- 3. Function

DELIMITER //

CREATE FUNCTION MentorSessionCount(p_mentor_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total_sessions INT;

    SELECT COUNT(*) INTO total_sessions
    FROM SessionParticipant sp
    JOIN MentorshipSession ms ON sp.session_id = ms.session_id
    WHERE sp.student_id = p_mentor_id
      AND sp.role = 'mentor'
      AND ms.status = 'completed';

    RETURN IFNULL(total_sessions, 0);
END;
//

DELIMITER ;

-- Check completed sessions for Maitreyi Vijay (ID = 1)
SELECT MentorSessionCount(1) AS TotalCompletedSessions;

