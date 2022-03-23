import json
import argparse


def ParseArgs():
    """Parse command line argumnets."""
    Args = argparse.ArgumentParser(description="Parser to parse vulnerability result file into JSON")
    Args.add_argument("--src", required=True,
		    help="result file absolute path to parse") # Input: ../data/scrawld_res_all.txt
    Args.add_argument("--dst", required=True,
                      help="output file absolute path to generate JSON file from result")
    return Args.parse_args()

def main(args):
    """Run Dynamic Analysis and feature extraction locally."""
    inpFile = args.src
    output_File = args.dst
    f = open(inpFile)
    lines = f.readlines()
    f.close()

    nLines = len(lines)
    cur = 0

    data = dict()

    while cur < nLines:
        line = lines[cur].rstrip()
        components = line.split(' ')
        obj = {}
        if components[0] not in data.keys():
            data[components[0]] = obj

        obj = data[components[0]]

        if (components[1] not in obj.keys()) and len(components) == 3:
            obj[components[1]] = []
        elif components[1] not in obj.keys():
            obj[components[1]] = {}

        if components[1] == 'LE':
            obj[components[1]] = obj[components[1]] + [components[2]]
        else:
            vulnObj = obj[components[1]]
            if components[3] not in vulnObj.keys():
                vulnObj[components[3]] = []

            if components[1] == 'RENT':
                vulnObj[components[3]] = vulnObj[components[3]] + [components[2]]
            else:
                vulnObj[components[3]] = vulnObj[components[3]] + [int(components[2].rstrip())]

            obj[components[1]] = vulnObj

        data[components[0]]
        cur = cur + 1

    with open(output_File, 'w') as fp:
        json.dump(data, fp, sort_keys = True, indent = 4)

if __name__ == "__main__":
    main(ParseArgs())
