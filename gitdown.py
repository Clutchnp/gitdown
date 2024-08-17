import requests
import os 
from urllib.request import urlretrieve
# expects a general url from github 
# for eg https://github.com/Clutchnp/myvim/lua/core
def makefile(download_url,rel,fullpath):
    urlretrieve(download_url,os.path.relpath(fullpath,os.path.dirname(rel)))

def createdir():
    pass

def  urlmaker(url):
    a=url.split('/')
    newurl = f'https://api.github.com/repos/{a[3]}/{a[4]}/contents/{'/'.join(a[7:])}'
    os.mkdir(a[-1])
    return newurl,'/'.join(a[7:])
def innerfunc(object):
    if object['type'] == 'dir':
        urlmaker(object['html_url'])

def upperfunc(newurl,rel):
    request = requests.get(newurl)
    jsonresponse = request.json()
    for x in jsonresponse:
        if x['type'] == 'dir':
            os.makedirs(os.path.relpath(x['path'],os.path.dirname(rel)), exist_ok=True)
            print(os.path.relpath(x['path'],os.path.dirname(rel)))
            upperfunc(x['url'],rel)
        else :
          makefile(x["download_url"],rel,x['path'])


if __name__ == "__main__":
    url = "https://github.com/Clutchnp/myvim/tree/main/lua"
    a,rel= urlmaker(url)
    upperfunc(a,rel)
    print('done')
    



    
