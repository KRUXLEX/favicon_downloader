#!/usr/bin/python3

import sys
import bs4
import requests
from urllib.parse import urlparse, urlunparse

def find_icon(domain):
    resp = requests.get("http://{}/".format(domain))
    page = bs4.BeautifulSoup(resp.text, 'html.parser')
    res = "http://{}/favicon.ico".format(domain)
    icons = [e for e in page.find_all(name='link') if 'icon' in e.attrs.get('rel')]
    if icons:
        res = icons[0].attrs.get('href')
    url = urlparse(res, scheme='http')
    if not url.netloc:
        res = urlunparse((url.scheme, domain, url.path, '', '', ''))
    return res

def download(domain, icon_url):
    i = icon_url.find('.', len(icon_url)-4)
    if i>=0:
        ext = icon_url[i+1:]
    else:
        ext = 'ico'
    fname = "{}.{}".format(domain, ext)
    resp = requests.get(icon_url)
    with open(fname, 'wb') as out:
        out.write(resp.content)

if __name__=='__main__':
    if len(sys.argv)<2:
        print('Need txt file!')
        sys.exit()
    sites = sys.argv[1]
    with open(sites, 'r') as sites:
        for d in sites.readlines():
            d = d.strip()
            download(d, find_icon(d))
