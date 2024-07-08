********************
Make sure to have Python, pip, node.js, and MySQL already installed onto your system 
Open command prompt or terminal and navigate to where the project directory is located
cd into it (you should be in project-hasnaindb)
Open app.py with notepad (or any editor)
Starting from line 12 is the connector to MySQL
You will need to change port, username, and password to what you set it to
Default port is 3306, and default username is root
Save and exit app.py, making sure you are still in the root of the project directory (project-hasnaindb)
The part below shows how to run the Flask portion
********************

Running for The First Time:
  if on Windows, copy the following into your command prompt:
    venv\Scripts\activate

  else if on Unix or Mac, copy the following command into your terminal:
    source venv/bin/activate

  then copy the following into your terminal/command prompt one by one:
    pip install -r requirements.txt
    flask run

  (flask should now be running)

********************
When you run flask, it should tell you what it is running on, in my case it was http://127.0.0.1:5000
If yours is the same, then ignore this
If not, do ctrl+c to stop flask from running
From project-hasnaindb, cd into frotnend, then open package.json with notepad or any editor
Go to line 21 and change the http to match what you system displayed
Save and exit
Make sure you are in the root of the project directory (project-hasnaindb)
Type in flask run and enter
********************

Not the First Time Running:
  if on Windows, copy the following into your command prompt:
    venv\Scripts\activate

  else if on Unix or Mac, copy the following command:
    source venv/bin/activate

  then copy the following into your temrinal:
    flask run

(The flask portion should now be running)

********************
Open a new command prompt/terminal, two terminals should now be open
Navigate to where the project directory is located
cd into it (you should be in project-hasnaindb)
The part below shows how to run the React portion
********************

Running for The First Time:
  copy the following into your command prompt one by one:
    npm install axios
    npm install --save-dev @babel/plugin-proposal-private-property-in-object
    cd frontend
    npm start
    
(The react portion should be running now, and a couple of seconds later a webpage should open)

Not Running for the First Time:
  cd frontend
  npm start

(The react portion should be running now, and a couple of seconds later a webpage should open)

********************
To stop flask and react from running, do ctr+c in both terminals
Run the flask part before running the react part
If (venv) is on, then you don't need to do the venv\Scripts\activate command again, skip straight to flask run to run the Flask portion
Conversely, if you are already in frontend, you can skip straight to npm start to run the React portion
The commands below show how to deactivate the virtual environment (need to be in the root of the directory; project-hasnaindb)
********************

if on Windows:
    venv\Scripts\deactivate

else if on Unix or Mac:
    deactivate

