# Airflow
Personal Airflow repository, for testing and personal programmable routines.


## Index

- [Pre-requisites](#pre-requisites)
- [Installation](#installation)
- [Usage](#usage)


## Pre-requisites

- [Docker](https://www.docker.com/)


## Installation

1. **[Optional]** Create a `.env` file in the project's root directory and fill the blanks based on following template:

```
# Base config
AIRFLOW_IMAGE_NAME="apache/airflow:2.0.1"
AIRFLOW__CORE__FERNET_KEY=""
_AIRFLOW_WWW_USER_USERNAME="airflow"
_AIRFLOW_WWW_USER_PASSWORD=""

# Additional config
AIRFLOW__CORE__LOAD_EXAMPLES="true"
AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG=3
AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS="true"
AIRFLOW__WEBSERVER__DEFAULT_UI_TIMEZONE="UTC"
```

In case you want to add more configurations, remember to also add them in the `docker-compose.yml` file.

2. Open the terminal in the project's directory and run the command `docker-compose up`


## Usage

1. Open your browser into the url http://localhost:8080/

2. Log in with the username and password set in the `.env` file or, if you skipped the first step, use the default:

- username: airflow
- password: airflow

3. Enable the DAG you want to test and check the logs
