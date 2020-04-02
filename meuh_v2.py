'''Due to changes in radiomeuh website there is no more acces to 10 last played titles, so the code changed'''
import requests
from bs4 import BeautifulSoup

radio_url = 'https://jazzradio.net/playlist/'
html_text = requests.get(radio_url).text
soup = BeautifulSoup(html_text, 'xml')
# print(soup.text)
for artist in soup.find_all('playlist'):
    print(artist.text)
else:
    print('nonono')


# from selenium.webdriver import Firefox
# from selenium.webdriver.firefox.options import Options
# opts = Options()
# opts.headless = True
# browser = Firefox(options=opts)
# browser.get('http://www.radiomeuh.com')
# print ("Headless Firefox Initialized")
#
#
# tracklist = []
#
# tracklist_element = browser.find_elements_by_id("track_list")
# print(tracklist_element.text)
# for element in tracklist_element:
#     print("loaded, idk why I can't get rid of these 3 lines")
#
# tracks = browser.find_elements_by_class_name("artist")
# for track in tracks:
#     print(track.text)
#     tracklist.append(track.text)
# print(tracklist)

# a_elements = []
#
# content_blocks = browser.find_elements_by_tag_name("artist")
# print(content_blocks)

# for block in content_blocks:
# 	# print (block)
# 	elements = block.find_elements_by_tag_name('td class-"Cell"')
# 	for el in elements:
# 		a_elements.append(el)
#
# print(a_elements)

# print('DONE')
#
# browser.close()
# quit()