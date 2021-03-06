__author__ = '311855'

import os
from services.common.RestTemplate import RestTemplate
from services.common.CONST import CONST


class Neutron:

    rest = RestTemplate()
    const = CONST()

    def __init__(self,endpoint,auth_token):
        self.url=endpoint
        self.auth_token=auth_token
        self.headers= {'Content-type': 'application/json','Accept':'application/json','X-Auth-Token':self.auth_token}
        self.data={}

    def getFloatingIps(self):
        data={}
        print(self.url+"/v2.0/floatingips")
        response = Neutron.rest.doGet(self.url+"/v2.0/floatingips",data,self.headers)
        floatingips = response["floatingips"]
        status = True
        for floatingip in floatingips:
            if self.const.DOWN == floatingip["status"]:
                return floatingip["floating_ip_address"]
            else:
                return False
        print response


