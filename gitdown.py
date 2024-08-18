import requests
import os
import rich.progress

def makefile(download_url, rel, fullpath, progress, status):
    r = requests.get(download_url, stream=True)
    with open(os.path.relpath(fullpath, os.path.dirname(rel)), 'wb') as f:
        for received in r.iter_content(50000):  # Chunk size of 50000 bytes
            f.write(received)
            progress.update(status, advance=len(received))

def urlmaker(url):
    a = url.split('/')
    newurl = f'https://api.github.com/repos/{a[3]}/{a[4]}/contents/{"/".join(a[7:])}'
    os.makedirs(a[-1], exist_ok=True)
    return newurl, '/'.join(a[7:])

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

def main():
    url = "https://github.com/Clutchnp/myvim/tree/main/lua"
    newurl, rel = urlmaker(url)
    upperfunc(newurl, rel)
    print('done')

if __name__ == "__main__":
    main()

