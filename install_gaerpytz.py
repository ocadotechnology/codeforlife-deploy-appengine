import StringIO
import urllib2
import zipfile

import requests
from bs4 import BeautifulSoup

# Get HTML of the gaerpytz home page
gaerpytz_url = "https://gaerpytz.appspot.com"
gaerpytz_webpage = urllib2.urlopen(gaerpytz_url)
gaerpytz_html = gaerpytz_webpage.read()

# Parse HTML to get the zipfile's download link
soup = BeautifulSoup(gaerpytz_html, "html.parser")
zip_href = soup.find(title="Download the latest build").get("href")
zip_url = gaerpytz_url + zip_href

# Download the zipfile and extract it to the lib folder
request = requests.get(zip_url, stream=True)
zip_file = zipfile.ZipFile(StringIO.StringIO(request.content))
zip_file.extractall("lib")
