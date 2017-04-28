# Uaveragebedgraphs v2.0

import argparse
import os
from array import *

#get arguments from command line
parser = argparse.ArgumentParser(description='Uaveragebedgraphs_args')
parser.add_argument('-o','--output', help='name of output file', required=True, type=str)
parser.add_argument('-f','--list_of_files', help='files to be averaged', required=True, nargs='+', type=str)
args = vars(parser.parse_args())
files = args['list_of_files']
output_file = args['output']

def add (input, newfile):
    done = "no"
    chromosomes_done = []
    while done == "no":

# get current chromosome
        with open(input[0]) as ctrl:
            current_chromosome = ""
            done = "yes"
            for line in ctrl:
                line_split = line.split("\t")
                line_split[3] = line_split[3].replace("\n", "")
                if line_split[0] not in chromosomes_done:
                    chromosomes_done.append(line_split[0])
                    current_chromosome = line_split[0]
                    done = "no"
                    break
            if done == "yes":
                break

# get start and stop for current chromosome
        stop = 0

        for file in input: # go through all files
            with open(file) as f:
                breakyn = "no"
                found = "no" #was chromosome found?

                for line in f:
                    if breakyn == "yes": break # if passed the current chromosome (no need to check the rest of the file)
                    line_split = line.split("\t")

                    if line_split[0] == current_chromosome:
                        if line_split[3] != 0:
                            if line_split[2] > stop:
                                stop = int(line_split[2])
                    elif found == "yes": #if passed chromosome trigger break
                        breakyn = "yes"

        if stop > 0:  #If there were values in that chromosome
            output = array('f', [0] * stop)

#sum up
            for file in input:
                with open(file) as f:
                    breakyn = "no"
                    for line in f:
                        line_split = line.split("\t")
                        if line_split[0] == current_chromosome:
                            if float(line_split[3]) > 0:
                                breakyn = "yes"
                                line_split[3] = line_split[3].replace("\n", "")
                                for o in range(int(line_split[2]) - int(line_split[1])):
                                    coord = o + int(line_split[1])
                                    output[coord] = output[coord] + float(line_split[3])/len(input)
                        elif breakyn == "yes": break

#concatenate entries with same value
            output2 = []
            temp_entry = []
            for x, value in enumerate(output):
                if value != 0:
                    if temp_entry == []:
                        temp_entry = [current_chromosome, x, x + 1, value]
                    elif temp_entry[3] == value:
                        temp_entry[2] += 1
                    elif temp_entry[3] != value:
                        output2.append(temp_entry)
                        temp_entry = [current_chromosome, x, x + 1, value]
                else: temp_entry == []

            if temp_entry != []:
                output2.append(temp_entry)

            with open(newfile, "a") as f:
                for row in output2:
                    f.write(str(row[0]) + "\t" + str(row[1]) + "\t" + str(row[2]) + "\t" + str(row[3]) + "\n")

############################################################################

add(files, output_file)
print("Success :)")
