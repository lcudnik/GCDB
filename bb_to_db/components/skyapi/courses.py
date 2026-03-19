import requests, json
from components import grace_sql
from . import shared


def GetCoursesFromBB(authData):

    global locationsList
    locationsList = grace_sql.queries.get.getLocationsTable()

    headers = {
        "Authorization" : "Bearer " + authData['accessToken'],
        "Bb-Api-Subscription-Key": authData['subKey']
    }


    i = 1
    loop = True
    coursesList = {}

    print("[INFO] - Starting academic enrollments data pull...")

    while(loop):
        coursesListEndpoint = f"https://api.sky.blackbaud.com/school/v1/lists/advanced/77848?page={i}"
        request = requests.get(coursesListEndpoint, headers=headers)
        returnData = json.loads(request.text)
        for row in returnData["results"]["rows"]:
            data = row["columns"]

            course = grace_sql.classes.Course()

            course.idCourse = data[0].get('value',"")
            course.courseTitle = data[1].get('value',"")
            course.idLocation = data[2].get('value',"")

            course = ParseCourse(course)
            coursesList[course.idCourse]= course

        if(returnData["count"] != 1000):
            loop = False
            break
        else:
            i += 1
            
    print("[INFO] - Finished course data pull...")
    return coursesList


def ParseCourse(course):
    course.idLocation = shared.ParseLocation(course.idLocation,locationsList)
    
    return course


def SendToDb(coursesList):
    print("[INFO] - Starting courses push to db...")

    coursesDbList = grace_sql.queries.get.GetCoursesTable()
   
    coursesListIDS = list(sorted(coursesList.keys()))

    coursesDbListIDS = list(sorted(coursesDbList.keys()))

    addToDb = list(set(coursesListIDS) -  set(coursesDbListIDS))

    removeFromDb = list(set(coursesDbListIDS) - set(coursesListIDS))

    updateDb = list(set(coursesListIDS) - set(addToDb))
    
    for course in addToDb:
        grace_sql.queries.insert.InsertDbCourse(coursesList[course])

    for course in removeFromDb:
        grace_sql.queries.delete.RemoveDbCourse(coursesDbList[course])

    for id in updateDb:
        if not coursesList[id] == coursesDbList[id]:
            grace_sql.queries.update.UpdateDbCourse(coursesList[id])

    print("[INFO] - Finished courses push to db...")


    return