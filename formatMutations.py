import json
import sys

def getMutations(input_file):
    with open(input_file) as data_file:
        data = json.load(data_file)
    stringToReturn = ""
    i = 0
    for j in range(len(data[0]["alignedGeneSequences"])):
        for n in range(data[0]["alignedGeneSequences"][j]["lastAA"] - data[0]["alignedGeneSequences"][0]["firstAA"]):
            refAALine = data[0]["alignedGeneSequences"][j]["prettyPairwise"]["refAALine"][n].strip()
            positionLine = data[0]["alignedGeneSequences"][j]["prettyPairwise"]["positionLine"][n].strip()
            mutationLine = data[0]["alignedGeneSequences"][j]["prettyPairwise"]["mutationLine"][n].strip()
            geneName = data[0]["alignedGeneSequences"][j]["gene"]["name"].strip()
            if(mutationLine != '-'):
                if(i == 0):
                    stringToReturn += geneName + ":" + refAALine + positionLine + mutationLine
                    #print "%s:%s%s%s" % (geneName,refAALine,positionLine,mutationLine),
                else:
                    stringToReturn += "+" + geneName + ":" + refAALine + positionLine + mutationLine
                    #print "+ %s:%s%s%s" % (geneName,refAALine,positionLine,mutationLine),
                i += 1
    return stringToReturn

if __name__ == "__main__":
   getMutations(sys.argv[1])
