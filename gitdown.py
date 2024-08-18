import requests
import os 
from urllib.request import urlretrieve
import rich.progress 
# expects a general url from github 
# for eg https://github.com/Clutchnp/myvim/lua/core


def makefile(download_url,rel,fullpath):
    # it maybe can get deprecated according to the documentation so creating a cutom implementation using requests 
    #urlretrieve(download_url,os.path.relpath(fullpath,os.path.dirname(rel)))
    r = requests.get(download_url,stream=True)
    total = int(r.headers.get('content-length', 0)) # get content length http header and return 0 if not recieved)
# Use Progress context manager
    with rich.progress.Progress() as progress:
        download_task = progress.add_task("Downloading....", total=total)
        print ( total )
        
        with open(os.path.relpath(fullpath, os.path.dirname(rel)), 'wb') as f:
            for received in r.iter_content(50000):  # Chunk size of 50000 bytes
                f.write(received)
                progress.update(download_task, advance=len(received))

def  urlmaker(url):
    a=url.split('/')
    newurl = f'https://api.github.com/repos/{a[3]}/{a[4]}/contents/{'/'.join(a[7:])}'
    os.makedirs(a[-1], exist_ok = True)
    return newurl,'/'.join(a[7:])

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

def main():
    url = "https://github.com/Clutchnp/myvim/tree/main/lua"
    a,rel= urlmaker(url)
    upperfunc(a,rel)
    print('done')
if __name__ == "__main__":
    main()
