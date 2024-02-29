-- TODO - check if valid schema attrs

-- Define User and their emails
CREATE TABLE User (
    UCINetID VARCHAR(20),
    firstName VARCHAR(20),
    middleName VARCHAR(20),
    lastName VARCHAR(20),
    PRIMARY KEY (UCINetID)
);

-- Define user email
CREATE TABLE UserEmails (
	UCINetID VARCHAR(20),
    email VARCHAR(30) NOT NULL,
	PRIMARY KEY (UCINetID, email),
    FOREIGN KEY (UCINetID) REFERENCES User(UCINetID)
        ON DELETE CASCADE
);

-- Student extends User
CREATE TABLE Student (
	UCINetID VARCHAR(20),
    PRIMARY KEY (UCINetID),
	FOREIGN KEY (UCINetID) REFERENCES User(UCINetID)
);

-- Administrator extends User
CREATE TABLE Administrator (
	UCINetID VARCHAR(20),
    PRIMARY KEY (UCINetID),
    FOREIGN KEY (UCINetID) REFERENCES User(UCINetID)
);

-- Define Course
CREATE TABLE Course (
	courseID INTEGER,
    title VARCHAR(100),
	-- Assumes that quarter is in the format
	-- of F22 (For Fall quarter 2022)
    quarter CHAR(3),
    PRIMARY KEY (courseID)
);


-- Define Project
-- Responsible for 1:N course project relation with forced
-- participation on the project side
CREATE TABLE Project (
    projectID INTEGER,
    courseID INTEGER NOT NULL,
    name VARCHAR(20),
    description VARCHAR(100),
    PRIMARY KEY (projectID),
    FOREIGN KEY (courseID) REFERENCES Course(courseID)
);


-- Define Machine
CREATE TABLE Machine (
    machineID INTEGER,
    -- max ip4 address char length in decimal
    IPAddress VARCHAR(15),
    hostname VARCHAR(20),
    operationalStatus ENUM('Active', 'Down'),
    location VARCHAR(20),
    PRIMARY KEY (machineID)
);


-- Student, project, machine relation ('use' relation)
CREATE TABLE studentUse (
    UCINetID VARCHAR(20),
    projectID INTEGER,
    machineID INTEGER,
    startDate DATETIME,
    endDate DATETIME,
    PRIMARY KEY (UCINetID, projectID, machineID),
    FOREIGN KEY (UCINetID) REFERENCES Student(UCINetID),
    FOREIGN KEY (projectID) REFERENCES Project(projectID),
    FOREIGN KEY (machineID) REFERENCES Machine(machineID)
);


-- Administrator machine relation
CREATE TABLE manages (
    UCINetID VARCHAR(20),
    machineID INTEGER,
    PRIMARY KEY (UCINetID, machineID),
    FOREIGN KEY (UCINetID) REFERENCES Administrator(UCINetID),
    FOREIGN KEY (machineID) REFERENCES Machine(machineID)
);
