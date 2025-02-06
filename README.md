## Description
This project aims to generate fake unstructured data(json) related to logistics and load it to mysql database.
Alerts are implemented to send messages on Slack upon tasks failure. 

## Overview
All tools used in this project were built using Docker.
There were 4 main Docker images used.
- `apache/airflow:2.9.1 ` , This is the main image used for airflow deployment.
- `mysql:oraclelinux9`, This is the image for mysql database, which will hold the data.
- `python:3.10.12-slim`, This image was used as the the remote server on which the data generation, preparation and transformation to a structured file is created. 

A pipeline was created using airflow to perform the following.

1. Connect to a remote python server, execute `generate_fake_data.py`. This step generates a json file.
2. Connect to a remote python server, execute `prepare_load.py` which flattens the json file from step 1 and loads into the mysql database using the sqlalchemy library.

If any of these tasks fails, an alert is sent to Slack. The following is an example of an alert sent to slack.

```
:red_circle: Task Failed.
            Task: generate_fake_data 
            Dag: etl-logistics
            Execution Time: 2025-02-04T22:12:25.786459+00:00 
            Log Url: http://localhost:8080/dags/etl-logistics/grid?dag_run_id=manual__2025-02-04T22%3A12%3A25.786459%2B00%3A00&task_id=generate_fake_data&map_index=-1&tab=logs
```

## How to run 

## Steps Explained in detail

### 1. Estbalish connection between airflow and python container
For that I defined a connection in airflow and used the service name of the container as the host name to connect to. I also needed to cerate a password for the python container in order to be able to connect to it from airflow.

I wanted to follow this approach of seperating airflow and python as this is regarded as best practice. Airflow is only an orchestrator and should not do any of the extarction,transformation or loading.

### 2. Generating fake data

For this task, the library faker was used to generate fake data. 

A function was created for column. To ensure that the data is semi-structured I used the library random, to introduce randomness into how the data was generated and also made sure that some columns are empyt for some records. 

Such columns are: Middle name and for orders that are not yet shipped (Status being Ordered only), there is no contact details yet for 'star' which indicates the person delivering the package.  

Finally this generated data is stored as a json file. Regarding the size of the file, the script takes one input being the size of the data to generate (small/medium/large)/ The following is the range of records to generate for each.

- small_range = [5000,9999]
- medium_range = [10000,20000]
- large_range = [25000,50000]

### 3. Flatten the dataset and load into mysql.

For this task, I used the library Pandas to load the json file and flatten it. The flattening technique used was to simply convert each key in the json file to a column. And for keys within other keys, the column name was `key_nestedkey`.  

I used the `json_normalize` method for this and used `_` as a separator for sub keys. I used the [documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.json_normalize.html) as a reference.

After normalising the json file into a structured dataframe, I did some basic cleaning before loading to mysql. That included renaming the columns so that they are all lowercase and following the snake case naming convention [reference](https://peps.python.org/pep-0008/#function-and-variable-names).

Finally the dataframe was loaded into mysql database.

### 4. Setting up alerts

For alerts, I used Slack as my destination as the integration between Slack and Airflow is well supported and straight-forward.

In Slack I created a workspace and enabled incoming web hooks following this [documentation](https://api.slack.com/messaging/webhooks).

After that I created a connection in Airflow and placed the token generated from the webhook as the password and used the [SlackWebhookOperator](https://airflow.apache.org/docs/apache-airflow-providers-slack/stable/_api/airflow/providers/slack/operators/slack_webhook/index.html#airflow.providers.slack.operators.slack_webhook.SlackWebhookOperator) to send the alerts on failure.

## Future considerations

### 1. Create a database model
For this step after loading the raw data into mysql. I would normalise the data and make sure they are following thirds Chumskys Normal Form (3NF).

### 2. Optimisations for querying
For this Step I would firstly partition the raw data by the execution date (which would be passed by airlfow) so that when transformations are made later they are only made on todays data.

Secondly, I would look for the columns that may be analysed frequently and index it. 



