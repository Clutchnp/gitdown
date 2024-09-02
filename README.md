This tool allows users to download specific directories from github repositories using the cli easily 


> [!Big Change]
> the commit #932a6b introduces a new way to handle api requests
> before no. of api requests were depandant on the directories traversed("because of recursion and chances of hitting rate limit were higher")
> This changed in this commit which now uses only 2 api requests for non truncated github responeses. Truncated responses(seen in largo repos) are still wip 
# Installation 
## For Linux Systems:

1. Install python-virtualenv and pyinstaller as you see fit.
    For arch-based systems  `yay -S pyinstaller python-virtualenv` (replace with appropriate aur helper)
2. Clone the repo using ```git clone https://github.com/Clutchnp/gitdown.git```
3. use the install script or install manually 
4. Enjoy
## For Windows Systems

1. Install python
2. Run install.bat
3. enjoy 
# Usage 

if you didn't install then ```python3 gitdown.py {link} {newname}```
if you did install then ``` gitdown {link} {newname}```
