import os
from dashboard import Dashboard
from network import Network
from utils import os_utils, blob_storage, decorator

API_KEY = os.environ['API_KEY']

class Organization:
    def __init__(self, organization_id=None):
        dashboard = Dashboard(API_KEY)
        self.organization = dashboard.dashboard.organizations
        self.organization_id = organization_id
        self.organization_dir_name = None
        self.organization_networks = None
        self.organization_devices = None
        self.network_clients = None
        self.organization_devices_serial_list = []
        self.organization_network_ids = []
    
    def getOrganization(self):
        return self.organization.getOrganization(organizationId = self.organization_id)

    def getOrganizationName(self):
        try:
            return self.organization.getOrganization(organizationId=self.organization_id)['name']
        except Exception as e:
            return str(self.organization_id)
    
    def getAllOrganizations(self):
        return self.organization.getOrganizations()

    def getOrganizationDirName(self, base_dir_name):
        org_name = self.getOrganizationName()
        self.organization_dir_name = base_dir_name + '/' + org_name + '/Organization'
        return self.organization_dir_name, base_dir_name + '/' + org_name
    
    def createOrganizationDir(self, base_dir_name, is_cloud):
        self.organization_dir_name, base_dir_name = self.getOrganizationDirName(base_dir_name)
        if not is_cloud:
            os_utils.makedirs(self.organization_dir_name)
        else:
            blob_client = blob_storage.get_blob_client()
            # blob_storage.create_container(blob_client, self.organization_dir_name)
        return self.organization_dir_name, base_dir_name 
    
    @decorator.exception_decorator
    def getOrganizationActionBatches(self):
        return self.organization.getOrganizationActionBatches(organizationId=self.organization_id)

    @decorator.exception_decorator
    def getOrganizationAdaptivePolicyAcls(self):
        return self.organization.getOrganizationAdaptivePolicyAcls(organizationId=self.organization_id)
    
    @decorator.exception_decorator
    def getOrganizationAdaptivePolicyGroups(self):
        return self.organization.getOrganizationAdaptivePolicyGroups(organizationId=self.organization_id)
    
    @decorator.exception_decorator
    def getOrganizationAdmins(self):
        self.organization.getOrganizationAdmins(organizationId=self.organization_id)
    
    @decorator.exception_decorator
    def getOrganizationAlertsProfiles(self):
        return self.organization.getOrganizationAlertsProfiles(organizationId=self.organization_id)
    
    @decorator.exception_decorator
    def getOrganizationNetworks(self):
        self.organization_networks = self.organization.getOrganizationNetworks(organizationId=self.organization_id)
        self.organization_network_ids = [network['id'] for network in self.organization_networks]
        return self.organization_networks
 
    
    @decorator.exception_decorator
    def getOrganizationBrandingPolicies(self):
        config = {}
        config = self.organization.getOrganizationBrandingPolicies(organizationId=self.organization_id)
        return config
    
    @decorator.exception_decorator
    def getOrganizationBrandingPoliciesPriorities(self):
        return self.organization.getOrganizationBrandingPoliciesPriorities(organizationId=self.organization_id)
        
    
    @decorator.exception_decorator
    def getOrganizationDevices(self):
        self.organization_devices = self.organization.getOrganizationDevices(organizationId=self.organization_id)
        self.organization_devices_serial_list = [x['serial'] for x in self.organization_devices]
        return self.organization_devices

    @decorator.exception_decorator
    def getOrganizationClients(self):
        config = {}
        if not self.organization_networks:
            self.organization_networks = self.getOrganizationNetworks()
        config['policy'] = self.getOrganizationNetworkClientPolicy()
        config['search'] = self.getOrganizationClientsSearch()
        config['splashAuthorizationStatus'] = self.getNetworkClientSplashAuthorizationStatus()
        return config


    @decorator.exception_decorator
    def getOrganizationNetworkClientPolicy(self):
        config = {}
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            config[network_id] = network.getNetworkPoliciesByClient()
        return config

    @decorator.exception_decorator
    def getOrganizationClientsByNetwork(self):
        self.network_clients = {}
        if not self.organization_networks:
            self.organization_networks = self.getOrganizationNetworks()
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            self.network_clients[network_id] = network.getNetworkClients()
        return self.network_clients

    @decorator.exception_decorator
    def fetchMacAddressFromNetworkClients(self):
        mac_address = []
        for key in self.network_clients:
            network_mac_list = [x['mac'] for x in self.network_clients[key]]
            mac_address.extend(network_mac_list)
        return mac_address

    @decorator.exception_decorator
    def getOrganizationClientsSearch(self):
        config = {}
        if not self.network_clients:
            self.network_clients = self.getOrganizationClientsByNetwork()
        self.organization_clients_mac = self.fetchMacAddressFromNetworkClients()
        for mac_id in self.organization_clients_mac:
            config[mac_id] = self.organization.getOrganizationClientsSearch(organizationId=self.organization_id, mac=mac_id)
        return config
    

    @decorator.exception_decorator
    def getNetworkClientSplashAuthorizationStatus(self):
        config = {}
        if not self.network_clients:
            self.network_clients = self.getOrganizationClientsByNetwork()
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            config[network_id] = network.getNetworkClientSplashAuthorizationStatus(self.network_clients[network_id])
        return config
    
    @decorator.exception_decorator
    def getOrganizationConfigTemplates(self):
        return self.organization.getOrganizationConfigTemplates(organizationId=self.organization_id)
    

    @decorator.exception_decorator
    def getOrganizationEarlyAccessFeatures(self):
        return self.organization.getOrganizationEarlyAccessFeatures(organizationId=self.organization_id)


    @decorator.exception_decorator
    def getOrganizationEarlyAccessFeaturesOptIns(self):
        return self.organization.getOrganizationEarlyAccessFeaturesOptIns(organizationId=self.organization_id)

    @decorator.exception_decorator
    def getOrganizationFirmware(self):
        config = {}
        config['upgrades'] = self.getFirmwareUpgrades()
        config['byDevice'] = self.getOrganizationFirmwareUpgradesByDevice()
    
    @decorator.exception_decorator
    def getFirmwareUpgrades(self):
        return self.organization.getOrganizationFirmwareUpgrades(organizationId=self.organization_id)
    

    @decorator.exception_decorator
    def getOrganizationFirmwareUpgradesByDevice(self):
        return self.organization.getOrganizationFirmwareUpgradesByDevice(organizationId=self.organization_id)


    @decorator.exception_decorator
    def getOrganizationFirmwareUpgrades(self):
        if not self.organization_networks:
            self.organization_networks = self.getOrganizationNetworks()
        config = self.getNetworkFirmwareUpgrades()
        config['staged'] = self.getStagedNetworkUpgrades()
        

    @decorator.exception_decorator
    def getNetworkFirmwareUpgrades(self):
        config = {}
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            config[network_id] = network.getNetworkFirmwareUpgrades()
        return config
    

    @decorator.exception_decorator
    def getStagedNetworkUpgrades(self):
        config = {}
        config['events'] = self.getFirmwareStagedEvents()
        config['groups'] = self.getNetworkFirmwareUpgradesStagedGroups()
        config['stages'] = self.getNetworkFirmwareUpgradesStagedStages()
        return config


    @decorator.exception_decorator
    def getFirmwareStagedEvents(self):
        config = {}
        if not self.organization_networks:
            self.organization_networks = self.getOrganizationNetworks()
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            config[network_id] = network.getNetworkFirmwareUpgradesStagedEvents()
        return config


    @decorator.exception_decorator
    def getNetworkFirmwareUpgradesStagedGroups(self):
        config = {}
        if not self.organization_networks:
            self.organization_networks = self.getOrganizationNetworks()
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            config[network_id] = network.getNetworkFirmwareUpgradesStagedGroups()
        return config
    

    @decorator.exception_decorator
    def getNetworkFirmwareUpgradesStagedStages(self):
        config = {}
        if not self.organization_networks:
            self.organization_networks = self.getOrganizationNetworks()
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            config[network_id] = network.getNetworkFirmwareUpgradesStagedStages()
        return config


    @decorator.exception_decorator
    def getOrganizationFloorPlans(self):
        config = {}
        if not self.organization_networks:
            self.organization_networks = self.getOrganizationNetworks()
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            config[network_id] = network.getNetworkFloorPlans()
        return config
    
    @decorator.exception_decorator
    def getOrganizationGroupPolicies(self):
        config = {}
        if not self.organization_networks:
            self.organization_networks = self.getOrganizationNetworks()
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            config[network_id] = network.getNetworkGroupPolicies()
        return config

    @decorator.exception_decorator
    def getOrganizationLicenses(self):
        try:
            return self.organization.getOrganizationLicenses(organizationId=self.organization_id)
        except Exception as e:
            if e.status == 400:
                return e.message['errors']
            else:
                raise(e)

    @decorator.exception_decorator
    def getOrganizationLoginSecurity(self):
        return self.organization.getOrganizationLoginSecurity(organizationId=self.organization_id)

    @decorator.exception_decorator
    def getOrganizationPolicyObjects(self):
        return self.organization.getOrganizationPolicyObjects(organizationId=self.organization_id)

    @decorator.exception_decorator
    def getOrganizationPolicyObjectsGroups(self):
        return self.organization.getOrganizationPolicyObjectsGroups(organizationId=self.organization_id)

    @decorator.exception_decorator
    def getOrganizationSaml(self):
        return self.organization.getOrganizationSaml(organizationId=self.organization_id)

    @decorator.exception_decorator
    def getOrganizationSamlIdps(self):
        return self.organization.getOrganizationSamlIdps(organizationId=self.organization_id)

    @decorator.exception_decorator
    def getOrganizationSamlRoles(self):
        return self.organization.getOrganizationSamlRoles(organizationId=self.organization_id)


    @decorator.exception_decorator
    def getOrganizationSnmp(self):
        return self.organization.getOrganizationSnmp(organizationId=self.organization_id)


    @decorator.exception_decorator
    def getOrganizationInventoryDevices(self):
        return self.organization.getOrganizationInventoryDevices(organizationId=self.organization_id)
