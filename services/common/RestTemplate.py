
import requests
import json

class RestTemplate:

    def doGet(self,endpoint,data,headers):
        data_json = json.dumps(data)
        response = requests.get(endpoint, data=data_json, headers=headers)
        if(response.status_code == 200):
            print(response.text)
            return response.json()
        else:
            response.raise_for_status()

    def doPost(self,endpoint,data,headers):
        data_json = json.dumps(data)
        response = requests.post(endpoint, data=data_json, headers=headers)
        print(response.text)
        if(response.status_code == 200):
            return response.json()
        else:
            response.raise_for_status()
