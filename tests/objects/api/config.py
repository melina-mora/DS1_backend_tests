import json
import os


class ConfigOpportunity:

	def configure_test_data_opportunities(self):
		"""
		Configures API data from objects.config_obj related to opportunities
		:return:
		"""
		# Fetch file
		script_dir = os.path.dirname(__file__)
		file_dir = '..\\api\\apis_opportunities.json'
		url = os.path.join(script_dir, file_dir)

		# Read file
		with open(file=url) as file:
			data = json.load(file)
		return data

class ConfigBusinessLines:

	def configure_test_data_business_lines(self):
		"""
		Configures API data from objects.config_obj related to opportunities
		:return:
		"""
		# Fetch file
		script_dir = os.path.dirname(__file__)
		file_dir = '..\\api\\apis_businesslines.json'
		url = os.path.join(script_dir, file_dir)

		# Read file
		with open(file=url) as file:
			data = json.load(file)
		return data
