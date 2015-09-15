from config.config import Configuration
from services.common.RestTemplate import RestTemplate

class KeyStone:

    tenant_id = ""
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
         self.headers = {'Content-type': 'application/json','Accept':'application/json'}

    def get_auth_token(self):
        #Retrieve Auth Token
        data = {"auth": {"tenantName": self.tenantName, "passwordCredentials": {"username": self.username, "password": self.password}}}
        response = KeyStone.rest.doPost(self.url,data,self.headers)
        auth_token = response["access"]["token"]["id"]
        KeyStone.tenant_id = response["access"]["token"]["tenant"]["id"]
        service_catalog = response["access"]["serviceCatalog"]
        KeyStone.service_catalog = service_catalog
        return auth_token

    def get_tenant_id(self):
        return KeyStone.tenant_id

    def get_end_point(self,serviceName):
       for services in KeyStone.service_catalog:
            if(serviceName == services["name"]):
                return services["endpoints"][0]["publicURL"]

