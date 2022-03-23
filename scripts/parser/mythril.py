import json
import sys
import subprocess
import os

path='../results'
class Mythril:
    vulnerabilities = {
        '115': 'TX-Origin',

        '101': 'ARTHM',

        '113': 'DOS',

        '114': 'TimeO',

        '107': 'RENT',

        '116': 'TimeM',

        '104': 'UE',

        #'TBD' : 'LE'

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

    def parse_issue(self, issues):

        for element in issues:
            keyword = element['swc-id']

            if keyword in self.vulnerabilities.keys():
                key = self.vulnerabilities[keyword]

                if (key in 'RENT'):
                    functionName = element['function']
                    contractName = element['contract']
                    if(contractName+'.'+functionName not in self.result[key]):
                        self.result[key].append(contractName+'.'+functionName)
                else:
                    if('lineno' in element.keys()):
                        lineNo = element['lineno']
                        self.result[key].append(lineNo)
        return self.result;


    def getResults(self, filename):

        try:
            f = open(filename)
            data = json.load(f)
        except:
            subprocess.call(["bash parser/process_mythril_file.sh"+" "+filename.replace('.sol','_mythril.json')], shell=True)
            f = open(filename.replace('.json','_bak.json'))
            #file_lines = f.readlines()
            #for line in file_lines:
                #print(line)
            data = json.load(f)
            os.remove(filename.replace('.json','_bak.json'))
        f.close()

        if (type(data) is dict):
            issues = data['issues']
            self.parse_issue(issues)
        if (type(data) is list):
            for d in data:
                issues = d['issues']
                self.parse_issue(issues)
        return self.result


