import math
import sys
sys.path.insert(1,"./parser")
import mythril
import oyente
import slither
import smartcheck
import osiris

import sys
import os
path='../results'
seq_no=sys.argv[1]
solidity_file=sys.argv[2]
choice=sys.argv[3] # Choice Options= all, majority_all, majority_unique

solidity_file=solidity_file.replace('./','')
class Main:

    tools=["oyente","smartcheck","osiris","slither","mythril"]
    vuln_threshold = {
        'TX-Origin': 1,
        'ARTHM':1,
        'DOS':1,
        'LE':1,
        'RENT':1,
        'TimeM':1,
        'TimeO':1,
        'UE':1,
    }
    final_result = {key: {} for key in vuln_threshold.keys()}  # Dictionary of Dictionaries
    mythril_obj = mythril.Mythril()
    oyente_obj = oyente.Oyente()
    slither_obj = slither.Slither()
    smartcheck_obj = smartcheck.SmartCheck()
    osiris_obj = osiris.Osiris()


    tools_obj=[]
    tools_threshold=[]
    for tool in tools:
        tools_obj.append(vars()[tool+'_obj'])


    def get_threshold(self):
        for tool,tool_obj in zip(self.tools,self.tools_obj):
            vars()[tool+'_vulnerabilities']=[]
            for vuln in tool_obj.vulnerabilities:
                vars()[tool+'_vulnerabilities'].append(tool_obj.vulnerabilities[vuln])

        for vuln in self.vuln_threshold.keys():
            vars()[vuln+'_count']=0

        for vuln in self.vuln_threshold.keys():
            for tool in self.tools:
                if vuln in vars()[tool+'_vulnerabilities']:
                    vars()[vuln+'_count'] += 1

        for vuln in self.vuln_threshold.keys():
            self.vuln_threshold[vuln]=int(math.ceil(vars()[vuln+'_count']/2))


        # for vuln in self.vuln_threshold.keys():
        #      print(vuln, vars()[vuln+'_count'], self.vuln_threshold[vuln])



    def get_results(self):
        #print(solidity_file)
        mythril_result=self.mythril_obj.getResults(path+'/mythril/'+solidity_file.replace('.sol','_mythril.json'))
        smartcheck_result=self.smartcheck_obj.getResults(path+'/smartcheck/'+solidity_file.replace('.sol','_smartcheck.txt'))
        slither_result=self.slither_obj.getResults(path+'/slither/'+solidity_file.replace('_ext.sol','.sol.json'))
        osiris_result=self.osiris_obj.getResults(path+'/osiris/'+solidity_file.replace('.sol','.json'))



        oyente_result_2 = {
            'TX-Origin': [], # Access control
            'ARTHM': [], # Arithmetic: Integer Overflow, Underflow
            'DOS': [], # Denial of Service
            'TimeO': [], # Timestamp Ordering
            'TimeM': [], # Time Manipulation
            'RENT': [], # Re-entrancy
            'UE': [], # Unhandled Exception
            'LE': [] # Locked Eather
        }
        for (root,dirs, files) in os.walk(path+'/oyente/'):
            for file in files:
                if solidity_file in file and '.json' in file:
                    oyente_result_1=self.oyente_obj.getResults(path+'/oyente/'+file)
                    for vuln_type in oyente_result_1.keys():
                        for lineno in oyente_result_1[vuln_type]:
                            oyente_result_2[vuln_type].append(lineno)


        oyente_result=oyente_result_2

        # print("Slither Result:",slither_result)
        # print("Mythril Result:",mythril_result)
        # print("Smartcheck Result:",smartcheck_result)
        # print("Oyente Result:",oyente_result)
        # print("Osiris Result:",osiris_result)


        


        for tool in self.tools:
            for vuln_type in vars()[tool+'_result'].keys():
                if (vars()[tool+'_result'][vuln_type]):
                    vars()[tool+'_result'][vuln_type] = set(vars()[tool+'_result'][vuln_type])
                    # Gets uniqe lines reported by each tool for each vulnerability,
                    # This removes duplicate lines reported by the tool for same vulnerability

                    vars()[tool+'_result'][vuln_type] = list(vars()[tool+'_result'][vuln_type])
                    vars()[tool+'_result'][vuln_type].sort()
                    # Sort the line numbers reported

                for lineno in vars()[tool+'_result'][vuln_type]:
                    if(vuln_type == 'RENT'):
                        self.final_result[vuln_type][lineno]=0
                    elif (vuln_type == 'LE'):
                        self.final_result[vuln_type][1]=0
                    else:
                        self.final_result[vuln_type][int(lineno)]=0
                    #Initializes each line reported by 0

        for tool in self.tools:
            for vuln_type in vars()[tool+'_result'].keys():
                if (vuln_type == 'LE'):
                    if(len(vars()[tool+'_result'][vuln_type]) > 0):
                        self.final_result[vuln_type][1]=self.final_result[vuln_type][1]+1
                        if (choice == 'all'):
                            print(solidity_file, vuln_type, tool)
                elif (vuln_type == 'RENT'):
                    for function_name in vars()[tool+'_result'][vuln_type]:
                        self.final_result[vuln_type][function_name] = self.final_result[vuln_type][function_name] + 1
                        if (choice == 'all'):
                            print(solidity_file, vuln_type, function_name, tool)
                elif (vuln_type != 'LE'):
                    for lineno in vars()[tool+'_result'][vuln_type]:
                        self.final_result[vuln_type][int(lineno)]=self.final_result[vuln_type][int(lineno)]+1
                        if (choice == 'all'):
                            print(solidity_file, vuln_type, lineno, tool)
                        #Increases the count if tool reports at line no




    def print_results(self):
        #print(self.final_result)
        #print(seq_no,  end =" ")
        if (choice != 'all'):
            print_vuln=[]
            is_solidity_file_printed=0
            for vuln in self.final_result:
                for lineno in self.final_result[vuln]:
                    if(self.final_result[vuln][lineno] >= self.vuln_threshold[vuln]):
                        if(is_solidity_file_printed == 0):
                            print(solidity_file, end =" ")            
                            is_solidity_file_printed=1
                        #print(vuln,lineno,self.final_result[vuln][lineno])
                        if(choice == 'majority_all' or (vuln not in print_vuln and choice == 'majority_unique')):
                            print(vuln , end =" ")
                            print_vuln.append(vuln)
            if(is_solidity_file_printed == 1):
                print()
            



#To do: Each tool supports different vulnerabilities, so the threshold
#should be different for each vulnerability

main=Main()
main.get_threshold()
main.get_results()
main.print_results()
