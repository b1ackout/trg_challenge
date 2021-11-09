# TRG Evaluation

## Challenge 1

I wanted to make something easily deployable so after some research I cloned [this](https://github.com/omahoco/spark-postgres) repo
 and made the appropriate changes. So a big thanks to omahoco

This project contains the following containers:

* A Spark cluster with two worker nodes.
* A Jupiter notebook server for exploration.
* A Shared filesystem for blob storage.

### Prerequisites

This runs only on unix systems. Please do not run on Windows.
You just need to have docker installed.


### Building the environment

```bash
# Clone the repo
git clone https://github.com/b1ackout/trg_challenge

# Create the environment
cd trg_challenge
make all

# Unpack the data:
make unpack_data
```

To submit the spark job that will generate the parquet files just run:

```bash
make spark-submit
```

To submit the spark job that will generate the json kpis run:

```bash
make spark-kpis
```

## Checking the data via Jupyter and steps followed

Navigate to http://localhost:9999. Jupyter will ask you for a token for authentication.

To get the authentication token from the Jupiter server.

```bash
make jupyter_token
```

In Jupyter, I did some data exploration.

I concluded that the left join of the `street` with the `outcome` datasets is the way to go, because the crimes of the `outcome` that don't join must be from older time period than that of our scope.

Also a window function was used to ensure that the outcome is actually the latest.

I also wanted to deploy an elastic and a kibana node but was not able to make elastic ingest the parquet data, I was always running to errors. I used [this](https://docs.databricks.com/data/data-sources/elasticsearch.html) for reference.

So my other thought was to use databricks for visualization. Since databricks uses its own datasources, lets assume that the shared spark containers storage (/data directory) is a blob storage like S3 and databricks can access it.

An html export file of a databricks notebook is included, containing the kpi visualizations. 