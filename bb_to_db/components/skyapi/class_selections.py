import requests, json
from components import grace_sql
from . import shared

def GetClassSelectionsFromBB(authData):

    global locationsList
    locationsList = grace_sql.queries.get.getLocationsTable()

    headers = {
        "Authorization" : "Bearer " + authData['accessToken'],
        "Bb-Api-Subscription-Key": authData['subKey']
    }


    i = 1
    loop = True
    classSelectionsList = {}
    selectionsFileOut = "/selections.csv"

    print("[INFO] - Starting class selections data pull...")

    while(loop):
        selectionsListEndpoint = f"https://api.sky.blackbaud.com/school/v1/lists/advanced/77847?page={i}"
        request = requests.get(selectionsListEndpoint, headers=headers)
        returnData = json.loads(request.text)
        for row in returnData["results"]["rows"]:
            data = row["columns"]

            classSelection = grace_sql.classes.ClassSelection()
            
            classSelection.idClass  = data[7].get('value',"")
            classSelection.idCourse  = data[3].get('value',"")
            classSelection.idLocation  = data[0].get('value',"")
            classSelection.classNumber  = data[1].get('value',"")
            classSelection.idInstructor  = data[4].get('value',"")


            classSelection = ParseClassSelection(classSelection)
            classSelectionsList[classSelection.idClass] = classSelection

        if(returnData["count"] != 1000):
            loop = False
            break
        else:
            i += 1

    print("[INFO] - Finished class selection data pull...")
    return classSelectionsList


def ParseClassSelection(classSelection):
    classSelection.idLocation = shared.ParseLocation(classSelection.idLocation,locationsList)
    
    return classSelection

def SendToDb(classSelectionsList):
    print("[INFO] - Starting class selections push to DB...")

    classSelectionsDbList = grace_sql.queries.get.GetClassSelectionsTable()
   
    classSelectionsListIDS = list(sorted(classSelectionsList.keys()))

    classSelectionsDbListIDS = list(sorted(classSelectionsDbList.keys()))

    addToDb = list(set(classSelectionsListIDS) -  set(classSelectionsDbListIDS))

    removeFromDb = list(set(classSelectionsDbListIDS) - set(classSelectionsListIDS))

    updateDb = list(set(classSelectionsListIDS) - set(addToDb))
    
    for classSelection in addToDb:
        grace_sql.queries.insert.InsertDbClassSelection(classSelectionsList[classSelection])

    for classSelection in removeFromDb:
        grace_sql.queries.delete.RemoveDbClassSelection(classSelectionsDbList[classSelection])

    for id in updateDb:
        if not classSelectionsList[id] == classSelectionsDbList[id]:
            grace_sql.queries.update.UpdateDbClassSelection(classSelectionsList[id])

    print("[INFO] - Finished class selections push to DB...")

    return