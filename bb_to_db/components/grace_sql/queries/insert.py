from components import grace_sql

def InsertDbStudent(student, session_id=None):
    db = grace_sql.db.get_db()
    cursor = db.cursor()
    
    # We use NEWID() for the NexusID and include the Sync Session ID
    sql = """
        INSERT INTO Constituents (
           NexusID,ExternalID_School,nameFirst,nameLast,nameMiddle,namePreferred,emailPersonal,locationID,DoB,gender,CurrentSyncID
        ) VALUES (NEWID(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        student.idBlackbaud, student.nameFirst, student.nameLast,student.nameMiddle, 
        student.namePreferred, student.emailAddress, student.idLocation, 
        student.birthDate,student.gender , session_id
    )
    cursor.execute(sql, params)
    db.commit()
    db.close()

def InsertDbStaff(staff):
    staffQuery = (f"INSERT INTO staff(idBlackbaud,idLocation,idRenWeb,nameLast,nameMiddle,nameFirst,namePreferred,jobBusiness,emailAddress,jobTitle,jobOrg,sam,userName,groupCA,groupHS,groupMS78,groupMS56,groupEL,groupGU,groupGAFE,groupSUB)VALUES('{staff.idBlackbaud}','{staff.idLocation}','{staff.idRenWeb}','{staff.nameLast}','{staff.nameMiddle}','{staff.nameFirst}','{staff.namePreferred}','{staff.jobBusiness}','{staff.emailAddress}','{staff.jobTitle}','{staff.jobOrg}','{staff.sam}','{staff.userName}','{staff.groupCA}','{staff.groupHS}','{staff.groupMS78}','{staff.groupMS56}','{staff.groupEL}','{staff.groupGU}','{staff.groupGAFE}','{staff.groupSUB}');")
    
    db = grace_sql.db.get_db()
    curser = db.cursor()

    curser.execute(staffQuery)
    db.commit()
    grace_sql.db.close_db(db)

def InsertDbCourse(course):
    courseQuery = (f"INSERT INTO courses(idCourse,idLocation,courseTitle)VALUES('{course.idCourse}','{course.idLocation}','{course.courseTitle}');")
    
    db = grace_sql.db.get_db()
    curser = db.cursor()

    curser.execute(courseQuery)
    db.commit()
    grace_sql.db.close_db(db)

def InsertDbEnrollment(enrollment):

    NexusID = grace_sql.queries.get.findConstituent(enrollment.idBlackbaud)
    if NexusID:
        enrollmentQuery = (f"INSERT INTO enrollments(NexusID, idRoster,idClass,idSection, idBlackbaud,idLocation)VALUES('{NexusID}','{enrollment.idRoster}','{enrollment.idClass}','{enrollment.idSection}','{enrollment.idBlackbaud}','{enrollment.idLocation}');")
    
        db = grace_sql.db.get_db()
        curser = db.cursor()

        curser.execute(enrollmentQuery)
        db.commit()
        grace_sql.db.close_db(db)

def InsertDbClassSelection(classSelection):
    classSelectionQuery = f"INSERT INTO class_selections(idClass,idCourse,idLocation,classNumber,idInstructor)VALUES('{classSelection.idClass}','{classSelection.idCourse}','{classSelection.idLocation}','{classSelection.classNumber}','{classSelection.idInstructor}');"
    
    db = grace_sql.db.get_db()
    curser = db.cursor()

    curser.execute(classSelectionQuery)
    db.commit()
    grace_sql.db.close_db(db)
