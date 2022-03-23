#This script parse vulnerabilities.json and produce bug report for 
#each smart contract as per majority of tools (>= ceil(n/2))

import json
import tools_info
import sys
import argparse

class Parse_Vuln:
	json_data = dict()
	filename='vulnerabilities.json'
	tools_info_obj = tools_info.Tools_Info()

	def ParseArgs(self):
		"""Parse command line argumnets."""
		Args = argparse.ArgumentParser(description="Parser to parse vulnerability result file into JSON")
		Args.add_argument("--src", required=True,
				help="result file absolute path to parse") # Input: ../data/scrawld_res_all.txt
		Args.add_argument("--dst", required=True,
						help="output file absolute path to generate JSON file from result")
		return Args.parse_args()
	
	

	def read_file_content(self, args):
		inpFile = args.src
		output_File = args.dst

		file_obj = open(inpFile)
		 
		data = json.load(file_obj)
		
		self.tools_info_obj.get_threshold()

		for filename in data:
			final_result = {key: {} for key in self.tools_info_obj.vuln_threshold.keys()}  # Dictionary of Dictionaries
#			majority_result = {key: {} for key in self.tools_info_obj.vuln_threshold.keys()}  # Dictionary of Dictionaries
			majority_result = {}
			
			for vuln in data[filename].keys():
				if (vuln != 'LE'):
					for tool_name in data[filename][vuln].keys():
						for lineno in data[filename][vuln][tool_name]:
							final_result[vuln][lineno]=0
				if (vuln == 'LE'):
					for tool_name in data[filename][vuln]:
							final_result[vuln][1]=0

			for vuln in data[filename].keys():
				if (vuln != 'LE'):
					for tool_name in data[filename][vuln].keys():
						for lineno in data[filename][vuln][tool_name]:
							final_result[vuln][lineno] += 1
				if (vuln == 'LE'):
					for tool_name in data[filename][vuln]:
							final_result[vuln][1] += 1


			final_result = dict( [(k,v) for k,v in final_result.items() if len(v)>0])  # Delete Empty keys from the Dictionary


			for vuln in final_result:
				majority_result[vuln] = []

			print_vuln=[]
			for vuln in final_result:
				for lineno in final_result[vuln]:
					if(final_result[vuln][lineno] >= self.tools_info_obj.vuln_threshold[vuln]):
						if (vuln == 'LE'):
							majority_result[vuln].append('Yes')
						elif(vuln != 'LE'):
							majority_result[vuln].append(lineno)
			

			majority_result = dict( [(k,v) for k,v in majority_result.items() if type(v) == int or len(v)>0])  # Delete Empty keys from the Dictionary
			
			self.json_data[filename]=majority_result

		
		#print(self.tools_info_obj.vuln_threshold)
		self.json_data = dict( [(k,v) for k,v in self.json_data.items() if len(v)>0])  # Delete Empty keys from the Dictionary
		 
		file_obj.close()
		with open(output_File, 'w') as f:
			json.dump(self.json_data, f, sort_keys = True, indent = 4)


parse_vuln_obj=Parse_Vuln()
parse_vuln_obj.read_file_content(parse_vuln_obj.ParseArgs())