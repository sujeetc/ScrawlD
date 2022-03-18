# ScrawlD: A Dataset of Real World Ethereum Smart Contracts Labelled with Vulnerabilities


## Smart Contracts
   ./contracts directory contains 6780 Smart Contracts from Ethereum Blockchain. ScrawlD provides a vulnerability report of these Smart Contracts using five tools. Interested people can parse the vulnerabilities.json file for each bug type by setting thresholds in the "Vulnerabilities" Section and get labels for the Smart Contracts.


## Used Tools

1. Slither
2. Mythril
3. Smartcheck
4. Oyente
5. Osiris



## Vulnerabilities
   vulnerabilites.json contains vulnerabilites in each smart contracts as per reported by 5 tools (Slither, Smartcheck, Mythril, Oyente, Osiris)

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



### How to read vulnerabilites.json?

![vuln-example](https://github.com/sujeetc/ScrawlD/blob/main/images/example.png?raw=true)

   1. Above snippet is taken from file vulnerabilities.json
   2. It shows an object in the vulnerabilities.json file
   3. According to the above snippet, smart contract deployed on address 0x000000002bb43c83ece652d161ad0fa862129a2c at Ethereum blockchain has Arithmetic (ARTHM) vulnerability at line number 350 and 372 according to results generated by Mythril tool
   4. Reentrancy (RENT) is a function-level bug. That is why we showed ContractName.FunctionName in vulnerabilities.json file.
   5. Moreover, Locked Ether (LE) is a contract-level bug. So, if the tool says that the contract is vulnerable for LE, we printed tool-name for LE in the vulnerabilities.json file.



##How to collect Real World Smart Contracts from Etherscan API

###Script
 scripts/ExtFromEtherScan.py

###Usage
 1. python3 ExtFromEtherScan.py

 2. contracts.csv contains addresses of Real World Smart Contracts
