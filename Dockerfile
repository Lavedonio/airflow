FROM apache/airflow:2.3.3-python3.10

# Installing packages
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow

ARG AIRFLOW_HOME=/opt/airflow

# Updating environment variables
ENV PATH="$PATH:${AIRFLOW_HOME}"
ENV PYTHONPATH="$PYTHONPATH:${AIRFLOW_HOME}/scripts/python"

# Copying project files
COPY ./scripts ${AIRFLOW_HOME}/scripts
COPY ./airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
COPY ./webserver_config.py ${AIRFLOW_HOME}/webserver_config.py

# Installing requirements
COPY ./requirements-airflow-docker.txt ${AIRFLOW_HOME}/requirements-airflow-docker.txt
COPY ./requirements.txt ${AIRFLOW_HOME}/requirements.txt

RUN set -ex \
    && pip install --user -r ${AIRFLOW_HOME}/requirements-airflow-docker.txt \
    && pip install --user -r ${AIRFLOW_HOME}/requirements.txt
