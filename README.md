# ScrawlD: A Dataset of Real World Ethereum Smart Contracts Labelled with Vulnerabilities

## Note: please cite our [work](https://arxiv.org/abs/2202.11409) if you use it 
 If you use any part of this dataset or entire dataset, please cite our works in your research papers. You can cite our [paper](https://arxiv.org/abs/2202.11409) using bibtex as follows
  
 @article{yashavant2022scrawld,
  title={ScrawlD: A Dataset of Real World Ethereum Smart Contracts Labelled with Vulnerabilities},
  author={Chavhan Sujeet Yashavant, Saurabh Kumar, and Amey Karkare},
  journal={arXiv preprint arXiv:2202.11409},
  year={2022}
}


## Smart Contracts
   data/contracts directory contains 6780 Smart Contracts from Ethereum Blockchain. ScrawlD provides a vulnerability report of these Smart Contracts using five tools. Interested people can parse the vulnerabilities.json file for each bug type by setting thresholds in the "Vulnerabilities" Section and get labels for the Smart Contracts.


## Used Tools

1. Slither
2. Mythril
3. Smartcheck
4. Oyente
5. Osiris



## Vulnerabilities
   data/vulnerabilites.json contains vulnerabilites in each smart contracts as per reported by 5 tools (Slither, Smartcheck, Mythril, Oyente, Osiris)

   | Vulnerability | SWC-ID | Description   | Number of Tools that can Detect the Vulnerability | Threshold |
   | ------------- | ------------- | ------------- | ---------- | ---------- | 
   | ARTHM  | SWC-101 | Arithmetic (Integer Overflow and Underflow)  | 4 | 2 |
   | DOS | SWC-113, SWC-128 | Denial of Service | 3 | 2 |
   | LE | - | Locked Ether | 2 | 1 |
   | RENT | SWC-107 | Reentrancy | 3 | 2 |
   | TimeM | SWC-116 | Time Manipulation (Block values as a proxy for time) | 4 | 2 |
   | TimeO | SWC-114 | Timestamp Ordering (Transaction Order Dependence) | 2 | 1 |
   | Tx-Origin  | SWC-115 | Authorization through tx.origin | 3 | 2 |
   | UE | SWC-104 | Unhandled Exception (Unchecked Call Return Value) | 3 | 2 |



### How to read data/vulnerabilites.json?

![vuln-example](https://github.com/sujeetc/ScrawlD/blob/main/images/example.png?raw=true)

   1. Above snippet is taken from file data/vulnerabilities.json
   2. It shows an object in the data/vulnerabilities.json file
   3. According to the above snippet, smart contract deployed on address 0x000000002bb43c83ece652d161ad0fa862129a2c at Ethereum blockchain has Arithmetic (ARTHM) vulnerability at line number 350 and 372 according to results generated by Mythril tool
   4. Reentrancy (RENT) is a function-level bug. That is why we showed ContractName.FunctionName in data/vulnerabilities.json file.
   5. Moreover, Locked Ether (LE) is a contract-level bug. So, if the tool says that the contract is vulnerable for LE, we printed tool-name for LE in the data/vulnerabilities.json file.




# Parser that parses results by different Tools

## data Directory

### Text Files
* data/function_lines.txt contains line numbers' range for each function for each contract
    * Slither's parser uses this data
* data/scrawld_res_all.txt contains vulnerability report produced by each tool for each contract
    * It contains vulnerabilities that are supported by ScrawlD
    * Along with vulnerability, it contains location (Line Number)
        * Locked Ether (LE) is a contract level vulnerability, that's why there is no Line Number associated with it
        * Re-entrancy (RENT) is a function level vulnerability, that's why there is function name associated with it
* data/scrawld_majority_all.txt contains vulnerabilities present for each contract according to majority tools
    * If a contract has a vulnerability at two locations, then data/scrawld_majority_all.txt shows that vulnerability twice
    * data/scrawld_majority_all.txt doesn't have location for each vulnerability, for getting locations use script scripts/parse_final_json.py
* data/scrawld_majority_unique.txt contains unique vulnerabilities for each contract

### JSON Files
* data/vulnerabilities.json contains vulnerability reports provided by tools for each contract in JSON format
* data/majority_result.json contains vulnerability report according to majority of tools


## scripts Directory
*  scripts directory contains python and bash scripts
*  scripts/parser directory contains parser script for each tool and supporting files for parser scripts
    * main.py --> main file that takes solidity file as input and produces results as per argument
        * Usage --> python3 main.py sequence_num(any number) solidity_file choice(all, majority_all, majority_unique)
        * choice
            * all --> emits all results with location
            * majority_all --> emits results by using majority voting (>=50%) of tools. It produces results without location information. If a vulnerability is present twice it will print it twice.
            * majority_unique --> Similar to majority_all. But it emits unique vulnerability per file. That means if a vulnerability is present twice it will print it once.
    * call_main.sh --> calls main.py for contracts results/sample_results.txt (can be changed by editing the file)
        * Usage --> bash call_main.sh parallel_processes choice(all, majority_all, majority_unique)
        * parallel_processes --> Number of parallel processes to run while parsing the results
        * choice --> Explained above while explaining main.py 
    * Please note that main.py produces results by parsing the results provided by different tools. It assumes that the tools' results are available. The user has to get tool's results and then use main.py
*  scripts/get_final_json.py parses results in text format (data/scrawld_res_all.txt) and produces results in JSON format
    * Usage: python3 scripts/get_final_json.py --src data/scrawld_res_all.txt --dst data/vulnerabilities.json
    * Feed the result of bash call_main.sh parallel_processes all to this script and get vulnerabilities with location information according to majority of the tools
*  scripts/parse_final_json.py parses results in JSON format (output of scripts/get_final_json.py) and produces vulnerability report according to the majority of tools
    * Usage: python3 scripts/parse_final_json.py --src data/vulnerabilities.json --dst data/majority_result.json


* scripts/ExtFromEtherScan.py can be used to collect Real World Smart Contracts from Etherscan API
	* Usage: python3 scripts/ExtFromEtherScan.py
	* data/contracts.csv contains addresses of Real World Smart Contracts

* scripts/graph.py emits the data in graphical format
 * Usage: cd scripts; python3 graph.py choice
 * Choice
    * 1: Total Contracts per Vulnerability
    * 2: Total Warnings per Vulnerability 
    * 3: Total Contracts with unique Vulnerabilities

## results Directory
* mythril, osiris, oyente, slither, smartcheck --> These directories contains sample results generated by the tools for the Real-World Ethereum Smart Contracts given in sample_results.txt
* sample_results.txt --> list of 100 Real-World Ethereum Smart Contracts. We provide sample results of these contracts to run main scripts.
* Total_Contracts_with_unique_Vuln.csv --> Contains total contracts with unique vulnerabilities according to majority of the tools
* Warnings_and_Unique_Contracts_per_Vuln.csv  --> Contains Total Warnings per Vulnerability and Unique Contracts per Vulnerability according to majority of the tools

## graphs Directory
* contracts_per_vuln.pdf --> contains number of contracts per vulnerability according to majority of the tools
* majority_warnings_per_vuln.pdf --> Contains number of warnings per vulnerability according to majority of the tools
* unique_vuln.pdf --> Contains total contracts with unique vulnerabilities according to majority of the tools
