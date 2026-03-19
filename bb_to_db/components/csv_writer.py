import csv, os ,shutil
from pathlib import Path




def WriteListToCsv(listObj,path):
    pathDir = Path(path)
    if not os.path.exists(pathDir.parent.absolute()):
        os.makedirs(pathDir.parent.absolute())


    if os.path.isfile(f"{path}.old"):
        os.remove(f"{path}.old")
        
    if os.path.isfile(path):
        shutil.copy(path, f"{path}.old")

    with open(path, "w+") as fileObj:
        writer = csv.writer(fileObj)
        key = list(listObj.keys())[0]
        writer.writerow(listObj[key].toHeader())
        for item in listObj:
            writer.writerow(listObj[item].toIterable())