import openstack_rest.api
import pytest
from nose.tools import with_setup
from openstack_rest.api import OpenstackRESTConnection
from openstack_rest.api import InvalidRequestException
from credentials import USER, PASSWORD, KEYSTONE_URL, EXPECTED_NOVA_SERVER_URL, EXPECTED_NOVA_DIRS_URL

class TestOpenstackRESTConnection(object):
    def setup(self):
        self.connection = OpenstackRESTConnection(
                USER, PASSWORD, KEYSTONE_URL)
        self.connection.authenticate()

    def teardown(self):
        print "tear-down"

    @with_setup(setup, teardown)
    def test_init(self):
        assert self.connection != None
        assert self.connection.username == USER
        assert self.connection.password == PASSWORD
        assert self.connection.keystone_url == KEYSTONE_URL
    
    # Authenticate with correct credentials
    def testAuthenticate(self):
        assert self.connection.authenticate()
        assert self.connection.token != ''
        assert self.connection.nova_server_url == EXPECTED_NOVA_SERVER_URL
        assert self.connection.nova_dirs_url == EXPECTED_NOVA_DIRS_URL

    # Authenticate with incorrect credentials
    def testAuthenticateWithInvalidCredentials(self):
        connection = openstack_rest.api.OpenstackRESTConnection(
                'invalid_username', 'invalid_password', KEYSTONE_URL)
        assert connection != None
        with pytest.raises(InvalidRequestException):
            connection.authenticate()

    def testGetImages(self):
        images = self.connection.get_images() 
        assert images != None
        assert len(images) > 0

    def testGetInstances(self):
        instances = self.connection.get_instances()
        assert instances != None
        assert len(instances) >= 0

    def testGetInstanceDetails(self):
        #relies on there being current instances running
        instance_id = self.connection.get_instances()[0]['id']
        details = self.connection.get_instance_details(instance_id)
        assert details != None

    def testGetInstanceMetadata(self):
        #relies on there being current instances running
        instance_id = self.connection.get_instances()[0]['id']
        metadata = self.connection.get_instance_metadata(instance_id)
        assert metadata != None

    def testSetAndGetInstanceMetadata(self):
        #relies on there being current instances running
        #WARNING: This will modify your running instances
        instance_id = self.connection.get_instances()[0]['id']
        metadata = {'unit_test_key': 'unit_test_value'}
        self.connection.set_instance_metadata(instance_id, metadata)
        metadata_retrieved = self.connection.get_instance_metadata(instance_id)
        assert metadata_retrieved['unit_test_key'] == 'unit_test_value'


