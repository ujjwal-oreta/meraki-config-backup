import meraki

class Dashboard:
    def __init__(self, API_KEY):
        self.dashboard = meraki.DashboardAPI(API_KEY, output_log=False, suppress_logging=True)
        