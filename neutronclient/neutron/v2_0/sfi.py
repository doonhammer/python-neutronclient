#  Service Function Insertion Common Line
#
#  Starting with the required imports
#
import argparse
import logging
 
from neutronclient.common import exceptions
from neutronclient.neutron import v2_0 as neutronV20
#from neutronclient.openstack.common.gettextutils import _
 
class ListSFI(neutronV20.ListCommand):
    # Writing a class to list all the data stored by your Sfi
    # extensions. This will call the get_sfis method of your
    # neutron plugin111111
 
    resource = 'sfi'
    # This will be explained later in this post
    log = logging.getLogger(__name__ + '.ListSFI')
    list_columns = [ 'name', 'priority', 'credential' ]
    # list_columns represents the column you wish to display when a
    # user uses "neutron sfi-list". Not all attributes of an
    # extension need be displayed
    pagination_support = True
    # No clue what this does, but other files in the same path use it
    sorting_support = True
    # Enables displaying the information in a sorted manner
 
class ShowSFI(neutronV20.ShowCommand):
    # This class is used to display information of only a specific value
    # for sfi extensions, unlike list which displays all stored
    # information
 
    resource = 'sfi'
    log = logging.getLogger(__name__ + '.ShowSFI')
    # Expected usage is "neutron sfi-show [name]"
    # The name is forwarded as the id for get_sfi method of your
    # neutron plugin
 
class CreateSFI(neutronV20.CreateCommand):
    # This class will forward to the create_sfi method of your
    # neutron plugin. This will go in as a dictionary which your plugin
    # to process.
 
    resource = 'sfi'
    log = logging.getLogger(__name__ + '.CreateSFI')
    def add_known_arguments(self, parser):
        # This method is used to define the arguments that this CLI
        # command expects. Our sfi extensions allows users to
        # specify name, priority and credential. When a user hits
        # "neutron sfi-create --help", information from these are
        # displayed.
 
        parser.add_argument(
            'name', metavar='NAME',
            help=("Name of the sfi"))
 
        parser.add_argument(
            '--priority', dest='priority',
            help=("Assign priority to this sfi"))
 
        parser.add_argument(
            '--credential', dest='credential',
            help=("Specify the credential to this sfi"))
 
        """ This is just an example for retrieving boolean values
        parser.add_argument(
            'admin', action='store_true',
            help=("Is admin is specified, it will store True,"
                   " else False"))
        """
 
    # Sample usage:
    # neutron sfi-create helloworld --priority 1 --credential owner
    # Here, name is helloworld, priority is 1 and credential is owner
 
    # Sample usage for boolean:
    # neutron sfi-create helloworld --priority 1 --credential owner admin
    # Here, the boolean attribute will get it as True. Not specifying admin
    # gives it as False
 
    def args2body(self, parsed_args):
        # This method will create a dictionary of all the specified arguments
        # and forward this data to the next step in neutronclient
        body = {'sfi': {
                    'name': parsed_args.name,
                    'priority': parsed_args.priority,
                    'credential': parsed_args.credential,
                    # for boolean types, it's no different
                    # 'admin': parsed_args.admin,
               }}
        # NOTE: parsed_args gets it's data members called priority and
        # credential from the dest that we specify in add_argument. Not specifying
        # dest will allow you to use the name as it is specified from on the CLI
        # admin attribute has been commented everywhere because sfi extension
        # I used for explanation doesn't contain. It will throw you unrecognized
        # attribute if you use it and send it to the neutron-server.
 
        if parsed_args.tenant_id:
            # this way can be used to check if the attribute has been specified
            # in the CLI. Default values need not be given here if user has
            # not specified the attribute as the "default" key in the extensions
            # dictionary will fill for absent attributes.
            body['sfi'].update({'tenant_id': parsed_args.tenant_id})
 
        return body
 
class DeleteSFI(neutronV20.DeleteCommand):
    # Usage: neutron sfi-delete [name]
    # The name is received as an id in delete_sfi method of your plugin
    log = logging.getLogger(__name__ + '.DeleteSFI')
    resource = 'sfi'
 
class UpdateSFI(neutronV20.UpdateCommand):
    # Usage: neutron sfi-update "name" [--priority | --credential | or both]
    # The name is received as an id in update_sfi method of your plugin
    # The other attributes are transformed into a dictionary and sent to the same
    # method. Sample: neutron sfi-update helloworld --credential group
    # helloworld will be the id, and neutronclient would make a dictionary by itself
    # using the resource as the key.
    # Dictionary = {'sfi': {'credential': 'group'}}
 
    resource = 'sfi'
    log = logging.getLogger(__name__ + '.UpdateSFI')
