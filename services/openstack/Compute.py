import base64

from services.common.RestTemplate import RestTemplate


class Compute:

    rest = RestTemplate()

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
            else:
                return False

    def create_instance(self,image_id,flavor_id,user_data):
        data= {
            "server": {"name": "PATinstance1", "imageRef": image_id, "flavorRef": flavor_id,
                       "max_count": 1, "min_count": 1,"key_name":"PATKeyPair","user_data":user_data}
            }

        response = Compute.rest.doPost(self.url+"/servers",data,self.headers)
        print(response)
        return response["server"]["id"]


    def terminate_instance(self,instance_id):
        data={}
        response = Compute.rest.doDelete(self.url+"/servers/"+instance_id,data,self.headers)
        print(response)

    def get_instance_creation_status(self,instance_id):
        data={}
        response = Compute.rest.doGet(self.url+"/servers/"+instance_id,data,self.headers)
        print response


    def encode_to_base64(self,file_path):
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return encoded_string

