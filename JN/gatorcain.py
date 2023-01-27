import numpy as np
import concurrent.futures
import requests
import math
import time
from datetime import datetime
import json

start = time.perf_counter()

session = requests.session()

baseUrl = "https://www.fema.gov/api/open/v1/IndividualsAndHouseholdsProgramValidRegistrations?$filter=damagedStateAbbreviation%20eq%20%27FL%27%20and%20incidentType%20eq%20%27Hurricane%27&$select=incidentType,disasterNumber,ihpAmount,floodDamageAmount,foundationDamageAmount,roofDamageAmount&$orderby=declarationDate"

top = 1000  # number of records to get per call
skip = 0  # number of records to skip

jsonData = session.get(baseUrl + "&$inlinecount=allpages&$select=id&$top=1").json()

recCount = jsonData['metadata']['count']
loopNum = math.ceil(recCount / top)

print("START " + str(datetime.now()) + ", " + str(recCount) + " records, " + str(top) + " returned per call, " + str(
    loopNum) + " iterations needed.")

insurance_data = open("insurranceClaims.json", "a")

insurance_data.write('{"insuranceClaims":[')

def download_data(req_url):
    response = session.get(req_url)

    if response.status_code == 200:
        print(round(int(req_url[req_url.index("skip=")+5:req_url.rindex("&")])/recCount, 4))
        return response.json()

    else:
        print(f"Error {response.status_code}: {response.text}")
        return

with concurrent.futures.ThreadPoolExecutor() as executor:
    urls_array = np.array([f"{baseUrl}&$metadata=off&$format=jsona&$skip={i*top}&$top={top}" for i in range(loopNum)])

    results = executor.map(download_data, urls_array)

    for i, f in results:
        if i == (loopNum - 1):
            # on the last so terminate the single JSON object
            insurance_data.write(str(f[1:-1], 'utf-8') + "]}")
        else:
            insurance_data.write(str(f[1:-1], 'utf-8') + ",")

insurance_data.close()

finish = time.perf_counter()

inFile = open("output2.json", "r")
my_data = json.load(inFile)
print("END " + str(datetime.now()) + ", " + str(len(my_data['insuranceClaims'])) + " records in file")
inFile.close()

print(f'Finished in {round(finish - start, 2)} seconds')