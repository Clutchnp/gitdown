python -m venv env 

source ./env/bin/activate 

pip install -r requirements.txt 

pyinstaller --onefile --paths=./env/lib/python3.12/site-packages  gitdown.py

cp ./dist/gitdown ~/.local/bin/

echo installed 
