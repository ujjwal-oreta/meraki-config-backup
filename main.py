import configuration 
from utils import blob_storage


def main():
    organization_ids = [601793500207384061, 863973]
    print("Getting all Configurations")
    config = configuration.get_all_configurations(organization_ids, is_cloud=True)
    configuration.store_all_configurations(config, organization_ids, is_cloud=True)
    # blob_storage.dump_data('temp-location', {'Data': 'Temp Data'})
    return 200


if __name__ == "__main__":
    main()