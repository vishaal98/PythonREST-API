# PythonREST-API
this is a basic rest API built with python Flask and SQLITE

HOW TO INSTALL
1. clone the repo
git clone https://github.com/vishaal98/PythonREST-API.git

2. create a virtual env
python -m venv venv
./venv/Scripts/activate

3. install all the packages from requirements.txt
pip install -r requirements.txt
or
pip install package-name  ## for each package in requirements.txt

4. run the app
python main.py


HOW TO MAKE API CALLS
1. Add User
open cmd and run the below command by modifying the values

curl -X POST -H "Content-Type: application/json" -d "{\"first_name\": \"Vishaal\", \"last_name\": \"Nair\", \"age\": \"25\", \"gender\": \"MALE\", \"email\": \"vishnair@gmail.com\", \"phone\": \"83838383\", \"birth_date\": \"2000-30-06\"}" http://127.0.0.1:5000/adduser


2. search user

open CMD and run the below command
curl -X GET http://127.0.0.1:5000/api/users/userName

where username is the name you want to search

OR

open the browser and run the 
http://127.0.0.1:5000/api/users/userName

where username is the name you want to search