import collections

PRDrugs = []
PRDrugs.append("IDV/r")
PRDrugs.append("SQV/r")
PRDrugs.append("NFV")
PRDrugs.append("FPV/r")
PRDrugs.append("LPV/r")
PRDrugs.append("ATV/r")
PRDrugs.append("TPV/r")
PRDrugs.append("DRV/r")

#NRTI
RTDrugs = []
RTDrugs.append("AZT")
RTDrugs.append("DDI")
RTDrugs.append("D4T")
RTDrugs.append("3TC")
RTDrugs.append("ABC")
RTDrugs.append("FTC")
RTDrugs.append("TDF")
# NNRTI
RTDrugs.append("NVP")
RTDrugs.append("EFV")
RTDrugs.append("ETR")
RTDrugs.append("RPV")

INIDrugs = []
INIDrugs.append("RAL")
INIDrugs.append("EVG")
INIDrugs.append("DTG")

EIDrugs = []
EIDrugs.append("T20")

def getAllDrugs():
	ALLDrugs = []
	ALLDrugs.extend(PRDrugs)
	ALLDrugs.extend(RTDrugs)
	ALLDrugs.extend(INIDrugs)
	ALLDrugs.extend(EIDrugs)
	return sorted(ALLDrugs)

# Standard Python dict doesn't have ordered items. The OrderedDict from collections does have it
def getEmptyDrugDict():
	return collections.OrderedDict((el,['-']) for el in getAllDrugs())
