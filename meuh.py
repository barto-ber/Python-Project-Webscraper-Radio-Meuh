
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import csv
import time
from datetime import date

def get_tracks():
    today_get = date.today()
    today = today_get.strftime("%d/%m/%Y")

    vgm_url = 'http://www.radiomeuh.com/rtdata/tracks10.xml'
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'xml')

    data = []

    for string in soup.stripped_strings:
        data.append(repr(string))

    for i in data:
        if "temps restant" in i:
            data.remove(i)

    tracksdict = {}
    iterdata = iter(data)

    for o in iterdata:
        if (re.search('\D\d\d\D\d\d\D\d\d\D', str(o))): #or ("..." in str(o)):
            tracksdict[today+"_"+o.replace("'","")] = [next(iterdata,""), next(iterdata,"")]

    #print(data)
    #print(tracksdict)
    #for key, value in tracksdict.items():
    #    print(key, '->', value)

    print(" --- Fetching tracks --- ")
#    print("Batch : "+ str(len(tracksdict))+" tracks fetched in last batch (should always be 10)")
    return tracksdict


archive = {}
def build_archive():
    #print(archive)
    last_tracks_batch = get_tracks()
    for key, value in last_tracks_batch.items():
        if key not in archive:
            archive[key] = value
    print(" --- Building Archive --- ")
    #print(archive)
    print("Archive size: " +str(len(archive))+" tracks.")
    return archive

def build_csv():
    # Getting current time
    t = time.localtime()
    current_time = time.strftime("%H:%M", t)
    print("* Script run at " + current_time + ":")

    # Getting the dictionary from build_archive(), naming it differently to be able to clear the 'real' one later
    archiveforcsv = build_archive()
    # If it's that time of the day, run the script => basic paste to CSV.
    # The parameter 'a' in open(csv) allows to 'append' to csv, not 'write' the file from scratch everytime
    if current_time >= "18:52" and current_time <= "18:55":
        csv_file = 'tracks.csv'
        with open(csv_file, 'a',  newline='\n', encoding='utf-8') as f:
            for key in archiveforcsv.keys():
                f.write("%s, %s\n" % (key, archiveforcsv[key]))
        print(" --- Copying to CSV ! --- ")
        print("Copied Archive to CSV")
        print("Emptying the archive and starting again.")
    # Clearing the 'real' archive, so it doesn't get too heavy.
        return archive.clear()

# How often does the code runs, in minutes :
minutes=20.0
# Will launch build_csv() every specified interval. This function launches the archive, that launches the "get tracks"
while True:
    build_csv()
    time.sleep(60*minutes)
