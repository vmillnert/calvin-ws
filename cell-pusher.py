import requests
import sys


class CellPusher:

    def __init__(self, curi):
        self.curi = curi

        self.node_id = ""

        self.get_node_id()

        self.applications = []
        self.actors = []
        self.capabilities = []

        self.log_user_id = ""

    def get_node_id(self):
        resp = requests.get('http://' + self.curi + '/id')
        if resp.status_code != 200:
            print('ERROR: ' + 'GET /id {}'.format(resp.status_code))

        else:
            resp_json = resp.json()
            self.node_id = resp_json['id']
            print('Node id: ' + self.node_id)

    def get_application_ids(self):
        resp = requests.get('http://' + self.curi + '/applications')
        if resp.status_code != 200:
            print('ERROR: ' + 'GET /applications {}'.format(resp.status_code))

        else:
            self.applications = resp.json()
            print("Application ids: ")
            for app in self.applications:
                print(app)

    def get_actor_ids(self):
        resp = requests.get('http://' + self.curi + '/actors')
        if resp.status_code != 200:
            print('ERROR: ' + 'GET /actors {}'.format(resp.status_code))

        else:
            self.actors = resp.json()
            print("Actor ids: ")

            for actor in self.actors:
                print(actor)

    def get_capabilities(self):
        resp = requests.get('http://' + self.curi + '/capabilities')
        if resp.status_code != 200:
            print('ERROR: ' + 'GET /capabilities {}'.format(resp.status_code))

        else:
            capabilities = resp.json()
            print("capabilities: " + str(capabilities))

            # print "Capabilities: "
            # for capability in self.capabilities:
            #     print capability

    def get_attributes(self):
        resp = requests.get('http://' + self.curi + '/node/' + self.node_id)
        if resp.status_code != 204:
            print('ERROR: ' + 'GET /node/<node_id> {}'.format(resp.status_code))
        else:
            node_info = resp.json()
            print("attributes: " + str(node_info['attributes']))

    def set_health(self, value):

        data = {"value": value}

        resp = requests.post('http://' + self.curi + '/node/attribute/healthMetric',
                             json=data)

        if resp.status_code != 204:
            print('ERROR: ' + 'POST /node/attribute/healthMetric {}'.format(resp.status_code))

        else:
            print('Updated node health with: ' + str(value))

    def add_attribute(self):
        # data = {"index": ["user_extra", {"healthy": "yes"}]}
        # data = {"node_name": {"name": "wasp"}}
        data = {"health": "good"}
        # data = [{"node_name": {}},
        #         {"owner": {}},
        #         {"address": {}},
        #         {"user_extra": {"healthy": "yes"}}]

        resp = requests.post('http://' + self.curi + '/node/' + self.node_id + '/attributes/indexed_public',
                             json=data)

        if resp.status_code != 200:
            print('ERROR: ' + 'POST /node/attributes/indexed_public {}'.format(resp.status_code))

        else:
            print('Added attribute!')

    def add_value(self):

        # data = {"index": ["user_extra", {"healthy": "yes"}]}
        # data = {"node_name": {"name": "wasp"}}

        data = {"value": "yes"}

        resp = requests.post('http://' + self.curi + '/index/healthy',
                             json=data)

        if resp.status_code != 200:
            print('ERROR: ' + 'POST /index/healthy {}'.format(resp.status_code))

        else:
            print('Added health-value!')

    def get_value(self):

        # data = {"index": ["user_extra", {"healthy": "yes"}]}
        # data = {"node_name": {"name": "wasp"}}

        resp = requests.get('http://' + self.curi + '/storage/health')

        if resp.status_code != 200:
            print('ERROR: ' + 'GET /storage/health {}'.format(resp.status_code))

        else:
            data = resp.json()
            print('Got health-value: ')
            print(data)

    def get_health(self):

        resp = requests.get('http://' + self.curi + '/node/attribute/getHealth')

        if resp.status_code != 200:
            print('ERROR: ' + 'GET /node/attribute/getHealth/ {}'.format(resp.status_code))

        else:
            data = resp.json()
            print('Is healthy: ' + str(data["healthy"]))

    def register_for_logging(self):

        data = {
            'events': ['health_new']
        }

        resp = requests.post('http://' + self.curi + '/log',
                             json=data)

        if resp.status_code != 200:
            print('ERROR: ' + 'GET /node/attribute/health {}'.format(resp.status_code))

        else:
            data = resp.json()
            print('Registred for log: ')
            print(data)

            print('User id: ' + str(data['user_id']))
            self.log_user_id = data['user_id']

    def get_log(self):

        print("About to request the stream")

        with requests.get('http://' + self.curi + '/log/' + self.log_user_id, stream=True) as r:
            for line in r.iter_lines():
                print(line)
        # resp = requests.get('http://' + self.curi + '/log/' + self.log_user_id, stream=True)
        # print "Streaming log..."

        # for line in iter(resp.content.readline, ''):
        #     print line

    def set_imei_cells(self, value):

        data = {"value": value}

        resp = requests.post('http://' + self.curi + '/node/attribute/imeicells',
                             json=data)

        if resp.status_code != 204:
            print('ERROR: ' + 'POST /node/attribute/imeicells {}'.format(resp.status_code))

        else:
            print('Updated node imei cell ids with: ' + str(value))


if __name__ == "__main__":
    # syntax: python cell-pusher.py <curi> <imei> <cell>

    curi = sys.argv[1]
    imei = sys.argv[2]
    cell = sys.argv[3]
    cp = CellPusher(curi)

    imei_cells = [{"imei": imei, "cell": cell}]

    cp.set_imei_cells(imei_cells)

