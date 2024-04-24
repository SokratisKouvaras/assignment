# NYC Taxi & Limousine Commission - For-Hire Vehicle (FHV) trip records



## Getting started

The For-Hire Vehicle (“FHV”) trip records include fields capturing the dispatching base license number and the pick-up date, time, and taxi zone location ID (shape file below). These records are generated from the FHV Trip Record submissions made by bases.

The purpose of this repository is to provide a way to: 
- ingest the NYC taxi data
- create a dbt project to transform the ingested data
- visualize the data using a PowerBI dashboard

## What we will need

To run the repository a [Docker Engine](https://www.docker.com/) is needed in order to create the required containers.

## Creating a Postgres database

The first thing that we need is a place to store the data as provided from the source. In order to do so we need to run the docker-compose YML file that is available in the root of the repository. The created database will have persistant volume to store the data. This way information will not be lost in case we shutdown the PG instance.

To create the instance we need to run:

```
docker-compose up -d
```
The newly created database will be listening in 127.0.0.1:5432 and the default credential (username:"postgres",pwd:"") can be used to connect to the "postgres" database.

## Ingesting the FHV High Volume dataset


cd ingestion
docker build -t ingestion .
docker run --net=host ingestion

docker build -t dbt .
docker run --net=host dbt

