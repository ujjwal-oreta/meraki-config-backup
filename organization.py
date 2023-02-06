import os
from dashboard import Dashboard
from network import Network
from utils import os_utils, blob_storage

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
        self.organization_devices_serial_list = None
    
    def getOrganization(self):
        return self.organization.getOrganization(organizationId = self.organization_id)

    def getOrganizationName(self):
        return self.organization.getOrganization(organizationId=self.organization_id)['name']
    
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
    
    def getOrganizationActionBatches(self):
        return self.organization.getOrganizationActionBatches(organizationId=self.organization_id)

    def getOrganizationAdaptivePolicyAcls(self):
        return self.organization.getOrganizationAdaptivePolicyAcls(organizationId=self.organization_id)
    
    def getOrganizationAdaptivePolicyGroups(self):
        return self.organization.getOrganizationAdaptivePolicyGroups(organizationId=self.organization_id)
    
    def getOrganizationAdmins(self):
        self.organization.getOrganizationAdmins(organizationId=self.organization_id)
    
    def getOrganizationAlertsProfiles(self):
        return self.organization.getOrganizationAlertsProfiles(organizationId=self.organization_id)
    
    def getOrganizationNetworks(self):
        self.organization_networks = self.organization.getOrganizationNetworks(organizationId=self.organization_id)
        self.organization_network_ids = [network['id'] for network in self.organization_networks]
        return self.organization_networks
    
    def getOrganizationBrandingPolicies(self):
        config = {}
        try:
            config = self.organization.getOrganizationBrandingPolicies(organizationId=self.organization_id)
        except Exception as e:
            if e.status == 400:
                print('This organization {} does not support Dashboard branding'.format(self.organization_id))
                return 'This organization {} does not support Dashboard branding'.format(self.organization_id)
            else:
                raise(e)
        return config
    
    def getOrganizationBrandingPoliciesPriorities(self):
        try:
            return self.organization.getOrganizationBrandingPoliciesPriorities(organizationId=self.organization_id)
        except Exception as e:
            if e.status == 400:
                print('This organization {} does not support Dashboard branding'.format(self.organization_id))
                return 'This organization {} does not support Dashboard branding'.format(self.organization_id)
            else:
                raise(e)
        
    
    def getOrganizationDevices(self):
        self.organization_devices = self.organization.getOrganizationDevices(organizationId=self.organization_id)
        self.organization_devices_serial_list = [x['serial'] for x in self.organization_devices]
        return self.organization_devices


    def getOrganizationClients(self):
        config = {}
        if not self.organization_networks:
            self.organization_networks = self.getOrganizationNetworks()
        config['policy'] = self.getOrganizationNetworkClientPolicy()
        config['search'] = self.getOrganizationClientsSearch()
        config['splashAuthorizationStatus'] = self.getNetworkClientSplashAuthorizationStatus()
        return config


    def getOrganizationNetworkClientPolicy(self):
        config = {}
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            config[network_id] = network.getNetworkPoliciesByClient()
        return config

    def getOrganizationClientsByNetwork(self):
        self.network_clients = {}
        if not self.organization_networks:
            self.organization_networks = self.getOrganizationNetworks()
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            self.network_clients[network_id] = network.getNetworkClients()
        return self.network_clients


    def fetchMacAddressFromNetworkClients(self):
        mac_address = []
        for key in self.network_clients:
            network_mac_list = [x['mac'] for x in self.network_clients[key]]
            mac_address.extend(network_mac_list)
        return mac_address

    
    def getOrganizationClientsSearch(self):
        config = {}
        if not self.network_clients:
            self.network_clients = self.getOrganizationClientsByNetwork()
        self.organization_clients_mac = self.fetchMacAddressFromNetworkClients()
        for mac_id in self.organization_clients_mac:
            config[mac_id] = self.organization.getOrganizationClientsSearch(organizationId=self.organization_id, mac=mac_id)
        return config
    

    def getNetworkClientSplashAuthorizationStatus(self):
        config = {}
        if not self.network_clients:
            self.network_clients = self.getOrganizationClientsByNetwork()
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            config[network_id] = network.getNetworkClientSplashAuthorizationStatus(self.network_clients[network_id])
        return config
    

    def getOrganizationConfigTemplates(self):
        return self.organization.getOrganizationConfigTemplates(organizationId=self.organization_id)
    

    def getOrganizationEarlyAccessFeatures(self):
        return self.organization.getOrganizationEarlyAccessFeatures(organizationId=self.organization_id)


    def getOrganizationEarlyAccessFeaturesOptIns(self):
        return self.organization.getOrganizationEarlyAccessFeaturesOptIns(organizationId=self.organization_id)

    
    def getOrganizationFirmware(self):
        config = {}
        config['upgrades'] = self.getFirmwareUpgrades()
        config['byDevice'] = self.getOrganizationFirmwareUpgradesByDevice()
    

    def getFirmwareUpgrades(self):
        return self.organization.getOrganizationFirmwareUpgrades(organizationId=self.organization_id)
    

    def getOrganizationFirmwareUpgradesByDevice(self):
        return self.organization.getOrganizationFirmwareUpgradesByDevice(organizationId=self.organization_id)


    def getOrganizationFirmwareUpgrades(self):
        if not self.organization_networks:
            self.organization_networks = self.getOrganizationNetworks()
        config = self.getNetworkFirmwareUpgrades()
        config['staged'] = self.getStagedNetworkUpgrades()
        

    def getNetworkFirmwareUpgrades(self):
        config = {}
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            config[network_id] = network.getNetworkFirmwareUpgrades()
        return config
    

    def getStagedNetworkUpgrades(self):
        config = {}
        config['events'] = self.getFirmwareStagedEvents()
        config['groups'] = self.getNetworkFirmwareUpgradesStagedGroups()
        config['stages'] = self.getNetworkFirmwareUpgradesStagedStages()
        return config

    def getFirmwareStagedEvents(self):
        config = {}
        if not self.organization_networks:
            self.organization_networks = self.getOrganizationNetworks()
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            config[network_id] = network.getNetworkFirmwareUpgradesStagedEvents()
        return config


    def getNetworkFirmwareUpgradesStagedGroups(self):
        config = {}
        if not self.organization_networks:
            self.organization_networks = self.getOrganizationNetworks()
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            config[network_id] = network.getNetworkFirmwareUpgradesStagedGroups()
        return config
    
    def getNetworkFirmwareUpgradesStagedStages(self):
        config = {}
        if not self.organization_networks:
            self.organization_networks = self.getOrganizationNetworks()
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            config[network_id] = network.getNetworkFirmwareUpgradesStagedStages()
        return config

    def getOrganizationFloorPlans(self):
        config = {}
        if not self.organization_networks:
            self.organization_networks = self.getOrganizationNetworks()
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            config[network_id] = network.getNetworkFloorPlans()
        return config
    
    def getOrganizationGroupPolicies(self):
        config = {}
        if not self.organization_networks:
            self.organization_networks = self.getOrganizationNetworks()
        for network_id in self.organization_network_ids:
            network = Network(network_id)
            config[network_id] = network.getNetworkGroupPolicies()
        return config

    
    def getOrganizationLicenses(self):
        try:
            return self.organization.getOrganizationLicenses(organizationId=self.organization_id)
        except Exception as e:
            if e.status == 400:
                return e.message['errors']
            else:
                raise(e)

    def getOrganizationLoginSecurity(self):
        return self.organization.getOrganizationLoginSecurity(organizationId=self.organization_id)

    def getOrganizationPolicyObjects(self):
        return self.organization.getOrganizationPolicyObjects(organizationId=self.organization_id)

    def getOrganizationPolicyObjectsGroups(self):
        return self.organization.getOrganizationPolicyObjectsGroups(organizationId=self.organization_id)

    def getOrganizationSaml(self):
        return self.organization.getOrganizationSaml(organizationId=self.organization_id)

    def getOrganizationSamlIdps(self):
        try:
            return self.organization.getOrganizationSamlIdps(organizationId=self.organization_id)
        except Exception as e:
            if e.status == 400:
                return e.message['error']
            else:
                raise(e)

    def getOrganizationSamlRoles(self):
        return self.organization.getOrganizationSamlRoles(organizationId=self.organization_id)

    def getOrganizationSnmp(self):
        return self.organization.getOrganizationSnmp(organizationId=self.organization_id)

    def getOrganizationInventoryDevices(self):
        return self.organization.getOrganizationInventoryDevices(organizationId=self.organization_id)
