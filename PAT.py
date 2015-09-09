import sys
from optparse import OptionParser
from services.openstack.Glance import Glance

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

    # Using Key Stone Service retrieve Auth Token and End Point Details
    identity = KeyStone(opts.user,opts.password,opts.tenant)
    auth_token=identity.get_auth_token()
    glance_endpoint = identity.get_end_point(const.GLANCE)
    heat_endpoint = identity.get_end_point(const.HEAT)
    nova_endpoint = identity.get_end_point(const.NOVA)


    # Using Glance Service Check and Upload Image

    image_service=Glance(glance_endpoint,auth_token)
    if image_service.is_img_available(opts.image):
        print "Image available"
    else:
        print "Image not available"
        image_service.upload_img()



if __name__ == '__main__':
    main()