import os
import json

from organization import Organization
from network import Network
from device import Device
from utils import os_utils, common_utils, blob_storage


def get_all_configurations(organization_ids, is_cloud):
    all_config = {}
    base_dir_name = get_config_dir_name(cloud=is_cloud)
    for organization_id in organization_ids:
        print("Organzation_id: ", organization_id)
        organization = Organization(organization_id)
        organization_dir, org_dir_name = organization.createOrganizationDir(base_dir_name, is_cloud=is_cloud)
        org_config, network_config, device_config = get_all_configs_for_organization(organization, org_dir_name, is_cloud)
        all_config[organization_id] = {}
        all_config[organization_id]['org_config'] = org_config
        all_config[organization_id]['network_config'] = network_config
        all_config[organization_id]['device_config'] = device_config
        all_config[organization_id]['organization_dir'] = organization_dir
    return all_config


def get_all_configs_for_organization(organization, org_dir_name, is_cloud):
    print("Getting Organzation Config")
    org_config = get_configurations_for_organization(organization)
    print("Getting Network Config")
    network_config = get_configurations_for_networks(organization, org_dir_name, is_cloud)
    print(network_config)
    print("Getting Device Config")
    device_config = get_configurations_for_devices(organization, org_dir_name, is_cloud)
    return org_config, network_config, device_config


def get_configurations_for_organization(organization):
    org_config = {}
    org_config['action_batches'] = organization.getOrganizationActionBatches()
    org_config['adaptive_policy_acls'] = organization.getOrganizationAdaptivePolicyAcls()
    org_config['adaptive_policy_groups'] = organization.getOrganizationAdaptivePolicyGroups()
    org_config['admins'] = organization.getOrganizationAdmins()
    org_config['alerts_profiles'] = organization.getOrganizationAlertsProfiles()
    org_config['branding_policies'] = organization.getOrganizationBrandingPolicies()
    org_config['branding_policies_priorities'] = organization.getOrganizationBrandingPoliciesPriorities()
    org_config['configTemplates'] = organization.getOrganizationConfigTemplates()
    org_config['devices'] = organization.getOrganizationDevices()
    org_config['early_access_features'] = organization.getOrganizationEarlyAccessFeatures()
    org_config['early_access_features_opt_ins'] = organization.getOrganizationEarlyAccessFeaturesOptIns()
    org_config['firmware_upgrades'] = organization.getFirmwareUpgrades()
    org_config['firmware_upgrades_by_device'] = organization.getOrganizationFirmwareUpgradesByDevice()
    org_config['inventory'] = organization.getOrganizationInventoryDevices()
    org_config['licenses'] = organization.getOrganizationLicenses()
    org_config['login_security'] = organization.getOrganizationLoginSecurity()
    org_config['networks'] = organization.getOrganizationNetworks()
    org_config['policy_objects'] = organization.getOrganizationPolicyObjects()
    org_config['policy_objects_groups'] = organization.getOrganizationPolicyObjectsGroups()
    org_config['saml'] = organization.getOrganizationSaml()
    org_config['saml_idps'] = organization.getOrganizationSamlIdps()
    org_config['saml_roles'] = organization.getOrganizationSamlRoles()
    org_config['snmp'] = organization.getOrganizationSnmp()
    return org_config


def get_configurations_for_networks(organization, base_dir_name, is_cloud):
    network_config = {}
    organization.getOrganizationNetworks()
    print(organization.organization_network_ids)
    for network_id in organization.organization_network_ids:
        network = Network(network_id)
        network_dir = network.createNetworkDir(base_dir_name + '/Networks', is_cloud)
        network_config[network_id] = get_configurations_for_network(network)
        network_config[network_id]['network_dir'] = network_dir
    return network_config


