import os
from dashboard import Dashboard
from utils import os_utils, blob_storage, decorator

API_KEY = '3e3110d2adff78d875beefb6a6e7d631db296004'

class Device():
    def __init__(self, serial=None):
        dashboard = Dashboard(API_KEY)
        self.devices = dashboard.dashboard.devices
        self.serial = serial
    
    def getDeviceDirName(self, base_dir_name):
        self.device_dir_name = base_dir_name + '/' + self.serial
        return self.device_dir_name
    
    def createDeviceDir(self, base_dir_name, is_cloud):
        self.device_dir_name = self.getDeviceDirName(base_dir_name)
        if not is_cloud:
            os_utils.makedirs(self.device_dir_name)
        else:
            blob_client = blob_storage.get_blob_client()
            # blob_storage.create_container(blob_client, self.device_dir_name)
        return self.device_dir_name
    
    def getDeviceCellularSims(self):
        try:
            return self.devices.getDeviceCellularSims(serial=self.serial)
        except Exception as e:
            if e.status == 400:
                print("This device - {} does not support SIM configurations".format(self.serial))
                return "This device - {} does not support SIM configurations".format(self.serial)
            else:
                raise(e)
    
    @decorator.exception_decorator
    def getDeviceManagementInterface(self):
        return self.devices.getDeviceManagementInterface(serial=self.serial)
        