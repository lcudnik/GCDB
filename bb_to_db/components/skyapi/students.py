import requests, json, datetime, uuid
from components import grace_sql

from . import shared



def GetStudentsFromBB(authData):
    global locationsList
    locationsList = grace_sql.queries.get.getLocationsTable()

    headers = {
        "Authorization" : "Bearer " + authData['accessToken'],
        "Bb-Api-Subscription-Key": authData['subKey']
    }

    i = 1
    loop = True
    studentList = {}
    studentFileOut = "/students.csv"

    print("[INFO] - Starting students data pull...")

    while(loop):
        studentListEndpoint = f"https://api.sky.blackbaud.com/school/v1/lists/advanced/77852?page={i}"
        request = requests.get(studentListEndpoint, headers=headers)
        returnData = json.loads(request.text)
        for row in returnData["results"]["rows"]:
            data = row["columns"]

            student = grace_sql.classes.Student()

            student.idLocation = data[0].get('value',"").replace("'","`")
            student.idBlackbaud = data[1].get('value',"").replace("'","`")
            student.idRenWeb = data[2].get('value',"").replace("'","`")
            student.nameLast = data[3].get('value',"").replace("'","`")
            student.nameMiddle = data[4].get('value',"").replace("'","`")
            student.nameFirst = data[5].get('value',"").replace("'","`")
            student.namePreferred = data[6].get('value',"").replace("'","`")
            student.gradeLevel = data[7].get('value',"").replace("'","`")
            student.gender = data[9].get('value',"").replace("'","`")
            student.graduationYear = data[10].get('value',"").replace("'","`")
            student.birthDate = data[11].get('value',"").replace("'","`")
            student.ethnicity = data[12].get('value',"").replace("'","`")
            student.race = data[13].get('value',"").replace("'","`")
            student.AccessCard = data[14].get('value',"")
            
            student = ParseStudents(student)
            studentList[student.idBlackbaud] = student
    
        if(returnData["count"] != 1000):
            loop = False
            break
        else:
            i += 1



    print("[INFO] - Finished students data pull...")
    return studentList


def GenerateEmail(student):
    cleanFN = shared.RemoveDiacriticsAndSpaces(student.nameFirst).replace("`","")
    cleanLN = shared.RemoveDiacriticsAndSpaces(student.nameLast).replace("`","")
    
    if student.gradeLevel > 10:
        emailAddress = cleanFN.lower() + "." + cleanLN.lower() + "@gracetyler.org"
        samLegnth = 20
    else:
        emailAddress = cleanFN.lower() + "." + cleanLN.lower() + "." + student.graduationYear[2:] + "@gracetyler.org"
        samLegnth = 17

    emailAddress = shared.RemoveDiacriticsAndSpaces(emailAddress)

    student.emailAddress = emailAddress

    samPre = cleanFN + "." + cleanLN

    if len(samPre) > samLegnth: 
        samPreTrn = samPre[:samLegnth]
    else:
        samPreTrn = samPre

    sam = samPreTrn + "." + student.graduationYear[2:]

    student.sam = sam
    student.userName = samPre.lower() + "." + student.graduationYear[2:]

    return student


def GradeLevel(gradYear):
    today = datetime.date.today()
    year = today.year
    if today.month < 6:
        year = today.year
    else:
        year = today.year + 1
    
    gradeLvl = 12 - (int(gradYear) - year)
    return gradeLvl

def CleanBirthDate(student):
    birthdate = student.birthDate[:10].replace("/","-")
    return birthdate




def ParseStudents(student):
    student.idLocation = shared.ParseLocation(student.idLocation, locationsList)
    student.gradeLevel = GradeLevel(student.graduationYear)
    student = GenerateEmail(student)
    student.birthDate = CleanBirthDate(student)

    return student


def SendToDb(studentsList):
    session_id = str(uuid.uuid4())
    print(f"[INFO] - Starting sync session: {session_id}")
   
    for bb_id, student in studentsList.items():
        # 1. Find the student
        nexus_id = grace_sql.queries.get.findConstituent(
            search_id=student.idBlackbaud,
            first=student.nameFirst,
            last=student.nameLast
        )

        if nexus_id:
            # 2. Update existing & Mark with Session ID
            grace_sql.queries.update.UpdateDbStudent(student, nexus_id, session_id)
        else:
            # 3. Insert new & Mark with Session ID
            grace_sql.queries.insert.InsertDbStudent(student, session_id)
            
    print("[INFO] - Sync Complete. Database is now an exact mirror of Blackbaud.")

