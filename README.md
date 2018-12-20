
# FreshBudgets

Instructions / notes for running and testing the backend server. MySQL server is hosted on Google Cloud.


### Prerequisites

* Python 3.6
* pip
* virtualenv

## Setup

### Virtual Environment

Before running the backend, you must setup a Python virtual environment. 
These are configured on a per-machine basis, so that is why it is not included in the repository. 

Start by creating a virtual environment called 'env' and specifying it to use Python 3

```
virtualenv --python Python3 env
```

This will create a folder named /env/ in whatever directory you are in. 
Don't worry if you are in the repository, the .gitignore is setup to ignore folders with name /env/. 

#### Activating the virtual environment

```
source env/bin/activate
```

#### Deactivating the virtual environment

```
deactivate
```

Activate your virtual environment and install dependencies for the project.

```
pip install -r requirements.txt
```

## Running the server

### Activate proxy

Activate the sql proxy to allow the server to connect to our MySQL database. Run the .sh file

```
./run_proxy.sh
```

### Run server

First, activate the virtual environment.

```
source env/bin/activate
```

Then run the server.

```
python manage.py runserver
```

The server is now running on 

```
localhost:8000
```

## Links
* https://www.techiediaries.com/create-react-app-django/
* https://cloud.google.com/python/django/appengine
* https://cloud.google.com/appengine/docs/flexible/python/testing-and-deploying-your-app
