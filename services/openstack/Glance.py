

class Glance:

    def __init__(self,endpoint,auth_token):
        self.url=endpoint
        self.auth_token=auth_token


    def is_img_available(self):
        print(self.url)
        print(self.auth_token)

    def upload_img(self):
        print("upload_img")