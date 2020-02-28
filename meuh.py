import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import csv
import time
from datetime import date
from collections import defaultdict
import threading
from threading import Thread



def get_tracks():
    # Getting current time
    t = time.localtime()
    current_time = time.strftime("%H:%M", t)
    print("* Script run at " + current_time + ":")

    today_get = date.today()
    today = today_get.strftime("%d/%m/%Y")
    radio_url = 'http://www.radiomeuh.com/rtdata/tracks10.xml'
    html_text = requests.get(radio_url).text
    soup = BeautifulSoup(html_text, 'xml')
    # print(soup)

    data = []

    for string in soup.stripped_strings:
        data.append(repr(string)) # modification delete repr from (repr(string)) but if so we cant more search with re.search L32

    for i in data:
        if "temps restant" in i:
            data.remove(i)

    # Deleting current song which is not complete.
    del data[0:3]

    # print(data)
    # print(type(data[0]))
    # print(data[0])
    tracksdict = {}
    iterdata = iter(data)

    for i in iterdata:
        if (re.search(r'\D\d{2}\D\d{2}\D\d{2}\D', str(i))): #or ("..." in str(o)):
            tracksdict[today+"_"+i] = [next(iterdata,""), next(iterdata,"")]

    # print(tracksdict)

    # # Creating a dataframe from tracksdict{}
    # df = pd.DataFrame.from_dict(data=tracksdict, orient='index', columns=['Song', 'Album'])
    # print(df)

    #for key, value in tracksdict.items():
    #    print(key, '->', value)

    print(" --- Fetching tracks --- ")
    # print("Batch : "+ str(len(tracksdict))+" tracks fetched in last batch (should always be 10)")
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
    # Getting the dictionary from build_archive(), naming it differently to be able to clear the 'real' one later
    while True:
        archive_for_csv = build_archive()
        minutes = 5
        time.sleep(60 * minutes)
        return archive_for_csv

def append_csv():
    while True:
        minutes = 10
        time.sleep(60 * minutes)
        append_archive = build_csv()
        csv_file = 'tracks.csv'
        with open(csv_file, 'a',  newline='\n', encoding='utf-8') as f:
            for key in append_archive.keys():
                f.write("%s, %s\n" % (key, append_archive[key]))
        print(" --- Copying to CSV! --- ")
        print("Copied Archive to CSV")
        print(" --- Emptying the archive and starting again! --- ")
        return archive.clear()

if __name__ == "__main__":
    t1 = Thread(target = build_csv)
    t2 = Thread(target = append_csv)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    while True:
        pass









# minutes = 15.0
# time.sleep(60 * minutes)
# thread_append_csv = threading.Thread(target=append_csv)
# thread_append_csv.start()
#
# wait_minutes = 10.0
# while True:
#     build_csv()
#     time.sleep(60*wait_minutes)