import json, pyodbc, os



def get_db():
    dbConfigPath =  r'\\uba-scripts\c$\Scripts\local_assets\grace_bb_stack\db.json'
    
    with open(dbConfigPath) as f:
        dbConfig = json.load(f)
    
    connection_string = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER=tcp:{dbConfig['serverIP']}\\GCDB;"
        f"DATABASE={dbConfig['dbName']};"
        f"Trusted_Connection=yes;"
        f"TrustServerCertificate=yes;"
    )

    db = pyodbc.connect(connection_string)
    return db


def close_db(db):
    db.close()

def init_db():
    db = get_db()
    cursor = db.cursor()

    try:
        test = cursor.execute("SELECT * FROM locations;")
    except:
        executeScriptsFromFile(dirname + "/schema.sql",db)
    
    close_db(db)
        


def executeScriptsFromFile(filename,db):
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')
    cursor = db.cursor()
    for command in sqlCommands:
        try:
            if command.strip() != '':
                cursor.execute(command.replace("\n",""))
                db.commit()
        except IOError:
            print("Command skipped: ")
