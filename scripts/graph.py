import matplotlib.pyplot as plt
import numpy as np
import os
present_dir=os.getcwd()
data_path=present_dir.replace('scripts','data/')
graph_path=present_dir.replace('scripts','graphs/')


class Graph:
    dict_contracts_per_vuln = {
        'ARTHM':0,
        'DOS':0,
        'LE':0,
        'RENT':0,
        'TimeM':0,
        'TimeO':0,
        'TX-Origin': 0,
        'UE':0,
    }

    no_of_vuln = {
        0:0,
        1:0,
        2:0,
        3:0,
        4:0,
        5:0,
        6:0,
        7:0,
        8:0
    }


    def tool_result(self):
        tools=['mythril','oyente','osiris','slither','smartcheck']
        filename=data_path+'scrawld_res_all.txt'
        file1 = open(filename, 'r')
        Lines = file1.readlines()
        for tool_name in tools:
            for key in self.dict_contracts_per_vuln.keys():
                self.dict_contracts_per_vuln[key]=0
            for key in self.dict_contracts_per_vuln.keys():
                file_list = []
                for line in Lines:
                    # print(line.rstrip().split(' ')[0])
                    if key in line and tool_name in line and line.rstrip().split(' ')[0] not in file_list:
                        file_list.append(line.rstrip().split(' ')[0])
                        self.dict_contracts_per_vuln[key] = self.dict_contracts_per_vuln[key] + line.count(key)
            print(tool_name, self.dict_contracts_per_vuln)
            xlabel="Vulnerability Name"
            ylabel="Number of Contracts"
            is_rotate=1
            self.plot_graph(self.dict_contracts_per_vuln, graph_path+tool_name+'.pdf',xlabel,ylabel, is_rotate)


    def majority_warnings_per_vuln(self):
        filename=data_path+'scrawld_majority_all.txt'
        file1 = open(filename, 'r')
        Lines = file1.readlines()
        for line in Lines:
            for key in self.dict_contracts_per_vuln.keys():
                if key in line:
                    self.dict_contracts_per_vuln[key] = self.dict_contracts_per_vuln[key] + line.count(key)
        xlabel="Vulnerability Name"
        ylabel="Count of Warnings"
        is_rotate=1
        self.plot_graph(self.dict_contracts_per_vuln, graph_path+'majority_warnings_per_vuln.pdf',xlabel,ylabel, is_rotate)

    def contracts_per_vuln(self):
        filename= data_path+'scrawld_majority_unique.txt'
        file1 = open(filename, 'r')
        Lines = file1.readlines()

        for line in Lines:
            for key in self.dict_contracts_per_vuln.keys():
                if key in line:
                    self.dict_contracts_per_vuln[key] = self.dict_contracts_per_vuln[key] + 1
        xlabel="Vulnerability Name"
        ylabel="Number of Contracts"
        is_rotate=1
        self.plot_graph(self.dict_contracts_per_vuln, graph_path+'contracts_per_vuln.pdf',xlabel,ylabel, is_rotate)


    def zero_to_nan(self,values):
        """Replace every 0 with 'nan' and return a copy."""
        to_remove_keys=[]
        for key in values.keys():
            if(values[key] == 0):
                to_remove_keys.append(key)
        for key in to_remove_keys:
                values.pop(key)
        return values

    def get_no_of_vuln(self):
        filename= data_path+'scrawld_majority_unique.txt'

        file1 = open(filename, 'r')
        Lines = file1.readlines()
        for line in Lines:
            vuln_count=0
            for key in self.dict_contracts_per_vuln.keys():
                if key in line:
                    vuln_count=vuln_count+1
            if(vuln_count>0):
                self.no_of_vuln[vuln_count]=self.no_of_vuln[vuln_count]+1
            if(vuln_count == 0):
                self.no_of_vuln[vuln_count]=self.no_of_vuln[vuln_count]+1
        xlabel="Number of Unique Vulnerabilities"
        ylabel="Number of Contracts"
        is_rotate=0
        self.plot_graph(self.zero_to_nan(self.no_of_vuln), graph_path+'unique_vuln.pdf',xlabel,ylabel, is_rotate)

    def plot_graph(self, dict, plot_name, xlabel, ylabel, is_rotate):
        contracts_per_vuln_array=[]
        vuln_name_array=[]
        for key in dict.keys():
            if(dict[key] != 0):
                contracts_per_vuln_array.append(dict[key])
                vuln_name_array.append(key)
        ypoints = np.array(contracts_per_vuln_array)

        xlocs=range(0,len(vuln_name_array))

        p1=plt.bar(xlocs, ypoints, color='gray')
        # print(plot_name, xlocs, contracts_per_vuln_array,vuln_name_array)

        if (is_rotate == 1):
            plt.xticks(xlocs, vuln_name_array, rotation=30)
        else:
            plt.xticks(xlocs, vuln_name_array)

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        #plt.show()
        plt.bar_label(p1)
        plt.subplots_adjust(bottom=0.2)
        plt.yscale('log')
        plt.savefig(plot_name)
        plt.clf() 

import sys
choice = sys.argv[1]
#filename = 'unique_vuln.txt'

graph=Graph()
if (int(choice) == 1):
    graph.contracts_per_vuln()
elif (int(choice) == 2):
    graph.majority_warnings_per_vuln()
elif (int(choice) == 3):
    graph.get_no_of_vuln()
elif (int(choice) == 4):
    graph.tool_result()

