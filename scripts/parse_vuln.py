#This script parse vulnerabilities.json and produce bug report for 
#each smart contract as per majority of tools (>= ceil(n/2))

import json
import tools_info
import sys

class Parse_Vuln:
	filename='../vulnerabilities.json'
	tools_info_obj = tools_info.Tools_Info()
	def read_file_content(self):
		file_obj = open(self.filename)
		 
		data = json.load(file_obj)
		
		self.tools_info_obj.get_threshold()

		for filename in data:
			final_result = {key: {} for key in self.tools_info_obj.vuln_threshold.keys()}  # Dictionary of Dictionaries

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

	        

			is_filename_printed=0
			print_vuln=[]
			for vuln in final_result:
				for lineno in final_result[vuln]:
					if(final_result[vuln][lineno] >= self.tools_info_obj.vuln_threshold[vuln]):
						if (is_filename_printed == 0):
							print(filename, end =" ")		
							is_filename_printed=1
						if (vuln == 'LE'):
							print(" \""+vuln+"\"",end="")
						elif(vuln != 'LE'):
							print(" \""+vuln+"\":"+str(lineno),end="")
			if (is_filename_printed ==1):
				print()


		
		#print(self.tools_info_obj.vuln_threshold)
		 
		file_obj.close()


parse_vuln_obj=Parse_Vuln()
parse_vuln_obj.read_file_content()