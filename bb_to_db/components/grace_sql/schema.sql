DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS class_selections;
DROP TABLE IF EXISTS locations;


CREATE TABLE students(
    idBlackbaud NVARCHAR(20) PRIMARY KEY,
    idLocation TINYINT,
    idRenWeb NVARCHAR(100),
    nameLast NVARCHAR(100),
    nameMiddle  NVARCHAR(100),
    nameFirst NVARCHAR(100),
    namePreferred NVARCHAR(100),
    gradeLevel NVARCHAR(100),
    emailAddress NVARCHAR(100),
    gender NVARCHAR(100),
    graduationYear NVARCHAR(100),
    birthDate NVARCHAR(100),
    ethnicity NVARCHAR(100),
    race NVARCHAR(100),
    sam NVARCHAR(100), 
    userName NVARCHAR(100)
);

CREATE TABLE staff(
    idBlackbaud NVARCHAR(20) PRIMARY KEY,
    idLocation TINYINT,
    idRenWeb NVARCHAR(100),
    nameLast NVARCHAR(100),
    nameMiddle  NVARCHAR(100),
    nameFirst NVARCHAR(100),
    namePreferred NVARCHAR(100),
    jobBusiness NVARCHAR(100),
    emailAddress NVARCHAR(100),
    jobTitle NVARCHAR(100),
    jobOrg NVARCHAR(100),
    sam NVARCHAR(100),
    userName NVARCHAR(100),
    groupCA BIT DEFAULT 0,
    groupHS BIT DEFAULT 0,
    groupMS78 BIT DEFAULT 0,
    groupMS56 BIT DEFAULT 0,
    groupEL BIT DEFAULT 0,
    groupGU BIT DEFAULT 0,
    groupGAFE BIT DEFAULT 0,
    groupSUB BIT DEFAULT 0
);

CREATE TABLE [dbo].[enrollments](
    [id] INTEGER IDENTITY(1,1) PRIMARY KEY,
    [NexusID] UNIQUEIDENTIFIER NOT NULL,        
    [idBlackbaud] NVARCHAR(20) NULL,            
    [idRoster] NVARCHAR(100) NULL,              
    [idClass] NVARCHAR(100) NOT NULL,           
    [idSection] NVARCHAR(100) NULL,
    [idLocation] NVARCHAR(50) NULL,
    CONSTRAINT FK_Enroll_NexusID FOREIGN KEY ([NexusID]) 
        REFERENCES [dbo].[Constituents]([NexusID]) ON DELETE CASCADE,
    CONSTRAINT FK_Enroll_ClassRef FOREIGN KEY ([idClass]) 
        REFERENCES [dbo].[class_selections]([idClass]) ON UPDATE CASCADE
);
GO

CREATE TABLE [dbo].[courses](
    [id] INTEGER IDENTITY(1,1) PRIMARY KEY,
    [idCourse] NVARCHAR(100) NOT NULL UNIQUE, 
    [courseTitle] NVARCHAR(100) NOT NULL,
    [idLocation] NVARCHAR(50) NULL
);
GO

CREATE TABLE [dbo].[class_selections](
    [id] INTEGER IDENTITY(1,1) PRIMARY KEY,
    [idClass] NVARCHAR(100) NOT NULL UNIQUE, 
    [idCourse] NVARCHAR(100) NOT NULL,          
    [classNumber] NVARCHAR(100) NULL,           
    [idInstructor] NVARCHAR(100) NULL,          
    [idLocation] NVARCHAR(50) NULL,
    CONSTRAINT FK_Class_CourseRef FOREIGN KEY ([idCourse]) 
        REFERENCES [dbo].[courses]([idCourse]) ON UPDATE CASCADE
);
GO

CREATE TABLE locations(
    id int IDENTITY PRIMARY KEY,
    idLocation NVARCHAR(5),
    campusCode NVARCHAR(5),
    campusName NVARCHAR(25),
    schoolOU NVARCHAR(25),
    campusNumber NVARCHAR(5)
);

INSERT INTO locations(idLocation,campusCode,campusName,schoolOU,campusNumber)VALUES('1825','OJ','Old Jacksonville','Elementary','1825');
INSERT INTO locations(idLocation,campusCode,campusName,schoolOU,campusNumber)VALUES('1826','UB','University Blvd','Middle School','1826');
INSERT INTO locations(idLocation,campusCode,campusName,schoolOU,campusNumber)VALUES('1827','UB','University Blvd','High School','1827');
INSERT INTO locations(idLocation,campusCode,campusName,schoolOU,campusNumber)VALUES('1828','UB','University Blvd','GraceU','1828');
INSERT INTO locations(idLocation,campusCode,campusName,schoolOU,campusNumber)VALUES('EL','OJ','Old Jacksonville','Elementary','1825');
INSERT INTO locations(idLocation,campusCode,campusName,schoolOU,campusNumber)VALUES('MS','UB','University Blvd','Middle School','1826');
INSERT INTO locations(idLocation,campusCode,campusName,schoolOU,campusNumber)VALUES('HS','UB','University Blvd','High School','1827');
INSERT INTO locations(idLocation,campusCode,campusName,schoolOU,campusNumber)VALUES('GU','UB','University Blvd','GraceU','1828');
INSERT INTO locations(idLocation,campusCode,campusName,schoolOU,campusNumber)VALUES('CA','UB','University Blvd','Central Administration','1827');
INSERT INTO locations(idLocation,campusCode,campusName,schoolOU,campusNumber)VALUES('','','None','','');
