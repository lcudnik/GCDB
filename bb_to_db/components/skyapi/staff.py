import requests, json
from components import grace_sql

from . import shared


def GetStaffFromBB(authData):

    global locationsList
    locationsList = grace_sql.queries.get.getLocationsTable()

    headers = {
        "Authorization" : "Bearer " + authData['accessToken'],
        "Bb-Api-Subscription-Key": authData['subKey']
    }


    i = 1
    loop = True
    staffList = {}
    staffFileOut = "/staff.csv"

    print("[INFO] - Starting staff data pull...")

    while(loop):
        staffListEndpoint = f"https://api.sky.blackbaud.com/school/v1/lists/advanced/82457?page={i}"
        request = requests.get(staffListEndpoint, headers=headers)
        returnData = json.loads(request.text)
        for row in returnData["results"]["rows"]:
            data = row["columns"]

            staff = grace_sql.classes.Staff()

            staff.idLocation = data[0].get('value',"").replace("'","`")
            staff.idBlackbaud = data[1].get('value',"").replace("'","`")
            staff.idRenWeb = data[2].get('value',"").replace("'","`")
            staff.nameLast = data[3].get('value',"").replace("'","`")
            staff.nameMiddle  = data[5].get('value',"").replace("'","`")
            staff.nameFirst = data[6].get('value',"").replace("'","`")
            staff.namePreferred = data[7].get('value',"").replace("'","`")
            staff.jobBusiness = data[4].get('value',"").replace("'","`")
            staff.jobTitle = data[10].get('value',"").replace("'","`")
            staff.jobOrg = data[11].get('value',"").replace("'","`")
            staff.groupCA = data[12].get('value',"False").replace("'","`")
            staff.groupHS = data[13].get('value',"False").replace("'","`")
            staff.groupMS78 = data[14].get('value',"False").replace("'","`")
            staff.groupMS56 = data[15].get('value',"False").replace("'","`")
            staff.groupEL = data[16].get('value',"False").replace("'","`")
            staff.groupGU = data[17].get('value',"False").replace("'","`")
            staff.groupGAFE = data[18].get('value',"False").replace("'","`")
            staff.groupSUB = data[19].get('value',"False").replace("'","`")

            staff = ParseStaff(staff)
            staffList[staff.idBlackbaud] = staff

        if(returnData["count"] != 1000):
            loop = False
            break
        else:
            i += 1
    print("[INFO] - Finished staff data pull...")
    return staffList


def GenerateEmail(staff):
    if staff.namePreferred != '' and staff.namePreferred != staff.nameFirst:
        useName = staff.namePreferred 
    else:
        useName = staff.nameFirst
    
    cleanUN = shared.RemoveDiacriticsAndSpaces(useName).replace("`","")
    cleanLN = shared.RemoveDiacriticsAndSpaces(staff.nameLast).replace("`","")
    cleanFN = shared.RemoveDiacriticsAndSpaces(staff.nameFirst).replace("`","")
    
    email = cleanUN.lower() + "." + cleanLN.lower() + "@gracetyler.org"
    staff.emailAddress = shared.RemoveDiacriticsAndSpaces(email)

    
    samPre = cleanUN + "." + cleanLN
    if (len(samPre) > 20):
        staff.sam = samPre.Substring[:20]
    else:
        staff.sam = samPre

    staff.userName = samPre.lower()
    return staff


def ParseBools(staff):
    groups = ["groupCA","groupHS","groupMS78","groupMS56","groupEL","groupGU","groupGAFE","groupSUB"]

    for group in groups:
        if (getattr(staff, group) == True):
            setattr(staff,group,1)
        else:
            setattr(staff,group,0)
    return staff

def ParseStaff(staff):
    staff = GenerateEmail(staff)

    staff.idLocation = shared.ParseLocation(staff.idLocation,locationsList)

    #staff = ParseBools(staff)
    return staff


def SendToDb(staffList):
    print("[INFO] - Starting staff push to db...")

    staffDbList = grace_sql.queries.get.GetStaffTable()
   
    staffListIDS = list(sorted(staffList.keys()))

    staffDbListIDS = list(sorted(staffDbList.keys()))

    addToDb = list(set(staffListIDS) -  set(staffDbListIDS))

    removeFromDb = list(set(staffDbListIDS) - set(staffListIDS))

    updateDb = list(set(staffListIDS) - set(addToDb))
    
    for staff in addToDb:
        grace_sql.queries.insert.InsertDbStaff(staffList[staff])

    for staff in removeFromDb:
        grace_sql.queries.delete.RemoveDbStaff(staffDbList[staff])

    for id in updateDb:
        if not staffList[id] == staffDbList[id]:
            grace_sql.queries.update.UpdateDbStaff(staffList[id])

    print("[INFO] - Finished staff push to db...")

    return