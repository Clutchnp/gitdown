import requests
import os 
#from urllib.request import urlretrieve
import rich.progress 
import pprint
# expects a general url from github 
# for eg https://github.com/Clutchnp/myvim/lua/core

all_size = 0
def makefile(download_url,rel,fullpath,size):
    # it maybe can get deprecated according to the documentation so creating a cutom implementation using requests 
    #urlretrieve(download_url,os.path.relpath(fullpath,os.path.dirname(rel)))
    r = requests.get(download_url,stream=True)
# Use Progress context manager
    with rich.progress.Progress() as progress:
        download_task = progress.add_task("Downloading....", total=all_size)
        
        with open(os.path.relpath(fullpath, os.path.dirname(rel)), 'wb') as f:
            for received in r.iter_content(50000):  # Chunk size of 50000 bytes
                f.write(received)
                progress.advance(download_task, advance=size)

def  urlmaker(url):
    a=url.split('/')
    newurl = f'https://api.github.com/repos/{a[3]}/{a[4]}/contents/{'/'.join(a[7:])}'
    os.makedirs(a[-1], exist_ok = True)
    return newurl,'/'.join(a[7:])

def get_size(newurl):
    global all_size
    request = requests.get(newurl)
    jsonresponse = request.json()
    for x in jsonresponse:
        if x['type'] == 'dir':
            get_size(x['url'])
        else:
            all_size+=x['size']

def upperfunc(newurl,rel):
    get_size(newurl) 
    innerfunc(newurl, rel)
  
def innerfunc(newurl,rel):
    request = requests.get(newurl)
    jsonresponse = request.json()
    for x in jsonresponse:
            if x['type'] == 'dir':
                os.makedirs(os.path.relpath(x['path'],os.path.dirname(rel)), exist_ok=True)
                innerfunc(x['url'],rel)
            else :
                makefile(x["download_url"],rel,x['path'],x['size'])

def main():
    url = "https://github.com/Clutchnp/myvim/tree/main/lua"
    a,rel= urlmaker(url)
    upperfunc(a,rel)
    print('done')
if __name__ == "__main__":
    main()
