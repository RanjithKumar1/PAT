import base64
import time

from services.common.RestTemplate import RestTemplate
from services.common.CONST import CONST

class Compute:

    rest = RestTemplate()
    const = CONST()

    def __init__(self,endpoint,auth_token,tenant_id):
        self.url=endpoint
        self.auth_token=auth_token
        self.headers= {'Content-type': 'application/json','Accept':'application/json','X-Auth-Token':self.auth_token}
        self.tenant_id=tenant_id


    def get_quota(self):
        data={}
        response = Compute.rest.doGet(self.url+"/limits",data,self.headers)
        limits=response["limits"]["absolute"]
        response={}
        if limits["maxTotalRAMSize"] == limits["totalRAMUsed"]:
            response["ram"]="Ram exceeded the limit"

        if limits["maxTotalInstances"] == limits["totalInstancesUsed"]:
            response["instance"]="Instance count exceeded the limit"

        if limits["maxTotalCores"] == limits["totalCoresUsed"]:
            response["core"]="Total core exceeded the limit"

        return response

    def get_flavor_id(self, flavor_name):
        data={}
        response = Compute.rest.doGet(self.url+"/flavors",data,self.headers)
        flavors = response["flavors"]
        status = True
        for flavor in flavors:
            if flavor_name == flavor["name"]:
                return flavor["id"]
        return false

    def create_instance(self,image_id,flavor_id,user_data):
        data= {
            "server": {"name": "PATinstance1", "imageRef": image_id, "flavorRef": flavor_id,
                       "max_count": 1, "min_count": 1,"key_name":"PATKeyPair","user_data":user_data}
            }

        response = Compute.rest.doPost(self.url+"/servers",data,self.headers)
        print(response)
        return response["server"]["id"]

    def assign_floating_ip_to_instance(self,instance_id,floating_ip):
        data= {"addFloatingIp": {"address": floating_ip}}
        response = Compute.rest.doPostWithOutRes(self.url+"/servers/"+instance_id+"/action",data,self.headers)
        print(response)

    def Soft_reboot(self,instance_id):
        data= {"reboot": {"type": "SOFT"}}
        response = Compute.rest.doPostWithOutRes(self.url+"/servers/"+instance_id+"/action",data,self.headers)
        print(response)

    def wait_for_instance_active(self,instance_id):
        status=self.get_instance_creation_status(instance_id)
        while(status != self.const.ACTIVE):
            time.sleep(30)
            status=self.get_instance_creation_status(instance_id)

    def Soft_reboot(self,instance_id):
        data= {"reboot": {"type": "SOFT"}}
        response = Compute.rest.doPostWithOutRes(self.url+"/servers/"+instance_id+"/action",data,self.headers)
        print(response)

    def get_console_output(self,instance_id):
        data= {"os-getConsoleOutput": {"length": 50}}
        response = Compute.rest.doPost(self.url+"/servers/"+instance_id+"/action",data,self.headers)
        print(response)
        return response["output"]

    def terminate_instance(self,instance_id):
        data={}
        response = Compute.rest.doDelete(self.url+"/servers/"+instance_id,data,self.headers)
        print(response)

    def get_instance_creation_status(self,instance_id):
        data={}
        response = Compute.rest.doGet(self.url+"/servers/"+instance_id,data,self.headers)
        print response["server"]["status"]
        return response["server"]["status"]


    def encode_to_base64(self,file_path):
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return encoded_string

