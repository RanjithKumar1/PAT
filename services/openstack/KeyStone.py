from config.config import Configuration
from services.common.RestTemplate import RestTemplate

class KeyStone:

    rest = RestTemplate()
    config = Configuration()
    service_catalog = ""

    def __init__(self,username,password,tenantname):
         #Server Details
         self.server_ip = KeyStone.config.SERVER_IP
         self.server_port = KeyStone.config.SERVER_PORT
         self.api_version = KeyStone.config.API_VERSION
         self.url = "http://"+self.server_ip+":"+self.server_port+"/"+self.api_version+"/tokens"

         #User Credentials
         self.tenantName = tenantname
         self.username = username
         self.password = password

    def get_auth_token(self):
        #Retrieve Auth Token
        data = {"auth": {"tenantName": self.tenantName, "passwordCredentials": {"username": self.username, "password": self.password}}}
        response = KeyStone.rest.doPost(self.url,data)
        auth_token = response["access"]["token"]["id"]
        service_catalog = response["access"]["serviceCatalog"]
        KeyStone.service_catalog = service_catalog
        return auth_token


    def get_end_point(self,serviceName):
       for services in KeyStone.service_catalog:
            if(serviceName == services["name"]):
                return services["endpoints"][0]["publicURL"]

