import json
import subprocess

class Osiris:
    vulnerabilities = {
        #'TBD': 'TX-Origin',
        'overflow': 'ARTHM',
        'underflow': 'ARTHM',
        #'TBD': 'TimeO',
        #'TBD': 'RENT',
        #'TBD': 'TimeM',
        #'TBD': 'UE'
    }

    def getResults(self, filename):
        result = {
            'TX-Origin': [], # Access control
            'ARTHM': [], # Arithmetic: Integer Overflow, Underflow
            'DOS': [], # Denial of Service
            'TimeO': [], # Timestam Ordering
            'TimeM': [], # Time Manipulation
            'RENT': [],  # Re-entrancy
            'UE': [], # Unhandled Exception
            'LE': [] # Locked Eather
        }

        f = open(filename)
        data_dict = json.load(f)
        f.close()

        keys=data_dict.keys()

        for key in keys:
            subprocess.call(["./parser/osiris_dup_keys.sh"+" "+key+" "+filename], shell=True)


        f = open(filename)
        data_dict = json.load(f)
        f.close()

        keys=data_dict.keys()

        for key in keys:
            vuln_keys=data_dict[key].keys()
            for vuln_key in vuln_keys:
                if vuln_key in self.vulnerabilities.keys():
                    if (data_dict[key][vuln_key] != False):
                        line=data_dict[key][vuln_key]
                        lineNo=line.rstrip().split(':')[2]
                        if lineNo not in result[self.vulnerabilities[vuln_key]]:
                            result[self.vulnerabilities[vuln_key]].append(lineNo)

        return result

