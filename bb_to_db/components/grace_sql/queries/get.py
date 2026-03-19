from components import grace_sql

def getLocationsTable():
    db = grace_sql.db.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM locations")
    results = {}
    for row in cursor.fetchall():
        location = grace_sql.classes.Location()
        location.idLocation = row.idLocation # Using row names is safer
        location.campusName = row.campusName
        location.campusCode = row.campusCode
        location.schoolOU = row.schoolOU
        results[row.idLocation] = location
    db.close()
    return results

def GetConstituentsTable():
    db = grace_sql.db.get_db()
    cursor = db.cursor()
    # Selecting from the new unified table
    cursor.execute("SELECT * FROM Constituents")
    results = {}
    for row in cursor.fetchall():
        results[row.ExternalID_School] = row.NexusID
    db.close()
    return results

def findConstituent(search_id=None, first=None, last=None, email=None):
    db_conn = grace_sql.db.get_db()
    cursor = db_conn.cursor()
    
    # The order here matches the procedure parameters: ID, First, Last, Email
    sql = "{CALL usp_FindConstituentCascading (?, ?, ?, ?)}"
    params = (search_id, first, last, email)
    
    cursor.execute(sql, params)
    row = cursor.fetchone()
    
    grace_sql.db.close_db(db_conn)

    if row:
        # returns the NexusID (GUID)
        return row.NexusID 
    return None


def GetStudentsTable(idBlackbaud=""):

    db = grace_sql.db.get_db()
    curser = db.cursor()
    
    if idBlackbaud == "":
        studentQuery = "SELECT * FROM students"
    else:
        studentQuery = f"SELECT * FROM students WHERE students.idBlackbaud = '{idBlackbaud}'"
    
    results = {}
    curser.execute(studentQuery)
    for row in curser.fetchall():
        student = grace_sql.classes.Student()

        student.idBlackbaud = row[0]
        student.idLocation = row[1]
        student.idRenWeb = row[2]
        student.nameLast = row[3]
        student.nameMiddle = row[4]
        student.nameFirst = row[5]
        student.namePreferred = row[6]
        student.gradeLevel = row[7]
        student.emailAddress = row[8]
        student.gender = row[9]
        student.graduationYear = row[10]
        student.birthDate = row[11]
        student.ethnicity = row[12]
        student.race = row[13]
        student.sam = row[14]
        student.userName = row[15]

        results[student.idBlackbaud] = student
    
    grace_sql.db.close_db(db)

    return results

def GetStaffTable(idBlackbaud=""):

    db = grace_sql.db.get_db()
    curser = db.cursor()
    
    if idBlackbaud == "":
        staffQuery = "SELECT * FROM staff"
    else:
        staffQuery = f"SELECT * FROM students WHERE staff.idBlackbaud = '{idBlackbaud}'"
    
    results = {}
    curser.execute(staffQuery)
    for row in curser.fetchall():
        staff = grace_sql.classes.Staff()
        
        staff.idBlackbaud = row[0]        
        staff.idLocation = row[1]
        staff.idRenWeb = row[2]
        staff.nameLast = row[3]
        staff.nameMiddle  = row[4]
        staff.nameFirst = row[5]
        staff.namePreferred = row[6]
        staff.jobBusiness = row[7]
        staff.emailAddress = row[8]
        staff.jobTitle = row[9]
        staff.jobOrg = row[10]
        staff.sam = row[11]
        staff.userName = row[12]
        staff.groupCA = str(row[13])
        staff.groupHS = str(row[14])
        staff.groupMS78 = str(row[15])
        staff.groupMS56 = str(row[16])
        staff.groupEL = str(row[17])
        staff.groupGU = str(row[18])
        staff.groupGAFE = str(row[19])
        staff.groupSUB = str(row[20])
        
        results[staff.idBlackbaud] = staff
    
    grace_sql.db.close_db(db)

    return results

def GetEnrollmentsTable(idBlackbaud=""):

    db = grace_sql.db.get_db()
    curser = db.cursor()
    
    if idBlackbaud == "":
        enrollmentQuery = "SELECT * FROM enrollments"
    else:
        enrollmentQuery = f"SELECT * FROM enrollments WHERE enrollments.idBlackbaud = '{idBlackbaud}'"
    
    results = {}
    curser.execute(enrollmentQuery)
    for row in curser.fetchall():
        enrollment = grace_sql.classes.Enrollment()

        enrollment.idRoster = row[2]
        enrollment.idClass = row[3]
        enrollment.idSection = row[5]
        enrollment.idBlackbaud = row[1]
        enrollment.idLocation = row[4]
        
        results[enrollment.idRoster] = enrollment
    
    grace_sql.db.close_db(db)

    return results

def GetCoursesTable():
    
    db = grace_sql.db.get_db()
    curser = db.cursor()
    

    courseQuery = "SELECT * FROM courses"

    results = {}
    curser.execute(courseQuery)
    for row in curser.fetchall():
        course = grace_sql.classes.Course()

        course.idCourse = row[0]
        course.courseTitle = row[1]
        course.idLocation = row[2]

        results[course.idCourse] = course
    
    grace_sql.db.close_db(db)

    return results

def GetClassSelectionsTable(idBlackbaud=""):
    
    db = grace_sql.db.get_db()
    curser = db.cursor()
    
    if idBlackbaud == "":
        classSelectionQuery = "SELECT * FROM class_selections"
    else:
        classSelectionQuery = f"SELECT * FROM class_selections WHERE class_selection.idInstructor = '{idBlackbaud}'"
    
    results = {}
    curser.execute(classSelectionQuery)
    for row in curser.fetchall():
        classSelection = grace_sql.classes.ClassSelection()

        classSelection.idClass  = row[1]
        classSelection.idCourse  = row[2]
        classSelection.idLocation  = row[3]
        classSelection.classNumber  = row[4]
        classSelection.idInstructor  = row[5]

        results[classSelection.idClass] = classSelection
    
    grace_sql.db.close_db(db)

    return results
    