"""
Name: Bria Weisblat
Date: 09/18/24
Assignment: Assignment # 2
Due Date: 09/25/24
About this project: This program extracts information from BGP routing tables and returns
two output files. The first output file, top10.txt, contains the information of the top
10 ASes in terms of the number of neighbors. The second output file, neighbor_count.txt,
lists the neighbor count for all ASes in the descending order based on the number of
neighbors they have.
Assumptions: Assumes that the input is a BGP dump file taken in as a command line argument
All work below was performed solely by Bria Weisblat
"""

# Imports
import sys
import re
from collections import OrderedDict

# my functions
def update_dict(input_dict, key):
    if key not in input_dict:
        input_dict[key] = []

# arguments are located in sys.argv[n]
filename = sys.argv[1]

# open the file
input_file = open(filename, 'r')

# create an empty dict to hold all the ASes and their neighbors
AS_dict = {}

# loop through every line in the file
for line in input_file:
    # split the line
    fields = line.split('|') # this is a list!
    # remove ASSET from the 7th field
    trimmed_7th_field = re.sub(r'\[.*?\]', '', fields[6]).strip()
    # split the 7th field into ASes
    AS_list = trimmed_7th_field.split(' ') # this is also a list

    # loop through every element in the list
    index = 0
    for AS in AS_list:
        # check if dictionary contains current AS, if not, update
        if int(AS) not in AS_dict:
            AS_dict[int(AS)] = set()
        # read the neighbor BEFORE the current one, unless index == 0
        if index != 0:
            neighbor_pre = AS_list[index-1]
            # don't add if equal to current AS
            if neighbor_pre != AS:
                AS_dict[int(AS)].add(int(neighbor_pre))
        # read the neighbor AFTER the current one, unless index == length-1
        if index != len(AS_list)-1:
            neighbor_next = AS_list[index+1]
            # don't add if equal to current AS
            if neighbor_next != AS:
                AS_dict[int(AS)].add(int(neighbor_next))
        index+=1

# sort the dict by length of the sets
sorted_AS_items = sorted(AS_dict.items(), key=lambda item: (len(item[1]), -item[0]), reverse=True)
sorted_AS_dict = OrderedDict(sorted_AS_items)
sorted_AS_list = list(sorted_AS_dict.items())
top_ten_ASes = list(sorted_AS_dict.items())[:10]

# format outputs for top10
with open(f"top10_{filename}.txt", 'w') as out:
    # loop through the dict
    for key, value in top_ten_ASes:
        # print the AS
        out.write(str(key) + ': ')
        # find the number of neighbors and print
        out.write(str(len(value)) + ' ')
        # create list of integers
        neighbor_list = list(value)
        neighbor_nums = [int(num) for num in neighbor_list]
        neighbor_nums.sort()
        # loop through list
        for neighbor_as in neighbor_nums:
            out.write(str(neighbor_as))
            # only output the pipe if we're not at the end
            if neighbor_as != neighbor_nums[len(neighbor_nums)-1]:
                out.write('|')
        # start new line
        out.write('\n')

# format outputs for neighbor count
with open(f"neighbor_count_{filename}.txt", 'w') as out2:
    # loop through the sorted dict
    for key, value in sorted_AS_list:
        # print key
        out2.write(str(key) + ': ')
        # print number of neighbors
        out2.write(str(len(value)) + '\n')