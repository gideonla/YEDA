#Used to make requests
import urllib.request
from bs4 import BeautifulSoup
import pdb
import re



def google_search():
    try:
        url = 'https://www.google.com/search?q=gideon+lapidoth'

        # now, with the below headers, we defined ourselves as a simpleton who is
        # still using internet explorer.
        headers = {}
        headers[
            'User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        respData = resp.read()
        urllist = re.findall(r"""<\s*a\s*href=["']([^=]+)["']""", respData.decode("utf-8"))
        print(urllist)

    except Exception as e:
        print(str(e))

if __name__ == '__main__':
  google_search()