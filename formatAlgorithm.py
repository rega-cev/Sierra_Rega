import json
import itertools
import sys
from drugs import getAllDrugs, getEmptyDrugDict


#input_file = '/Users/ewout/Documents/Kristof/Sierra/sierra_new/output_protease.json'

def generateCSVHeader():
    #Print header of csv file with predefined values
    ALLDrugs = getAllDrugs()
    stringToReturn = ""
    stringToReturn += "id,"
    for i in range(len(ALLDrugs)):
        stringToReturn += ALLDrugs[i] + "_SIR" + ","
        #ALLDrugs[i] + "_level" + "," +
        #ALLDrugs[i] + "_score" + ","
    stringToReturn += "\n"
    return stringToReturn

def generateCSVLine(seq_name,input_file):
    with open(input_file) as data_file:
        try:
            data = json.load(data_file)
        except Exception as e:
            return seq_name + ","

    #SIR = data[0]["algorithmComparison"][0]["drugScores"][0]["SIR"].strip()
    #algorithm = data[0]["algorithmComparison"][0]["drugScores"][0]["algorithm"].strip()
    #name = data[0]["algorithmComparison"][0]["drugScores"][0]["drug"]["name"].strip()

    # Loop over all the sequences
    for n in range(len(data)):
        empty_dict = getEmptyDrugDict()
        # Print all the drug_SIR, drug_level, drug_score
        # Loop over all the different genes (PR, RT, IN, ...)
        for i in range(len(data[n]["algorithmComparison"])):
            # Loop over each drug within each gene
            for j in range(len(data[n]["algorithmComparison"][i]["drugScores"])) :
                # Replace each [-,-,-] in the dict for each drug that we have in the json result
                if data[n]["algorithmComparison"][i]["drugScores"][j]["algorithm"] == 'REGA':
                    empty_dict[str(data[n]["algorithmComparison"][i]["drugScores"][j]["drug"]["displayAbbr"])] = [str(data[n]["algorithmComparison"][i]["drugScores"][j]["SIR"])]
        return seq_name + "," + ",".join(list(itertools.chain.from_iterable(empty_dict.values())))
