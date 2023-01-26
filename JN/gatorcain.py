#!/usr/bin/env python3
# Paging example using Python 3. Output in JSON.

import sys
import urllib.request
import json
import math
from datetime import datetime

baseUrl = "https://www.fema.gov/api/open/v1/IndividualsAndHouseholdsProgramValidRegistrations?$filter=damagedStateAbbreviation%20eq%20%27FL%27%20and%20incidentType%20eq%20%27Hurricane%27&$select=incidentType,disasterNumber,ihpAmount,floodDamageAmount,foundationDamageAmount,roofDamageAmount&$orderby=declarationDate"

top = 1000  # number of records to get per call
skip = 0  # number of records to skip

webUrl = urllib.request.urlopen(baseUrl + "&$inlinecount=allpages&$select=id&$top=1")
result = webUrl.read()
jsonData = json.loads(result.decode())

recCount = jsonData['metadata']['count']
loopNum = math.ceil(recCount / top)

print("START " + str(datetime.now()) + ", " + str(recCount) + " records, " + str(top) + " returned per call, " + str(
    loopNum) + " iterations needed.")

outFile = open("output2.json", "a")
outFile.write('{"IndividualsAndHouseholdsProgramValidRegistrations":[')

i = 0
while i < loopNum:
    webUrl = urllib.request.urlopen(baseUrl + "&$metadata=off&$format=jsona&$skip=" + str(skip) + "&$top=" + str(top))
    result = webUrl.read()

    if (i == (loopNum - 1)):
        outFile.write(str(result[1:-1], 'utf-8') + "]}")
    else:
        outFile.write(str(result[1:-1], 'utf-8') + ",")
    i += 1
    skip = i * top

    print("Iteration " + str(i) + " done")

outFile.close()

inFile = open("output2.json", "r")
my_data = json.load(inFile)
print("END " + str(datetime.now()) + ", " + str(len(my_data['femawebdisasterdeclarations'])) + " records in file")
inFile.close()