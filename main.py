import configuration 
from utils import blob_storage
import azure.functions as func


def main(req: func.HttpRequest):
    organization_ids = [601793500207384061, 863973]
    print("Getting all Configurations")
    config = configuration.get_all_configurations(organization_ids, is_cloud=True)
    print(config)
    configuration.store_all_configurations(config, organization_ids, is_cloud=True)
    # blob_storage.dump_data('temp-location', {'Data': 'Temp Data'})
    return func.HttpResponse(
             "This HTTP triggered function executed successfully",
             status_code=200
        )
