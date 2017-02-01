import requests
from retry import retry

class ServiceStateException(Exception):
    pass

class Api(object):
    def __init__(self, config):
        super(Api, self).__init__()
        self.init(config)

    def init(self, config):
        self.config = config
        self.stacks_url = "%s/environments" % config.RANCHER_URL
        self.services_url = "%s/services" % config.RANCHER_URL
        self.auth=(config.RANCHER_ACCESS_KEY, config.RANCHER_SECRET_KEY)

    def get_stack_by_name(self, name):
        params = { 'name': name }
        response = requests.get(self.stacks_url, params=params, auth=self.auth)
        return response.json()['data'][0]

    def get_service_by_fullname(self, fullname):
        # fullname = "{stack_name}/{service_name}"
        stack_name = fullname.split('/')[0]
        service_name = fullname.split('/')[1]

        stack = self.get_stack_by_name(stack_name)

        params = {
            'name': service_name,
            'environmentId': stack['id']
            }
        response = requests.get(self.services_url, params=params, auth=self.auth)
        return response.json()['data'][0]

    def get_service_by_id(self, id):
        service_url = "%s/%s" % (self.services_url, id)
        response = requests.get(service_url, auth=self.auth)
        return response.json()

    def service_action(self, id, action, json=None):
        params = { "action": action }
        service_url = "%s/%s" % (self.services_url, id)
        return requests.post(service_url, params=params, auth=self.auth, json=json).json()

    def service_upgrade(self, id, launch_config, batch_size=1, interval_millis=2000, start_first=False):
        json = {
            "inServiceStrategy": {
                "batchSize": batch_size,
                "intervalMillis": interval_millis,
                "launchConfig": launch_config,
                "startFirst": start_first
            },
            "toServiceStrategy": None
        }
        return self.service_action(id, "upgrade", json=json)

    def service_confirm(self, id):
        return self.service_action(id, "finishupgrade")

    @retry(ServiceStateException, tries=30, delay=2, backoff=1.2, max_delay=30)
    def service_wait_state(self, id, state):
        service = self.get_service_by_id(id)
        if service['state'] != state:
            msg = "State is %s (expected %s)" % (service['state'], state)
            raise ServiceStateException(msg)
