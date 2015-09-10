from services.common.RestTemplate import RestTemplate


class Glance:

    rest = RestTemplate()
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
                return status
            else:
                status = False

        return status

    def upload_img(self):
        data = {"name": "testImg","container_format": "bare","disk_format": "qcow2","min_disk": 0,"min_ram": 0}
        response = Glance.rest.doPost(self.url+"/v2/images",data,self.headers)
        print(response["file"])
        print("upload_img")