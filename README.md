# Connect-Long-Beach
Team Bofa's Connect LB project repository for CECS 491

---

## Python Setup/Connecting to the Database  
Install [Python](https://www.python.org/downloads/) if you haven't already; it's reccomended to use the latest version of 3.8 for this project. <b>MAKE SURE</b> to check the box on the python installer that adds it to your PATH variable. Use pip to install pipenv on your computer `pip install pipenv`. Next, open a terminal/command prompt in the directory with the project's Python files ex.`cd C:\Users\Tanner\Documents\Github\Connect-Long-Beach\Python`. Create a text file called `credentials.txt` in that directory if you don't have one already. See below for how to set that file up. In the terminal/command prompt, enter `pipenv shell`. Once in this virtual environment, enter `pipenv install` and it will install all the dependencies automatically. After that you can simply run the main Python file `app.py`. If `app.py` does not work, there may be a conflict with your PATH environment variables. In this case, try `python app.py`.  

IF ANACONDA IS INSTALLED and above doesn't work try it through the anaconda command prompt
---

### Setting Up the credentials.txt File  
Write into the credentials.txt file you made/have so it look like this:  
```
host = <ipv4 of database server>  
user = <username>
passwd = <plaintext password> 
database = <name of database>
```
example
```
host = 123.123.123.123 
user = bob
passwd = securePassword123 
database = work
```
Note: this file needs to be in the same directory as `app.py`.
