from services.common.RestTemplate import RestTemplate


class Glance:

    rest = RestTemplate()
    def __init__(self,endpoint,auth_token):
        self.url=endpoint
        self.auth_token=auth_token


    def is_img_available(self,image_name):
        headers = {'Content-type': 'application/json','Accept':'application/json','X-Auth-Token':self.auth_token}
        data={}
        response = Glance.rest.doGet(self.url+"/v2/images",data,headers)
        images = response["images"]
        status = True
        for image in images:
            if image_name == image["name"]:
                status = True
                return status
            else:
                status = False

        return status

    def upload_img(self):
        print("upload_img")