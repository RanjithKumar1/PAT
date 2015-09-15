
import requests
import json

class RestTemplate:

    def doGet(self,endpoint,data,headers):
        data_json = json.dumps(data)
        response = requests.get(endpoint, data=data_json, headers=headers)
        if(response.status_code == 200 or response.status_code == 201):
            print(response.text)
            return response.json()
        else:
            response.raise_for_status()

    def doPost(self,endpoint,data,headers):
        data_json = json.dumps(data)
        response = requests.post(endpoint, data=data_json, headers=headers)
        print(response.status_code)
        if(response.status_code == 200 or response.status_code == 201):
            print(response.text)
            return response.json()
        else:
            response.raise_for_status()

    def doPatch(self,endpoint,data,headers):
        data_json = json.dumps(data)
        response = requests.patch(endpoint, data=data_json, headers=headers)
        print(response.text)
        print(response.status_code)
        if(response.status_code == 200 or response.status_code == 201):
            return response.json()
        else:
            response.raise_for_status()

    def doPut(self,endpoint,data,headers):
        print(data)
        response = requests.put(endpoint,data, headers=headers)
        print(response.status_code)
        if(response.status_code == 204):
            return response.headers
        else:
            response.raise_for_status()
