import requests
import os
import rich.progress
import sys
import argparse

def arghelper():
    parser = argparse.ArgumentParser(description= "Download Github Directories from command line easily!!")
    parser.add_argument('[link]', type=str,help='link of the HTML page of the directory to download (just copy it from the URL bar, adding directory to https clone link won’t work)')
    parser.add_argument('[newname]', type=str,nargs='?',help='lets you specify the name of folder being downloaded')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    print(vars(args))
    return vars(args)  

def makefile(download_url, rel, fullpath, progress, status):
    r = requests.get(download_url, stream=True)
    with open(os.path.relpath(fullpath, os.path.dirname(rel)), 'wb') as f:
        for received in r.iter_content(50000):  # Chunk size of 50000 bytes
            f.write(received)
            progress.update(status, advance=len(received))

def urlmaker(url):
    a = url.split('/')
    newurl = f'https://api.github.com/repos/{a[3]}/{a[4]}/contents/{"/".join(a[7:])}'
    name = [x for x in a if x][-1]
    os.makedirs(name, exist_ok=True)
    return newurl, '/'.join(a[7:]), name

def get_size(newurl):
    total_size = 0
    request = requests.get(newurl)
    jsonresponse = request.json()
    for x in jsonresponse:
        if x['type'] == 'dir':
            total_size += get_size(x['url'])
        else:
            total_size += x['size']
    return total_size

def innerfunc(newurl, rel, progress, status):
    request = requests.get(newurl)
    jsonresponse = request.json()
    for x in jsonresponse:
        if x['type'] == 'dir':
            os.makedirs(os.path.relpath(x['path'], os.path.dirname(rel)), exist_ok=True)
            innerfunc(x['url'], rel, progress, status)
        else:
            makefile(x["download_url"], rel, x['path'], progress, status)

def upperfunc(newurl, rel):
    total_size = get_size(newurl)
    progress = rich.progress.Progress()
    status = progress.add_task('Downloading', total=total_size)
    progress.start()
    innerfunc(newurl, rel, progress, status)
    progress.stop()

def rename(orignal_name,new_name): 
    os.rename(orignal_name,new_name)

def main():
    arg = arghelper()
    url = arg['[link]']
    newurl, rel, orignal_name = urlmaker(url)
    upperfunc(newurl, rel)
    if arg['[newname]'] :
        rename(orignal_name,arg['[newname]'])
    print('done')
    
if __name__ == "__main__":
    main()

