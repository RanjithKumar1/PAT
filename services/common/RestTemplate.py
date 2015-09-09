
import requests
import json

class RestTemplate:

    headers = {'Content-type': 'application/json','Accept':'application/json'}

    def doGet(self,endpoint):
        response = requests.get(endpoint, headers=RestTemplate.headers)
        if(response.status_code == 200):
            return response.json()
        else:
            response.raise_for_status()

    def doGet(self,endpoint,data):
        data_json = json.dumps(data)
        response = requests.get(endpoint, data=data_json, headers=RestTemplate.headers)
        if(response.status_code == 200):
            return response.json()
        else:
            response.raise_for_status()

    def doGet(self,endpoint,data,headers):
        data_json = json.dumps(data)
        response = requests.get(endpoint, data=data_json, headers=headers)
        if(response.status_code == 200):
            print(response.text)
            return response.json()
        else:
            response.raise_for_status()

    def doPost(self,endpoint,data):
        data_json = json.dumps(data)
        response = requests.post(endpoint, data=data_json, headers=RestTemplate.headers)
        print(response.text)
        if(response.status_code == 200):
            return response.json()
        else:
            response.raise_for_status()