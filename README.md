## CandidateScope: Automated Profiling and Cultural Fit Analysis
## Team: DH

## Presentation
An overview of our presentation's key points and highlights:<a href="https://docs.google.com/presentation/d/16UfgbIRd2ZKFoP5PyvyKgu0Xo_pkp7nxvJ_S2yB_01o/edit?usp=sharing"> Presentation </a>

## Setup Instructions
Clone the repository

```sh
$ git clone https://github.com/rishavgoenka8/dh-megathon.git
```

###  Backend
Create a virtual environment to install dependencies in and activate it:

```sh
$ cd dh-megathon/backend
$ python3 -m venv venv
$ source venv/bin/activate
```

Then install the dependencies:

```sh
(venv)$ pip3 install -r requirements.txt
```

To perform db-migrations and running django server:

```sh
(venv)$ python3 manage.py makemigrations
(venv)$ python3 manage.py migrate
(venv)$ python3 manage.py runserver
```

### Frontend
```sh
$ cd dh-megathon/frontend
$ npm install
$ npm start
```
