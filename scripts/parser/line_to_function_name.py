import sys
import csv


class LineToFunctionName:
    function_lines_file_path='../data/function_lines.txt'
    def get_function_name(self, filename, lineno):
        with open(self.function_lines_file_path, 'r') as csv_file:
            reader = csv.reader(csv_file,delimiter=';')
            for row in reader:
                if((row[0] == filename or row[0] == filename.replace('0x','./0x')) and int(lineno) in range(int(row[2]), int(row[3])+1)):
                    return row[1]

#filename=sys.argv[1]
#lineno=sys.argv[2]
#print(get_function_name(filename, lineno))
