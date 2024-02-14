import logging
import time,re,json
from aiohttp import ClientSession
import aiohttp
from bs4 import BeautifulSoup
import random
import asyncio
import json
import requests
import unicodedata
import urllib3

def random_ip():
  ips = ['46.227.123.', '37.110.212.', '46.255.69.', '62.209.128.', '37.110.214.', '31.135.209.', '37.110.213.'];
  prefix = random.choice(ips)
  return prefix + str(random.randint(1, 255))

class Downloads():
    async def instagram(url):
        result = []
        RES = {}
        data = {'q': url, 'vt': 'home'}
        headers = {
        'origin': 'https://snapinsta.io',
        'referer': 'https://snapinsta.io/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'X-Forwarded-For': random_ip(),
        'X-Client-IP': random_ip(),
        'X-Real-IP': random_ip(),
        'X-Forwarded-Host': 'snapinsta.io'
        }
        base_url = 'https://snapinsta.io/api/ajaxSearch'
        async with ClientSession() as session:
            async with session.post(base_url, data=data, headers=headers) as response:
                # encoded_text = unicodedata.normalize('NFKD', await response.text()).encode('ascii', 'ignore')
                # soup = BeautifulSoup(encoded_text, 'html.parser')
                jsonn = json.loads(await response.text())
                print(jsonn)
                if jsonn['status'] == 'ok':
                    print(jsonn)
                    data = jsonn['data']
                    soup = BeautifulSoup(data, 'html.parser')
                    for i in soup.find_all('div', class_='download-items__btn'):
                        url = i.find('a')['href']
                        result.append({'url': url})
                    RES = {'status': True, 'result': result}
                else:
                    RES = {'status': False, 'result': 'Error'}
                print(RES['result'][0])
                #print(json.dumps(RES, ensure_ascii=False, indent=4))
                

async def insta():
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(Downloads.instagram("https://www.instagram.com/reel/Cz3sdpkIqww/?igshid=MTc4MmM1YmI2Ng=="))
insta()