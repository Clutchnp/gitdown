import requests
import os
import rich.progress
import sys
import argparse

def arghelper():
    parser = argparse.ArgumentParser(description= "Download Github Directories from command line easily!!")
    parser.add_argument('link', type=str,help='link of the HTML page of the directory to download (just copy it from the URL bar, adding directory to https clone link won’t work)')
    parser.add_argument('newname', type=str,nargs='?',help='lets you specify the name of folder being downloaded')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    return vars(args)  

def responder(url): 
    piece = url.split("/")
    repo = piece[3]+"/"+piece[4]
    newurl = f"https://api.github.com/repos/{repo}/git/trees/{piece[6]}?recursive=1"
    jsonresponse = requests.get(newurl).json() # Not handling truncated responeses yet but will in future
    name = [x for x in piece if x][-1]
    path = ''.join(piece[7:])
    return jsonresponse,repo,path,piece[6],name
def get_size(json):
    size = 0 
    for x in json['tree']: 
        if x["type"]=="blob":
          size+=x['size']
    return size 

def thejsonresponse(response,path):
     for x in response['tree']:
        if x['path'] == path:
            jsonresponse = requests.get(x["url"]+"?recursive=1").json() 
            return jsonresponse

        else:
            continue
def create_dir(path):
    if path:
        os.makedirs(path,exist_ok=True)

def downplace(json,repo,branch,name,newname,progress,status):
    for x in json["tree"]: 
        if x["type"]=="blob":
         download_url=f"https://raw.githubusercontent.com/{repo}/{branch}/{name}/{x["path"]}"
         file = x["path"]
         r = requests.get(download_url, stream=True)
         create_dir(newname + os.path.dirname(file))
         with open(newname + file, "wb") as f:
              for received in r.iter_content(50000):  # Chunk size of 50000 bytes
                f.write(received)
                progress.update(status, advance=len(received))

def main():
    arg = arghelper()
    url = arg['link']
    response,repo,path,branch,name = responder(url)
    thejson = thejsonresponse(response,path) 
    size = get_size(thejson)
    progress = rich.progress.Progress()
    status = progress.add_task('Downloading', total=size)
    progress.start()
    if arg['newname'] :
        downplace(thejson,repo,branch,name,arg["newname"]+"/",progress,status)
    else :
        downplace(thejson,repo,branch,name,name+"/",progress,status)
    progress.stop()
if __name__ == "__main__":
    main()

