import requests, json, os

def ConnectSkyAPI():
    dirname = os.path.dirname(__file__)

    skyApiFile = r'\\UB-g-Script\c$\Scripts\local_assets\bb\skyapi.json'
    with open(skyApiFile, 'r') as f:
        authData = json.load(f)
    
    body = {
        "grant_type":'refresh_token',
        "refresh_token": authData['refreshToken'],
        "client_id":authData['clientId'],
        "client_secret":authData['clientSecret']
    }

    headers = {
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(authData['refreshUrl'],headers=headers, data=body)
    except:
        print("[ERROR] - Auth Failed!")
        
    try:
        responseData = json.loads(response.text)
        authData['refreshToken'] = responseData["refresh_token"]
        authData['accessToken'] = responseData["access_token"]
    except:
        print("Script Missing Locals Folder or needs Re-Auth.")

    # Serializing json
    json_object = json.dumps(authData, indent=4)
 
    # Writing to sample.json
    with open(skyApiFile, "w") as outfile:
        outfile.write(json_object)

    return authData

