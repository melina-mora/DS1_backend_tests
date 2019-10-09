import requests


def login(env_url, user, pw):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "App-Code": "DCMWebTool_App"
    }
    body = {
        "grant_type": "password",
        "scope": "security",
        "username": user,
        "password": pw
    }
    print("sign in")
    failed = True
    counter = 0
    while failed and counter < 10:
        try:
            response = requests.post(env_url + "/v2/secm/oam/oauth2/token", data=body, headers=headers)
            if response.status_code == 200:
                print("invalid status code")
        except Exception as e:
            print("login failed - %s" % e)
            counter += 1
            failed = True
        else:
            failed = False
        if counter > 10: break
    else:
        resp = response.json()
        token = resp["oauth2"]["access_token"]
        jwt = resp["jwt"]

        return {
            "Accept-Language": "en-US",
            "Content-Type": "application/json",
            "App-Code": "DCMWebTool_App",
            "Authorization": "Bearer " + token,
            "jwt": jwt
        }

    raise ("Failed to login")
