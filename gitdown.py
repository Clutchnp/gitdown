import requests
import os
import rich.progress
import sys
import argparse

def arghelper():
    parser = argparse.ArgumentParser(description="Download GitHub Directories from the command line easily!")
    parser.add_argument('link', type=str, help='Link of the HTML page of the directory to download (just copy it from the URL bar, adding directory to https clone link won’t work)')
    parser.add_argument('newname', type=str, nargs='?', help='Specify the name of the folder being downloaded')
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    args = parser.parse_args()
    return vars(args)
def file(repo,path,branch,name):
    download_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"
    # Download the file
    try:
        r = requests.get(download_url, stream=True)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        sys.exit(1)
    
    progress = rich.progress.Progress()
    status = progress.add_task('Downloading', total=int(requests.get(download_url, stream=True).headers['Content-length']))
    with progress:
    # Write the file in chunks
        with open(name, "wb") as f:
            for chunk in r.iter_content(50000):  # Chunk size of 50000 bytes
                if chunk:
                    f.write(chunk)
                    progress.update(status, advance=len(chunk))
def responder(url):
    piece = url.split("/")
    piece = [x for x in piece if x]
    repo = f"{piece[2]}/{piece[3]}"
    if len(piece) == 4:
        print("Branch not provided, assuming main branch") 
        piece += ['tree','main']
    content_type = piece[4]
    branch = piece[5]
    name = piece[-1]
    path = '/'.join(piece[6:])
    if content_type == "tree":
        newurl = f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"
        try:
            response = requests.get(newurl)
            response.raise_for_status()  # Ensure we catch any HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from GitHub API: {e}")
            sys.exit(1)
        
        jsonresponse = response.json()
    else:
        jsonresponse = None
    
    return jsonresponse, repo, path, branch,content_type, name

def get_size(json):
    size = sum(x['size'] for x in json['tree'] if x['type'] == 'blob')
    return size

def thejsonresponse(response, path):
    if path == "":
        try:
            jsonresponse = requests.get(response['url'] + "?recursive=1")
            jsonresponse.raise_for_status()
            return jsonresponse.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching file tree: {e}")
            sys.exit(1)
    else: 
        for x in response['tree']:
            if x['path'] == path:
                try:
                    jsonresponse = requests.get(x['url'] + "?recursive=1")
                    jsonresponse.raise_for_status()
                    return jsonresponse.json()
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching file tree: {e}")
                    sys.exit(1)
    return None

def create_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def downplace(json, repo, branch,path,name, newname, progress, status):
    
    for x in json["tree"]:
        if x["type"] == "blob":
            download_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}/{x['path']}"
            file_path = x['path']
            
            # Download the file
            try:
                r = requests.get(download_url, stream=True)
                r.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")
                continue
            
            # Create the necessary directories
            if newname == f'{name}/' and path =='':
              newname = repo.split('/')[-1]+ '/'
            create_dir(newname + os.path.dirname(file_path))
            # Write the file in chunks
            with open(newname + file_path, "wb") as f:
                for chunk in r.iter_content(50000):  # Chunk size of 50000 bytes
                    if chunk:
                        f.write(chunk)
                        progress.update(status, advance=len(chunk))

def main():
    arg = arghelper()
    url = arg['link']
    response, repo, path, branch,content_type, name = responder(url)
    if content_type == "tree":
        thejson = thejsonresponse(response, path)
        if thejson is None:
            print("No matching directory found in the repository.Response might be truncated or link might be wrong")
            sys.exit(1)
        
        size = get_size(thejson)
        
        progress = rich.progress.Progress()
        status = progress.add_task('Downloading', total=size)
        
        with progress:
            if arg['newname']:
                downplace(thejson, repo, branch, path,name, arg['newname'] + "/", progress, status)
            else:
                downplace(thejson, repo, branch, path,name, name + "/", progress, status)
    elif content_type == "blob":
        if arg['newname']:
            file(repo,path,branch,arg['newname'])
        else:
            file(repo,path,branch,name)
if __name__ == "__main__":
    main()
