import configuration 
from utils import blob_storage
import getpass


def main():
    organization_ids = [601793500207384061, 863973]
    print("Getting all Configurations")
    user = getpass.getuser()
    print(user)
    # return organization_ids
    # config = configuration.get_all_configurations(organization_ids, is_cloud=True)
    # return config
    # configuration.store_all_configurations(config, organization_ids, is_cloud=True)
    # blob_storage.dump_data('temp-location', {'Data': 'Temp Data'})
    return 200


if __name__ == "__main__":
    main()