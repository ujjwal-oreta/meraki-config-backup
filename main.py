import configuration 
from utils import blob_storage


def main():
    # Fetch complete list of organization IDs
    organization_ids = configuration.get_all_organization_ids()
    print("Getting all Configurations")
    config = configuration.get_all_configurations(organization_ids, is_cloud=True)
    configuration.store_all_configurations(config, organization_ids, is_cloud=True)
    return 200


if __name__ == "__main__":
    main()