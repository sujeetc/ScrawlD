# 'ARTHM'	 : Arithmetic (Integer Overflow, Underflow)
# 'DOS'		 : Denial of Service
# 'LE'		 : Locked Eather
# 'RENT'	 : Re-entrancy
# 'TimeO'	 : Timestam Ordering
# 'TimeM'	 : Time Manipulation
# 'TX-Origin': Access control
# 'UE'		 : Unhandled Exception
import math


class Tools_Info:
	tool_vuln_support = {
		'slither' : 	{        'DOS','LE','RENT','TimeM',		   'TX-Origin','UE'},
		'mythril' : 	{'ARTHM','DOS',		'RENT','TimeM','TimeO','TX-Origin','UE'},
		'smartcheck' :  {'ARTHM','DOS','LE',	   'TimeM',		   'TX-Origin','UE'},
		'oyente' : 		{'ARTHM',			'RENT','TimeM','TimeO'				   },
		'osiris' : 		{'ARTHM'												   }
	}	
	vuln_threshold = {
        
        'ARTHM':0,
        'DOS':0,
        'LE':0,
        'RENT':0,
        'TimeM':0,
        'TimeO':0,
        'TX-Origin': 0,
        'UE':0
    }

	def get_threshold(self):

		for vuln in self.vuln_threshold:
			vuln_support_count=0
			for tool_name in self.tool_vuln_support:
				if (vuln in self.tool_vuln_support[tool_name]):
					vuln_support_count += 1
			threshold=int(math.ceil(float(vuln_support_count)/2))  # Current Threshold is ceil(n/2) 
																   # n = no. of tools that detect the particular vulnerability
			self.vuln_threshold[vuln]=threshold
		# print(self.vuln_threshold)
			

# tools_info_obj = Tools_Info()
# tools_info_obj.get_threshold()
