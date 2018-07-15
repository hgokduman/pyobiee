from pyobiee import pyOBIEE
from multiprocessing import Pool
import os
import time
import json

login = json.load(open('login.json'))
obiee = pyOBIEE(login['wsdlURL'], login['username'], login['password'])
obiee.Login()
obiee.SetDelimiters(fieldDelimiter=chr(7))

def runSQL(fileName):
    print(f"Processing {fileName}")
    obiee.Get(f"{fileName}", fileName='output/' + os.path.basename(fileName)[:-4] + '.csv')
    print(f"Done processing {fileName}")

if __name__ == '__main__':
    pool = Pool(processes=2)
    sqlFolder = 'sql'
    files = [sqlFolder + '/' + f for f in os.listdir(sqlFolder)]
    poolMap = pool.map_async(runSQL, files)
    print("Now we will wait...")
    while poolMap.ready() == False:
        print("Still working")
        time.sleep(1)
    print("Ready!")