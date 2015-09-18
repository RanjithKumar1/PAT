import sys
import os
import time

from optparse import OptionParser
from services.openstack.Glance import Glance
from services.openstack.Compute import Compute
from services.openstack.Neutron import Neutron

from services.openstack.KeyStone import KeyStone
from services.common.CONST import CONST


def main():

    parser = OptionParser(usage="""\
        Product Testing Automation.
        Usage: %prog [options]""")

    parser.add_option('-u', '--user',
                      type='string', action='store',metavar='USER ID',
                      help="""User Id of Open Stack. (required)""")
    parser.add_option('-p', '--password',
                      type='string', action='store', metavar='PASSWORD',
                      help="""Password for given user id. (required)""")
    parser.add_option('-t', '--tenant',
                      type='string', action='store',metavar='TENANT ID',
                      help='Tenant id of user. (required)')
    parser.add_option('-i', '--image',
                      type='string', action='store',metavar='TENANT ID',
                      help='Image to be uploaded or avaiable in openstack eg: Ubuntu 14.04 x64 Murano Agent (New).qcow2 (required)')

    opts, args = parser.parse_args()
    const = CONST()

    if not opts.user or not opts.password or not opts.tenant or not opts.image:
        parser.print_help()
        sys.exit(1)

    # ####################################################################
    # Using Key Stone Service retrieve Auth Token and End Point Details
    ######################################################################
    identity = KeyStone(opts.user,opts.password,opts.tenant)
    auth_token=identity.get_auth_token()
    tenant_id=identity.get_tenant_id()
    glance_endpoint = identity.get_end_point(const.GLANCE)
    heat_endpoint = identity.get_end_point(const.HEAT)
    nova_endpoint = identity.get_end_point(const.NOVA)
    neutron_endpoint = identity.get_end_point(const.NEUTRON)

    # ####################################################################
    # Using Glance Service Check and Upload Image
    # ####################################################################

    image_service=Glance(glance_endpoint,auth_token)
    if image_service.is_img_available(opts.image):
        print "Image available"
        image_id=image_service.img_id
    else:
        print "Image not available"
        sys.exit(1)

    # ####################################################################
    # Using Neutron Service to get Floating IP
    # ####################################################################
    neutron=Neutron(neutron_endpoint,auth_token)
    floating_ip=neutron.getFloatingIps()
    if floating_ip:
        print("floating ip available")
    else:
        print("floating ip not available")
    print(floating_ip)


    # ####################################################################
    # Using Compute Service Create Environment
    # ####################################################################
    compute=Compute(nova_endpoint,auth_token,tenant_id)

    #Check and Get Flavour Id
    flavor = compute.get_flavor_id("d0.quarter")
    print flavor

    if flavor:
        print("flavor available")
    else:
        print("flavor not available")

    #Check Quota and Create ENV
    quota_info = compute.get_quota()
    if bool(quota_info):
        print quota_info
    else:
        print "quota still available"
        user_data = compute.encode_to_base64(const.USER_DATA_FILE)
        instance_id = compute.create_instance(image_id,flavor,user_data)

    # ####################################################################
    # Wait for Instance to Create
    # ####################################################################
    status=compute.get_instance_creation_status(instance_id)
    while(status != const.ACTIVE):
        time.sleep(30)
        status=compute.get_instance_creation_status(instance_id)


    # ####################################################################
    # Assign Floating Ip to Instance
    # ####################################################################
    compute.assign_floating_ip_to_instance(instance_id,floating_ip)


    # ####################################################################
    # Execute and Collect Test Results
    # ####################################################################


    # ####################################################################
    # Terminate Instance
    # ####################################################################

    #compute.terminate_instance("554cf19d-a8fa-4186-8107-76e8b6672ea2")


if __name__ == '__main__':
    main()