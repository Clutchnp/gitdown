import requests
import os 
from urllib.request import urlretrieve
# expects a general url from github 
# for eg https://github.com/Clutchnp/myvim/lua/core

def makefile(download_url,path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    urlretrieve(download_url,path)

def  urlmaker(url):
    a=url.split('/')
    newurl = f'https://api.github.com/repos/{a[3]}/{a[4]}/contents/{'/'.join(a[7:])}'
    return newurl
def innerfunc(object):
    if object['type'] == 'dir':
        urlmaker(object['html_url'])

def upperfunc(newurl):
    request = requests.get(newurl)
    jsonresponse = request.json()
    for x in jsonresponse:
        if x['type'] == 'dir':
            return upperfunc(x['url'])
        else :
          makefile(x["download_url"],x["path"])


if __name__ == "__main__":
    url = "https://github.com/Clutchnp/myvim/lua/core"
    a = urlmaker(url)
    upperfunc(a)
    print('done')
    



    
