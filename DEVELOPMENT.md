## Pull the Repository to Local Machine

```sh
git clone git@github.com:Juggernaut9434/CSE412-PlaneRouteGeoMap.git
```

## Create a Postgres Database Instance

### Install PostgresSQL

1. [Install PostgreSQL](https://www.postgresql.org/download)
1. check CLI is installed with `psql -V`

### Create Database

1. Navigate to `application/db_setup`
1. Unzip the data zip file [all_the_data.zip](application/db_setup/)
 - so each .dat is in the db_setup directory
1. There is a setup script provided [setup.sh](application/db_setup/setup.sh)
1. Run this script, it will create a database, tables, and import data

#### Password for User

By default the password for users are `postgres` but if there are any issues run:

```sh
psql -c "ALTER USER user_name  WITH PASSWORD 'postgres';"
```

### Setup Credentials for back_end

1. Edit [database.ini](database.ini) to include user and password

## Setup Python 3.9

### (optional) Install Python Environment Manager

1. Install `pyenv` to your machine. [Documentation](https://github.com/pyenv/pyenv#installation)
1. Check Version with `pyenv --version`
1. Navigate to the root directory of the repository
1. `pyenv install 3.9.13`
1. `pyenv local 3.9.13`

### Create Python Virtual Environment

1. `python -m venv application/venv` will create a virtual environment under application
1. `source application/venv/bin/activate` will activate the virtual environment

NOTE: to deactivate type `deactivate` in the terminal

### Install Dependencies

1. With the venv activated, run:
 ```sh
 pip install --upgrade pip;
 pip install -r requirements.txt
 ```

## Run the Program

```sh
python application/application.py
```

There is a gui that will pop up and the console will list any logs and warnings encountered.
If there any unusual behavior, check the console and it will print out the errors.
Expected errors are the PhotoImage error.

The gui will be empty for about a minute before the routes are fully loaded onto the page.
By default 1000 routes are loaded in which take a little time to load.
