
class CONST:

    def __init__(self):
        #openstack services
        self.NOVA = "nova"
        self.GLANCE = "glance"
        self.HEAT = "heat"
        self.KEYSTONE = "keystone"
        self.NEUTRON = "neutron"

        #status
        self.ACTIVE = "ACTIVE"
        self.DOWN = "DOWN"
        self.ENV_SETUP_COMPLETE="COMPLETED PAT ENVIRONMENT SETUP"

        #paths
        self.USER_DATA_FILE = "resources/user_data.file"
        self.PRIVATE_KEY = "resources/patkeypair.pem"