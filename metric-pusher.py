import requests
import sys

class metricPusher:

    def __init__(self, curi):
        self.curi = curi

        self.node_id = ""

        self.get_node_id()
        
        self.applications = []
        self.actors = []
        

    def get_node_id(self):
        resp = requests.get('http://' + self.curi + '/id')
        if resp.status_code != 200:
            print('ERROR: ' + 'GET /id {}'.format(resp.status_code))

        else:
            resp_json = resp.json()
            self.id = resp_json['id']
            print 'Node id: ' + self.id


    def get_application_ids(self):
        resp = requests.get('http://' + self.curi + '/applications')
        if resp.status_code != 200:
            print('ERROR: ' + 'GET /applications {}'.format(resp.status_code))

        else:
            self.applications = resp.json()
            print "Application ids: "
            for app in self.applications:
                print app

    def get_actor_ids(self):
        resp = requests.get('http://' + self.curi + '/actors')
        if resp.status_code != 200:
            print('ERROR: ' + 'GET /actors {}'.format(resp.status_code))

        else:
            self.actors = resp.json()
            print "Actor ids: "
            for actor in self.actors:
                print actor

    def set_health(self, value):
        
        data = {"value": value}

        resp = requests.post('http://' + self.curi + '/node/resource/healthMetric',
                             json=data)

        if resp.status_code != 200:
            print('ERROR: ' + 'POST /node/resource/healthMetric {}'.format(resp.status_code))

        else:
            print 'Updated health. ID: ' + resp.json()["id"]


            
if __name__ == "__main__":

    curi = sys.argv[1]
    mp = metricPusher(curi)
    mp.get_application_ids()
    mp.get_actor_ids()
    mp.set_health(0.5)
