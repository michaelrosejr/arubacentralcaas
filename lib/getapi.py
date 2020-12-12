import requests
import json
import sys


class APICall:
    def __init__(self, central, token, url, apiPath, group_name, reqtype, payload = None):
        self.central = central
        self.token = token
        self.url = url
        self.apiPath = apiPath,
        self.group_name = group_name,
        self.reqtype = reqtype
        self.payload = payload

    def getData(self):

        while True:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.token['access_token'],
            }
            params = {"group_name": self.group_name[0]}

            if self.payload is None:
                payload = {}
            else:
                payload = self.payload

            if self.reqtype == "get":
                response = requests.get(
                    self.url
                    # + self.apiPath[0] + "?group_name=" + self.group_name[0],
                    + self.apiPath[0],
                    headers=headers,
                    params=params,
                    data=json.dumps(payload)
                )
            elif self.reqtype == "post":
                response = requests.post(
                    self.url
                    # + self.apiPath[0] + "?group_name=" + self.group_name[0],
                    + self.apiPath[0],
                    headers=headers,
                    params=params,
                    data=json.dumps(payload)
                )
            else:
                print("ERROR: No request type sent.")
                sys.exit(1)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                if response.status_code == 401:
                    print(f"Refreshing Aruba Central Token...")
                    newtoken = self.central.refreshToken(self.token)
                    if "access_token" in newtoken:
                        self.central.storeToken(newtoken)
                        self.central.central_info["token"] = newtoken
                        self.token = newtoken
                else:
                    print(f"Error: {err}")
                    break
                continue
            break
        return response.json()
