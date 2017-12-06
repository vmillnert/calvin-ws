import json
import sys
import yaml
import logging

class Workload(object):
	def __init__(self, file_name):
		self.workload = yaml.load(open(file_name))

	# Produce workload
	def next(self):
		for t in sorted(self.workload, key=lambda x: float(x)):
			yield (float(t), self.workload[t])

	# Get the last time stamp in the workload
	def get_workload_time_span(self):
		return float(sorted(self.workload, key=lambda x: int(x))[-1])+1