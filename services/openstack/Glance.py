import os
from services.common.RestTemplate import RestTemplate


class Glance:

    rest = RestTemplate()
    img_id=""
    def __init__(self,endpoint,auth_token):
        self.url=endpoint
        self.auth_token=auth_token
        self.headers= {'Content-type': 'application/json','Accept':'application/json','X-Auth-Token':self.auth_token}
        self.data={}

    def is_img_available(self,image):
        imageFormat=image.split(".")[-1:][0]
        imageName = image.replace("."+imageFormat, "")
        print(imageName)
        response = Glance.rest.doGet(self.url+"/v2/images",self.data,self.headers)

        images = response["images"]
        status = True
        for image in images:
            if imageName == image["name"]:
                status = True
                Glance.img_id=image["id"]
                return status
            else:
                status = False

        return status

    def upload_img(self):
        #create Image
        data = {"name": "testImg","container_format": "bare","disk_format": "qcow2","min_disk": 0,"min_ram": 0}
        response = Glance.rest.doPost(self.url+"/v2/images",data,self.headers)
        image_file=response["file"]

        #upload Image Data
        headers= {'Content-type': 'application/octet-stream','X-Auth-Token':self.auth_token}
        BASE_DIR = os.path.dirname(os.path.dirname(__file__)).replace("services","")
        IMAGE_DATA=BASE_DIR+"resources"+os.path.sep+"images"+os.path.sep+"cirros-0.3.4-x86_64-disk.img"
        print(self.auth_token)
        print(self.url+image_file)
        print(IMAGE_DATA)
        response=Glance.rest.doPut(self.url+image_file,IMAGE_DATA,headers)
        print("upload_img")