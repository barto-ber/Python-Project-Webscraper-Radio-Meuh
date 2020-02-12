from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re

SONGS_URL = "http://www.radiomeuh.com/rtdata/tracks10.xml"
PARSE_REGEXP = r"([\d:]{8}|\.\.\.)+<.{2,4}>([^<]+)-([^<]+)<.{2,4}>([^<]+)"


class Song:
    """ Class probably would be more useful than pandas here """

    def __init__(self):
        """ Describing function what parameters song can have and what are defaults """
        self.last_aired = None
        self.author = None
        self.name = None
        self.album = None

    def __str__(self):
        """ This function tells python what to print when you do print(song)"""
        return f"Song {self.name}. Album {self.album}. Author {self.author}. Last aired {self.last_aired}"


def simple_get(url):
    """
   NOTE: Copied the function from here https://realpython.com/python-web-scraping-practical-introduction/
   Attempts to get the content at `url` by making an HTTP GET request.
   If the content-type of response is some kind of HTML/XML, return the
   text content, otherwise return None.
   """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
   NOTE: Copied the function from here https://realpython.com/python-web-scraping-practical-introduction/
   Returns True if the response seems to be HTML, False otherwise.
   """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None)


def log_error(e):
    """
   NOTE: Copied the function from here https://realpython.com/python-web-scraping-practical-introduction/
   It is always a good idea to log errors.
   This function just prints them, but you can
   make it do anything.
   """
    print(e)


def parse_songs(raw_html):
    # If there is nothing to parse - return None
    if raw_html is None:
        print("HTML is empty")
        return None

    # Get All Cell and TextCell values
    html = BeautifulSoup(raw_html, 'html.parser')
    table = html.findAll(True, {'class': ['Cell', "TextCell"]})

    # List to push all the songs later
    all_songs = list()

    for line in table:
        # find all groups by regexp. Use to play with regexp https://regex101.com/
        grs = re.findall(PARSE_REGEXP, str(line))
        if not grs:
            print("Can't parse the line, skipping...", line)
            continue

        # Deleting all spaces in the begining and end f the lines
        grs = [x.strip() for x in grs[0]]

        # If the name/album/author ois missing - skip it.
        if len(grs) != 4:
            print("Not enough data for ", str(line))
            print(grs)
            continue
        # Create a new Song and add params to it according to grs. grs is a list with 4 elements.
        song = Song()
        song.last_aired, song.author, song.name, song.album = grs
        print(song)

    return all_songs


def main():
    # Download HTML (actually XML) file
    html = simple_get(SONGS_URL)

    # Parse the file
    songs = parse_songs(html)

    for song in songs:
        print(song)


if __name__ == "__main__":
    main()
