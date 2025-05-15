# CS551P Assignment 3

### What is this?
This `README.md` will show the files about CS551P Assignment 3.

# How to run (local version on Codio)
```bash
source .venv/bin/activate
python emissions.py
```
then you can visit the page by this url: https://buenossonic-henrydemo-5000.codio-box.uk/

# Solutions for some common questions:
### Get python version 3.10.7
When open your codio link for this Assignment, firstly checking the python version is necessary. Try with this code:
```bash 
python --version
```
If your python version is 2.7.17, you should download 3.10.7 version. Type the following command:
```bash
pyenv install 3.10.7
```
If you meet an error like '*python-build: definition not found: 3.10.7*', then you should upload your pyenv. Try this:
```bash
cd ~/.pyenv
git pull
```
Then, go back to your working directory:
```bash
cd -
```
Now you should be able to download the version 3.10.7:
```bash
pyenv install 3.10.7
```
After downloading, remember to check the version again. If it's still 2.7.17, try this command:
```bash
pyenv rehash
```

### Download files from github repository
I have created a repository on github for this Assignment, you can download files from it. You can use this commend to download.
```bash
git clone https://github.com/Thorki-Su/CS551P_Assignment_3.git
```
This will download all the files into your codio as a new folder '*CS551P_Assignment_3*'. To make edits and commits easier, please move all files out of the folder.

# Usage of Templates
'404.html' is for the 404 error.   
'500.html' is for the 500 error.   
'main.html' is the main template for other pages.   
'homepage.html' is for the homepage.   
'country.html' is for the country detail pages.   

#Name in the git log
'Thorki Su' is the username of Peiheng Su in github.