def get_configurations_for_network(network):
    network_config = {}
    network_config['network_alert_settings'] = network.getNetworkAlertsSettings()
    network_config['network_policies_by_client'] = network.getNetworkPoliciesByClient()
    network_config['network_firmware_upgrades'] = network.getNetworkFirmwareUpgrades()
    network_config['network_firmware_upgrades_staged_events'] = network.getNetworkFirmwareUpgradesStagedEvents()
    network_config['network_firmware_upgrades_staged_groups'] = network.getNetworkFirmwareUpgradesStagedGroups()
    network_config['network_firmware_upgrades_staged_stages'] = network.getNetworkFirmwareUpgradesStagedStages()
    network_config['network_floor_plans'] = network.getNetworkFloorPlans()
    network_config['network_group_policies'] = network.getNetworkGroupPolicies()
    network_config['network_health_alerts'] = network.getNetworkHealthAlerts()
    network_config['meraki_auth_users'] = network.getNetworkMerakiAuthUsers()
    network_config['network_mqtt_brokers'] = network.getNetworkMqttBrokers()
    network_config['network_netflow'] = network.getNetworkNetflow()
    # network_config['network_pii_pii_keys'] = network.getNetworkPiiPiiKeys()
    network_config['network_pii_requests'] = network.getNetworkPiiRequests()
    # network_config['network_pii_sm_devices_for_key'] = network.getNetworkPiiSmDevicesForKey()
    # network_config['network_pii_sm_owners_for_key'] = network.getNetworkPiiSmOwnersForKey()
    network_config['network_policies_by_client'] = network.getNetworkPoliciesByClient()
    network_config['settings'] = network.getNetworkSettings()
    network_config['snmp'] = network.getNetworkSnmp()
    network_config['syslog_servers'] = network.getNetworkSyslogServers()
    network_config['traffic_analysis'] = network.getNetworkTrafficAnalysis()
    network_config['traffic_shaping_application_categories'] = network.getNetworkTrafficShapingApplicationCategories()
    network_config['traffic_shaping_dscp_tagging_options'] = network.getNetworkTrafficShapingDscpTaggingOptions()
    network_config['network_webhooks_http_servers'] = network.getNetworkWebhooksHttpServers()
    network_config['network_webhooks_payload_templates'] = network.getNetworkWebhooksPayloadTemplates()
    return network_config


def get_configurations_for_devices(organization, base_dir_name, is_cloud):
    device_config = {}
    organization.getOrganizationDevices()
    for serial in organization.organization_devices_serial_list:
        device = Device(serial)
        device_dir = device.createDeviceDir(base_dir_name + '/Devices', is_cloud)
        device_config[serial] = get_configurations_for_device(device)
        device_config[serial]['device_dir'] = device_dir
    return device_config


def get_configurations_for_device(device):
    device_config = {}
    device_config['device_cellular_sims'] = device.getDeviceCellularSims()
    device_config['management_interface'] = device.getDeviceManagementInterface()
    return device_config


def get_config_dir_name(output_directory = 'config_output', cloud = True):
    now = common_utils.get_now(str_format=True)
    if not cloud:
        cwd = os.getcwd()
        path = os_utils.join_path_name(cwd, output_directory)
        path = os_utils.join_path_name(path, now)
        return path
    else:
        return now


def store_organization_configuration(org_config, organization_dir, is_cloud):
    store_configuration(org_config, organization_dir, is_cloud)


def store_network_configuration(network_config, is_cloud):
    for key in network_config:
        config = network_config[key]
        network_dir_name = config['network_dir']
        # del config['network_dir']
        store_configuration(config, network_dir_name, is_cloud)


def store_device_configuration(device_config, is_cloud):
    for key in device_config:
        config = device_config[key]
        device_dir_name = config['device_dir']
        # del config['device_dir']
        store_configuration(config, device_dir_name, is_cloud)


def store_configuration(org_config, organization_dir, is_cloud):
    for key in org_config:
        file_name = key + '.json'
        path = organization_dir + '/' + file_name
        print("Path: ", path)
        if not is_cloud:
            common_utils.write_file(path, org_config[key])
        else:
            blob_storage.dump_data(path, org_config[key])


def store_all_configurations(config, organization_ids, is_cloud):
    for organization_id in organization_ids:
        organization_config = config[organization_id]
        org_config, network_config, device_config = organization_config['org_config'], organization_config['network_config'], organization_config['device_config']
        organization_dir = organization_config['organization_dir']
        store_organization_configuration(org_config, organization_dir, is_cloud)
        store_network_configuration(network_config, is_cloud)
        store_device_configuration(device_config, is_cloud)
