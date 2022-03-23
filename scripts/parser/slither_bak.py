import json
import char_index_to_line
import sys

class Slither:
    char_index_to_line_obj = char_index_to_line.CharIndexToLine()
    vulnerabilities = {
        'tx-origin': 'AC',

        #TBD' : 'ARTHM',

        'calls-loop': 'DOS',

        #'TBD': 'TimeO',

        'reentrancy-unlimited-gas': 'RENT',
        'reentrancy-eth': 'RENT',
        'reentrancy-no-eth': 'RENT',
        'reentrancy-benign': 'RENT',
        'reentrancy-events': 'RENT',

        'timestamp': 'TimeM',

        'unchecked-transfer': 'UE',
        'unchecked-lowlevel': 'UE',
        'unchecked-send': 'UE',

        'locked-ether': 'LE'
    }

    nodeCheck = ['timestamp', 'unchecked-send', 'unchecked-lowlevel', 'unchecked-transfer', 'tx-origin']
    lockedEther = ['locked-ether'] # to check locked ether regarding contracts


    def getResults(self, filename):
        result = {
            'AC': [], # Access control
            'ARTHM': [], # Arithmetic: Integer Overflow, Underflow
            'DOS': [], # Denial of Service
            'TimeO': [], # Timestamp Ordering
            'TimeM': [], # Time Manipulation
            'RENT': [], # Re-entrancy
            'UE': [], # Unhandled Exception
            'LE': [] # Locked Eather
        }

        f = open(filename)
        data = json.load(f)
        f.close()

        detectors = data['results']['detectors']

        for detector in detectors:
            keyword = detector['check']

            if keyword in self.vulnerabilities.keys():
                if keyword in self.nodeCheck:
                    for element in detector['elements']:
                        if element['type'] == 'node':
                            key = self.vulnerabilities[keyword]
                            if "element['source_mapping']['lines']" in locals():
                                lineNo = element['source_mapping']['lines'][0]
                                result[key].append(lineNo)
                            else:
                                lineNo=self.char_index_to_line_obj.get_char_range_per_line(filename, element['source_mapping']['start'])
                                result[key].append(lineNo)
                                  # To do: Add code here for finding
                                      # lines for unchecked-lowlevel vulnerabilit
                            break
                elif keyword in self.lockedEther:
                    for element in detector['elements']:
                        if element['type'] == 'contract':
                                key = self.vulnerabilities[keyword]
                                try:
                                    for lineNo in element['source_mapping']['lines']:
                                        result[key].append(lineNo)
                                except:
                                    result[key].append(1)

                                break
                else:
                    for element in detector['elements']:
                        if element['type'] == 'function':

                            key = self.vulnerabilities[keyword]
                            if "element['source_mapping']['lines']" in locals() and (key not in 'RENT'):
                                for lineNo in element['source_mapping']['lines']:
                                    result[key].append(lineNo)
                            else:
                                if (key in 'RENT'):
                                    reentrancy_function=detector['description'].split(' ')[2]
                                    if (reentrancy_function not in result[key]):
                                        result[key].append(reentrancy_function)
                            break
        return result

solidity_file=sys.argv[1]
obj = Slither()
print(obj.getResults('../../UR-results/slither/'+solidity_file.replace('_ext.sol','.sol.json')))

#To do: Solve Error in these files:
#1./0x44977767dfe24dc8a95ff0affb48a3871312bccf_ext.sol
#2. ./0x1d2b42b3531fad9e544dd4288b788cacc898d555_ext.sol
