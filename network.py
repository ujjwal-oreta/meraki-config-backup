import os
from dashboard import Dashboard
from utils import os_utils, blob_storage

API_KEY = os.environ['API_KEY']

class Network():
    def __init__(self, network_id):
        dashboard = Dashboard(API_KEY)
        self.network = dashboard.dashboard.networks
        self.network_id = network_id
        self.network_dir_name = None

    def getNetworkDirName(self, base_dir_name):
        self.network_dir_name = base_dir_name + '/' + self.network_id
        return self.network_dir_name
    
    def createNetworkDir(self, base_dir_name, is_cloud):
        self.network_dir_name = self.getNetworkDirName(base_dir_name)
        if not is_cloud:
            os_utils.makedirs(self.network_dir_name)
        else:
            blob_client = blob_storage.get_blob_client()
            # blob_storage.create_container(blob_client, self.network_dir_name)
        return self.network_dir_name
    
    def getNetworkAlertsSettings(self):
        print(self.network_id)
        return self.network.getNetworkAlertsSettings(networkId=self.network_id)

    def getNetworkPoliciesByClient(self):
        return self.network.getNetworkPoliciesByClient(networkId=self.network_id)
    
    def getNetworkClients(self):
        return self.network.getNetworkClients(networkId=self.network_id)
    
    def getNetworkClientSplashAuthorizationStatus(self, network_client_map):
        config = {}
        client_ids = [x['id'] for x in network_client_map]
        for client_id in client_ids:
            config[client_id] = self.network.getNetworkClientSplashAuthorizationStatus(networkId = self.network_id, clientId = client_id)
        return config

    def getNetworkFirmwareUpgrades(self):
        return self.network.getNetworkFirmwareUpgrades(networkId=self.network_id)

    def getNetworkFirmwareUpgradesStagedEvents(self):
        try:
            return self.network.getNetworkFirmwareUpgradesStagedEvents(networkId=self.network_id)
        except Exception as e:
            if e.status == 400:
                return "This endpoint only supports MS network"
            else:
                raise(e)
    
    def getNetworkFirmwareUpgradesStagedGroups(self):
        try:
            return self.network.getNetworkFirmwareUpgradesStagedGroups(networkId=self.network_id)
        except Exception as e:
            if e.status == 400:
                return "This endpoint only supports MS network"
            else:
                raise(e)
        
    def getNetworkFirmwareUpgradesStagedStages(self):
        try:
            return self.network.getNetworkFirmwareUpgradesStagedStages(networkId=self.network_id)
        except Exception as e:
            if e.status == 400:
                return "This endpoint only supports MS network"
            else:
                raise(e)
    
    def getNetworkGroupPolicies(self):
        return self.network.getNetworkGroupPolicies(networkId=self.network_id)
    
    def getNetworkFloorPlans(self):
        return self.network.getNetworkFloorPlans(networkId=self.network_id)

    def getNetworkHealthAlerts(self):
        return self.network.getNetworkHealthAlerts(networkId=self.network_id)

    def getNetworkMerakiAuthUsers(self):
        return self.network.getNetworkMerakiAuthUsers(networkId=self.network_id)

    def getNetworkMqttBrokers(self):
        try:
            return self.network.getNetworkMqttBrokers(networkId=self.network_id)
        except Exception as e:
            if e.status == 400:
                return e.message['errors']
            else:
                raise(e)

    def getNetworkNetflow(self):
        return self.network.getNetworkNetflow(networkId=self.network_id)

    def getNetworkPiiPiiKeys(self):
        return self.network.getNetworkPiiPiiKeys(networkId=self.network_id)

    def getNetworkPiiRequests(self):
        return self.network.getNetworkPiiRequests(networkId=self.network_id)

    def getNetworkPiiSmDevicesForKey(self):
        return self.network.getNetworkPiiSmDevicesForKey(networkId=self.network_id)

    def getNetworkPiiSmOwnersForKey(self):
        return self.network.getNetworkPiiSmOwnersForKey(networkId=self.network_id)

    def getNetworkPoliciesByClient(self):
        return self.network.getNetworkPoliciesByClient(networkId=self.network_id)

    def getNetworkSettings(self):
        return self.network.getNetworkSettings(networkId=self.network_id)
    
    def getNetworkSnmp(self):
        return self.network.getNetworkSnmp(networkId=self.network_id)
    
    def getNetworkSyslogServers(self):
        return self.network.getNetworkSyslogServers(networkId=self.network_id)
    
    def getNetworkTrafficAnalysis(self):
        return self.network.getNetworkTrafficAnalysis(networkId=self.network_id)

    def getNetworkTrafficShapingApplicationCategories(self):
        return self.network.getNetworkTrafficShapingApplicationCategories(networkId=self.network_id)
    
    def getNetworkTrafficShapingDscpTaggingOptions(self):
        return self.network.getNetworkTrafficShapingDscpTaggingOptions(networkId=self.network_id)

    def getNetworkWebhooksHttpServers(self):
        return self.network.getNetworkWebhooksHttpServers(networkId=self.network_id)

    def getNetworkWebhooksPayloadTemplates(self):
        return self.network.getNetworkWebhooksPayloadTemplates(networkId=self.network_id)
