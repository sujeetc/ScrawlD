import json
import csv
import line_to_function_name

class Oyente:
    vulnerabilities = {

	    #'TBD': 'TX-Origin',

        'integer_overflow': 'ARTHM',
        'integer_underflow': 'ARTHM' ,

        #'TBD': 'DOS',

        'money_concurrency': 'TimeO',

        'reentrancy': 'RENT',

        'time_dependency': 'TimeM',

	    #'TBD': 'UE',

        #'TBD': 'LE'
    }

    result = {
            'TX-Origin': [], # Access control
            'ARTHM': [], # Arithmetic: Integer Overflow, Underflow
            'DOS': [], # Denial of Service
            'TimeO': [], # Timestam Ordering
            'TimeM': [], # Re-entrancy
            'RENT': [], # Time Manipulation
            'UE': [], # Unhandled Exception
            'LE': [] # Locked Eather
        }
    def process_reentrancy(self, filename, lineNo):
        line_to_function_name_obj = line_to_function_name.LineToFunctionName()
        for key in self.result.keys():
            if 'RENT' in key:
                result_key=self.result[key]
                self.result[key]=[]
                zeroXIndex=filename.index('0x')
                solIndex=filename.index('.sol')
                solidity_file=filename[zeroXIndex:solIndex]+'.sol'
                reent_function_name=line_to_function_name_obj.get_function_name(solidity_file,lineNo)
                if (reent_function_name not in self.result[key]):
                        self.result[key].append(reent_function_name)

    def getResults(self, filename):


        f = open(filename)
        data = json.load(f)
        f.close()

        issues = data['vulnerabilities']
        for element in issues:
                if element in self.vulnerabilities.keys():
                      if(len(issues[element]) > 0):  # Try to replace if(len(issues[element]) > 0) with if(issues[element])
                            for issue in issues[element]:
                                  if(isinstance(issue, str)):
                                             lineNo = issue.split(':')[1]
                                             key = self.vulnerabilities[element]
                                             if lineNo not in self.result[key] and key != 'RENT':
                                                self.result[key].append(lineNo)
                                             elif(key == 'RENT'):
                                                self.process_reentrancy(filename, lineNo)
                                  else:
                                        for i in issue:
                                             lineNo = i.split(':')[1]
                                             key = self.vulnerabilities[element]
                                             if lineNo not in self.result[key] and key != 'RENT':
                                                self.result[key].append(lineNo)
                                             elif (key == 'RENT'):
                                                self.process_reentrancy(filename, lineNo)


	#print(issues[element])
	#for k in self.vulnerabilities.keys():
	#        if(len(issues[k])>0):
	#                print(k,len(issues[k]))
		#key = self.vulnerabilities[keyword]
		#lineNo = element[1]
		#self.result[key].append(lineNo)
        return self.result


