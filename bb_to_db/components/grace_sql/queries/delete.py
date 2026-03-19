from components import grace_sql

def RemoveDbStudent(remove):

    db = grace_sql.db.get_db()
    curser = db.cursor()

    cascadeTables = ['students', 'enrollments']
    for table in cascadeTables:
        studentsQuery = f"DELETE FROM {table} WHERE {table}.idBlackbaud = '{remove.idBlackbaud}';"

        curser.execute(studentsQuery)

    db.commit()
    grace_sql.db.close_db(db)

def RemoveDbStaff(remove):

    db = grace_sql.db.get_db()
    curser = db.cursor()

    cascadeTables = ['staff', 'class_selections']
    for table in cascadeTables:
        if table == "staff":
            staffQuery = f"DELETE FROM {table} WHERE {table}.idBlackbaud = '{remove.idBlackbaud}';"
        else:
            staffQuery = f"DELETE FROM {table} WHERE {table}.idInstructor = '{remove.idBlackbaud}';"

        curser.execute(staffQuery)

    db.commit()
    grace_sql.db.close_db(db)

def RemoveDbCourse(remove):

    db = grace_sql.db.get_db()
    curser = db.cursor()

    coursesQuery = f"DELETE FROM courses WHERE courses.idCourse = '{remove.idCourse}';"

    curser.execute(coursesQuery)

    db.commit()
    grace_sql.db.close_db(db)

def RemoveDbEnrollment(remove):

    db = grace_sql.db.get_db()
    curser = db.cursor()


    enrollmentsQuery = f"DELETE FROM enrollments WHERE enrollments.idRoster = '{remove.idRoster}';"

    curser.execute(enrollmentsQuery)

    db.commit()
    grace_sql.db.close_db(db)

def RemoveDbClassSelection(remove):

    db = grace_sql.db.get_db()
    curser = db.cursor()


    classSelectionsQuery = f"DELETE FROM class_selections WHERE class_selections.idClass = '{remove.idClass}';"

    curser.execute(classSelectionsQuery)

    db.commit()
    grace_sql.db.close_db(db)
