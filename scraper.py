from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import pdb
import re
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = False


ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]

# Main function
#browser = webdriver.Chrome(executable_path='/home/gideon/YEDA/chromedriver')
browser = webdriver.Firefox()
def search_using_selenium(query:str):

    url = 'https://www.google.com/search?q=' + query
    browser.get(url)
    results = browser.find_elements_by_css_selector('div.g')
    links = []
    href = []
    for i in results:
        links.append(i.find_element_by_tag_name("a"))
    for i in links:
        href.append(i.get_attribute("href"))

    return (href)

def parse_search_results_links(response,search_engine:str):
    if search_engine == "google":
        urllist = re.findall(r"""<\s*a\s*href=["']([^=]+)["']""", response)
        return urllist
    elif search_engine == "duckduckgo":
        urllist=[]
        soup = BeautifulSoup(response, 'html.parser')
        results = soup.find_all('a', attrs={'class': 'result__a'}, href=True)
        #pdb.set_trace()
        for link in results:
            url = link['href']
            o = urllib.parse.urlparse(url)
            d = urllib.parse.parse_qs(o.query)
            urllist.append(d['uddg'][0])
            pdb.set_trace()


    else:
        raise ValueError('Search engine parameter should be either google or duckduckgo')

def search_in_search_engine(query:str,search_engine:str):
    # Retrieve latest proxies
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent',ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    # Save proxies in the array
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
            'ip':   row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
        })

    # Choose a random proxy
    proxy_index = random_proxy()
    proxy = proxies[proxy_index]

    for n in range(1, 10):
        query= re.sub(r"\s+", '+', query)
        if search_engine=="google":
            url = 'https://www.google.com/search?q=' + query
        elif search_engine=="duckduckgo":
            url = 'https://www.duckduckgo.com/html/?q='+query

        else:
            raise ValueError('Search engine parameter should be either google or duckduckgo')
        print(url)

        req = Request(url)
        #req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')
        #req.set_proxy('192.241.245.207:1080', 'http')




        # Every 10 requests, generate a new proxy
        if n % 10 == 0:
            proxy_index = random_proxy()
            proxy = proxies[proxy_index]

        # Make the call
        try:
            req.add_header('User-Agent', 'Mozilla/5.0')
            response = urlopen(req).read().decode('utf8')
            #print(my_ip)
            urllist = parse_search_results_links(response,search_engine)
            return (urllist)
        except Exception as e:
            print(str(e))
            del proxies[proxy_index]
            print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
            proxy_index = random_proxy()
            proxy = proxies[proxy_index]


# Retrieve a random index proxy (we need the index to delete it if not working)
def random_proxy():
    return random.randint(0, len(proxies) - 1)

if __name__ == '__main__':
    main()