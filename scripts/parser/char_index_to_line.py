import re
import sys

class CharIndexToLine:

    function_lines = {} # Empty dictionary
    char_range_per_line={} # Empty dictionary

    def get_char_range_per_line(self, filename, char_index):
        file = open(filename, "r")
        stringList = file.readlines()
        i=0
        lineno=1
        for line in stringList:
            start=i
            i=i+len(line)+1
            self.char_range_per_line[lineno]=(range(start,i))
            lineno=lineno+1

        for lineno in self.char_range_per_line.keys():
            if (int(char_index) in self.char_range_per_line[lineno]):
                return lineno
        #print(self.char_range_per_line)

# obj = CharIndexToLine()
# filename=sys.argv[1]
# char_index=sys.argv[2]
# print(obj.get_char_range_per_line(filename, char_index))
