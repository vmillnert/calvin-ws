from workload import Workload
import time
import urllib
import urllib2
import urlparse

def periodic_curl(workload):
	'''
	fn sends data to calvin runtime
	'''
	url     = urlparse.urljoin('http://localhost:8080', '/BTS/App/location')
	payload = { 'key' : workload}
	params = urllib.urlencode(payload)
	post_req = urllib2.Request(url)
	post_req.add_data(params)

	response = urllib2.urlopen(post_req)
	response_data = response.read()
	response.close()
	print response_data


def main(file_path):
	workload =Workload(file_path)
	for t, workload in workload.next():
		time.sleep(1) # sleep for 1 sec
		periodic_curl(workload) 

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='Periodic POST script')
	parser.add_argument('-w', 
		metavar='W', 
		type=str, 
		default='test_data.json', 
		help='Workload path')
	args = parser.parse_args()
	main(args.w)
	