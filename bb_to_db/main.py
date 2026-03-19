from components import skyapi,csv_writer , grace_sql, os
import time, datetime, threading

dirname = os.path.dirname(__file__)

csv_output = dirname + "/components/csv"
pathEnrollments = f"{csv_output}/academicEnrollments.csv"
pathClassSelections = f"{csv_output}/classSelections.csv"
pathCourses = f"{csv_output}/courses.csv"
pathStaffFaculty = f"{csv_output}/staffFaculty.csv"
pathStudents = f"{csv_output}/students.csv"

MAXRETRIES = 3
RETRY_TIMOUT = 30

def Students(authData):
    i=1
    while i < MAXRETRIES:
        studentData = skyapi.students.GetStudentsFromBB(authData)
        
        if len(studentData) == 0:
            if i == MAXRETRIES:
                print("[ERROR] - MAX RETRIES REACHED ABORTING STUDENT PULL!")
                break
            i+=1
            print("[WARNING] - Student pull empty! retrying.")
            time.sleep(RETRY_TIMOUT)

        else:
            csv_writer.WriteListToCsv(studentData,pathStudents)
            skyapi.students.SendToDb(studentData)
            break

def Staff(authData):
    i=1
    while i < MAXRETRIES:
        staffData = skyapi.staff.GetStaffFromBB(authData)

        if len(staffData) == 0:
                if i == MAXRETRIES:
                    print("[ERROR] - MAX RETRIES REACHED ABORTING STAFF PULL!")
                    break
                i+=1
                print("[WARNING] - Staff pull empty! retrying.")
                time.sleep(RETRY_TIMOUT)

        else:
            csv_writer.WriteListToCsv(staffData,pathStaffFaculty)
            skyapi.staff.SendToDb(staffData)
            break

def Enrollments(authData):
    i=1
    while i < MAXRETRIES:
        enrollmentData = skyapi.enrollments.GetEnrollmentsFromBB(authData)

        if len(enrollmentData) == 0:
                if i == MAXRETRIES:
                    print("[ERROR] - MAX RETRIES REACHED ABORTING ENROLLMENTS PULL!")
                    break
                i+=1
                print("[WARNING] - Enrollments pull empty! retrying.")
                time.sleep(RETRY_TIMOUT)

        else:
            csv_writer.WriteListToCsv(enrollmentData,pathEnrollments)
            skyapi.enrollments.SendToDb(enrollmentData)
            break

def ClassSelections(authData):
    i=1
    while i < MAXRETRIES:
        classSelectionData = skyapi.class_selections.GetClassSelectionsFromBB(authData)
        
        if len(classSelectionData) == 0:
                if i == MAXRETRIES:
                    print("[ERROR] - MAX RETRIES REACHED ABORTING CLASS SELECTIONS PULL!")
                    break
                i+=1
                print("[WARNING] - Class Selections pull empty! retrying.")
                time.sleep(RETRY_TIMOUT)

        else:
            csv_writer.WriteListToCsv(classSelectionData,pathClassSelections)
            skyapi.class_selections.SendToDb(classSelectionData)
            break

def Courses(authData):
    i=1
    while i < MAXRETRIES:
        courseData = skyapi.courses.GetCoursesFromBB(authData)

        if len(courseData) == 0:
                if i == MAXRETRIES:
                    print("[ERROR] - MAX RETRIES REACHED ABORTING COURSE PULL!")
                    break
                i+=1
                print("[WARNING] - Course pull empty! retrying.")
                time.sleep(RETRY_TIMOUT)

        else:
            csv_writer.WriteListToCsv(courseData,pathCourses)
            skyapi.courses.SendToDb(courseData)
            break


def Threads():

    authData = skyapi.auth.ConnectSkyAPI()
    threads = []
    processes = [Students]
    for process in processes:
        thread = threading.Thread(target=process,args=(authData,))
        threads.append(thread)
        thread.start()
        time.sleep(.01)

    for thread in threads:
        thread.join()


    Courses(authData)
    ClassSelections(authData)
    Enrollments(authData)
    


def main():

    grace_sql.db.init_db()
    Threads()



if __name__ == "__main__":

    startTime = datetime.datetime.now()
    main()
    endTime = datetime.datetime.now()
    runTime =  endTime - startTime
    print(f"[INFO] - Run Time:  {runTime.total_seconds()} seconds")