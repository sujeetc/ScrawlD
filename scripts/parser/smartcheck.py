
class SmartCheck:
    vulnerabilities = {
        'SOLIDITY_TX_ORIGIN': 'TX-Origin',

        'SOLIDITY_VAR': 'ARTHM',
        'SOLIDITY_VAR_IN_LOOP_FOR': 'ARTHM',
        'SOLIDITY_UINT_CANT_BE_NEGATIVE' : 'ARTHM',

        'SOLIDITY_TRANSFER_IN_LOOP': 'DOS',

        #'TBD': 'RENT',

        'SOLIDITY_EXACT_TIME': 'TimeM',

        'SOLIDITY_UNCHECKED_CALL': 'UE',

        'SOLIDITY_LOCKED_MONEY': 'LE'
    }


    def getResults(self, filename):
        result = {
            'TX-Origin': [], # Access controll
            'ARTHM': [], # Arithmetic: Integer Overflow, Underflow
            'DOS': [], # Denial of Service
            'TimeO': [], # Timestam Ordering
            'TimeM': [], # Time Manipulation
            'RENT': [], # Re-entrancy
            'UE': [], # Unhandled Exception
            'LE': [] # Locked Eather
        }

        f = open(filename)
        lines = f.readlines()
        f.close()
        nLines = len(lines)
        cur = 0

        while cur < nLines:
            line = lines[cur].rstrip()
            if 'ruleId: ' in line:
                keyword = line.split(': ')[1]
                if keyword in self.vulnerabilities.keys():
                    # find line number
                    key = self.vulnerabilities[keyword]
                    cur += 1
                    while lines[cur].rstrip().startswith('line:') is False:
                        cur += 1

                    lineNo = int(lines[cur].rstrip().split(': ')[1])
                    result[key].append(lineNo)
            cur += 1

        return result


