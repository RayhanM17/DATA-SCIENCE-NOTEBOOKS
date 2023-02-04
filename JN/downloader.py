import urllib.request
import json
import time
import math
import threading
from tqdm import tqdm
from datetime import datetime
import pandas as pd
import numpy as np
import concurrent.futures

# Base URL for this endpoint. Add filters, column selection, and sort order to this.
baseUrl = "https://www.fema.gov/api/open/v1/IndividualsAndHouseholdsProgramValidRegistrations?$filter" \
          "=disasterNumber%20eq%20%274680%27&$select" \
          "=incidentType,disasterNumber,ihpAmount,floodDamageAmount,foundationDamageAmount,roofDamageAmount"

top = 1000  # number of records to get per call
skip = 0  # number of records to skip

# Return 1 record with your criteria to get total record count
webUrl = urllib.request.urlopen(baseUrl + "&$inlinecount=allpages&$select=id&$top=1")
result = webUrl.read()
jsonData = json.loads(result.decode())

# calculate the number of calls we will need to get all of our data (using the maximum of 1000)
recCount = jsonData['metadata']['count']
loopNum = math.ceil(recCount / top)

# ensure that only one thread can write to the file at a time
lock = threading.Lock()

start = time.perf_counter()

# send some logging info to the console so we know what is happening
print("START " + str(datetime.now()) + ", " + str(recCount) + " records, " + str(top) + " returned per call, " + str(
    loopNum) + " iterations needed.")


# Create empty dataframe & csv file
df = pd.DataFrame(columns=["incidentType", "disasterNumber", "ihpAmount", "floodDamageAmount", "foundationDamageAmount", "roofDamageAmount"])
df.to_csv('HURRICANE_NICOLE.csv', index=False, mode='w')



def download_data(req_url):
    # By default data is returned as a CSV, if you want to begin working with and manipulating the CSV,
    file = urllib.request.urlopen(baseUrl + "&$format=csv" + "&$skip=" + str(skip) + "&$top=" + str(top))
    temp_df = pd.read_csv(file, skiprows=1)
    with lock:
        temp_df.to_csv('HURRICANE_NICOLE.csv', mode='a', index=False)

with concurrent.futures.ThreadPoolExecutor() as executor:
    urls_array = np.array([f"{baseUrl}&$format=csv&$skip={i * top}&$top={top}" for i in range(loopNum)])

    for _ in tqdm(executor.map(download_data, urls_array), total=len(urls_array)):
        pass

finish = time.perf_counter()
print(f'Finished in {round(finish - start, 2)} seconds')