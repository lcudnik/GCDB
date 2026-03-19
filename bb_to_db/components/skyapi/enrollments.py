import requests, json
from components.skyapi import shared
from components import grace_sql


def GetEnrollmentsFromBB(authData):

    global locationsList
    locationsList = grace_sql.queries.get.getLocationsTable()
    
    headers = {
        "Authorization" : "Bearer " + authData['accessToken'],
        "Bb-Api-Subscription-Key": authData['subKey']
    }


    i = 1
    loop = True
    enrollmentsList = {}
    staffFileOut = "/enrollments.csv"

    print("[INFO] - Starting academic enrollments data pull...")

    while(loop):
        enrollmentsListEndpoint = f"https://api.sky.blackbaud.com/school/v1/lists/advanced/82491?page={i}"
        request = requests.get(enrollmentsListEndpoint, headers=headers)
        returnData = json.loads(request.text)
        for row in returnData["results"]["rows"]:
            data = row["columns"]

            enrollment = grace_sql.classes.Enrollment()

            enrollment.idRoster = (data[5].get('value',"") + "-" + data[2].get('value',""))
            enrollment.idClass = data[5].get('value',"")
            enrollment.idSection = data[1].get('value',"")
            enrollment.idBlackbaud = data[2].get('value',"")
            enrollment.idLocation = data[0].get('value',"")

            enrollment.idLocation = shared.ParseLocation(enrollment.idLocation, locationsList)

            enrollmentsList[enrollment.idRoster] = enrollment
        if(returnData["count"] != 1000):
            loop = False
            break
        else:
            i += 1


    print("[INFO] - Finished enrollments data pull...")
    return enrollmentsList

def SendToDb(enrollmentsList):
    print("[INFO] - Starting enrollments push to db...")

    enrollmentsDbList = grace_sql.queries.get.GetEnrollmentsTable()
   
    enrollmentsListIDS = list(sorted(enrollmentsList.keys()))

    enrollmentsDbListIDS = list(sorted(enrollmentsDbList.keys()))

    addToDb = list(set(enrollmentsListIDS) -  set(enrollmentsDbListIDS))

    removeFromDb = list(set(enrollmentsDbListIDS) - set(enrollmentsListIDS))

    updateDb = list(set(enrollmentsListIDS) - set(addToDb))
    
    for enrollment in addToDb:
        grace_sql.queries.insert.InsertDbEnrollment(enrollmentsList[enrollment])

    for enrollment in removeFromDb:
        grace_sql.queries.delete.RemoveDbEnrollment(enrollmentsDbList[enrollment])

    for id in updateDb:
        if not enrollmentsDbList[id] == enrollmentsList[id]:
            grace_sql.queries.update.UpdateDbEnrollment(enrollmentsList[id])

    print("[INFO] - Finished enrollments push to db...")

    return