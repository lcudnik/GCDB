from components import grace_sql

def UpdateDbStudent(student, nexus_id, session_id=None):
    db = grace_sql.db.get_db()
    cursor = db.cursor()
    
    sql = """
        UPDATE Constituents SET
            ExternalID_School = ?,
            nameFirst = ?,
            nameLast = ?,
            nameMiddle = ?,
            namePreferred = ?,
            emailPersonal = ?,
            locationID = ?,
            DoB = ?,
            gender = ?,
            CurrentSyncID = ?
        WHERE NexusID = ?
    """

    params = (
        student.idBlackbaud, student.nameFirst, student.nameLast,student.nameMiddle, 
        student.namePreferred, student.emailAddress, student.idLocation, 
        student.birthDate,student.gender , session_id, nexus_id
    )
    cursor.execute(sql, params)
    db.commit()
    db.close()

def UpdateDbStaff(staff):
    staffQuery = (f"""UPDATE staff SET
            idLocation = {staff.idLocation},
            idRenWeb = '{staff.idRenWeb}',
            nameLast = '{staff.nameLast}',
            nameMiddle = '{staff.nameMiddle}',
            nameFirst = '{staff.nameFirst}',
            namePreferred = '{staff.namePreferred}',
            jobBusiness = '{staff.jobBusiness}',
            emailAddress = '{staff.emailAddress}',
            jobTitle = '{staff.jobTitle}',
            jobOrg = '{staff.jobOrg}',
            sam = '{staff.sam}',
            userName = '{staff.userName}',
            groupCA = '{staff.groupCA}',
            groupHS = '{staff.groupHS}',
            groupMS78 = '{staff.groupMS78}',
            groupMS56 = '{staff.groupMS56}',
            groupEL = '{staff.groupEL}',
            groupGU = '{staff.groupGU}',
            groupGAFE = '{staff.groupGAFE}',
            groupSUB = '{staff.groupSUB}'
            WHERE idBlackbaud = '{staff.idBlackbaud}';""")
    
    db = grace_sql.db.get_db()
    curser = db.cursor()

    curser.execute(staffQuery)
    db.commit()
    grace_sql.db.close_db(db)

def UpdateDbEnrollment(enrollment):
    enrollmentQuery = (f"UPDATE enrollments SET idClass = '{enrollment.idClass}', idSection = '{enrollment.idSection}', idBlackbaud = '{enrollment.idBlackbaud}', idLocation = '{enrollment.idLocation}' WHERE idRoster = '{enrollment.idRoster}';")
    
    db = grace_sql.db.get_db()
    curser = db.cursor()

    curser.execute(enrollmentQuery)
    db.commit()
    grace_sql.db.close_db(db)


def UpdateDbCourse(course):
    courseQuery = (f"UPDATE courses SET idLocation = {course.idLocation},courseTitle = '{course.courseTitle}' WHERE idCourse = '{course.idCourse}';")
    
    db = grace_sql.db.get_db()
    curser = db.cursor()

    curser.execute(courseQuery)
    db.commit()
    grace_sql.db.close_db(db)

def UpdateDbClassSelection(classSelection):
    classSelectionQuery = (f"UPDATE class_selections SET idCourse = '{classSelection.idCourse}',idLocation = '{classSelection.idLocation}',classNumber = '{classSelection.classNumber}',idInstructor = '{classSelection.idInstructor}' WHERE idClass = '{classSelection.idClass}';")
    
    db = grace_sql.db.get_db()
    curser = db.cursor()

    curser.execute(classSelectionQuery)
    db.commit()
    grace_sql.db.close_db(db)
