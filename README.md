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

To populate our database with the FHV High Volume dataset we need to create the container using the Dockerfile that is available in the ingestion directory.


```
cd ingestion
docker build -t ingestion .
docker run --net=host ingestion
```
For simplicity only the dataset of January 24 is downloaded by default but with a simple modification of the script all datasets (green/yellow/fhv) can be downloaded.
```
if __name__ == "__main__":
    for dataset in [list_of_dataset_to_download ]: 
        for year in [list_of_years_to_download ]:
            for month in [list_of_months_to_download ]:  
                main(dataset=dataset,year=year,month=month)
```
How the script works:
Using the requests python library a GET request is performed in the https://d37ci6vzurychx.cloudfront.net/trip-data/{dataset}_{year}-{month}.parquet URL and the content of the responce is stored in a temporary file within the container. The saved file is then used to create a ParquetFile object using the PyArrow library. Then we iterate over the ParquetFile that is split into BATCH_SIZE chuncks and for every chunck it is converted into a pandas dataframe. Using the build-in to_sql function of pandas the dataframe is stored in the PG database marked with a timestamp of the ingestion. Finally in order to enable rerunning the same script multiple times the final table is drop if it exists (it won't exist the first time we run the script) and our temporary table is renamed by removing the timestamp.

## DBT

To perform all the necessary transformations and enrichment of our dataset we will be using [dbt](https://www.getdbt.com/)

### Seeds
The following additional information is available that can be linked to our FHV dataset:
- [Taxi Bases](https://www.nyc.gov/site/tlc/businesses/for-hire-vehicle-bases.page) with metadata regarding the available taxi bases in NY.
- [Taxi Zones](https://data.cityofnewyork.us/Transportation/NYC-Taxi-Zones/d3c5-ddgc) with metadata about all pickup/dropoff locations in NY.

The structure of the dbt project is the following:
- CleansedZone is the part of the project where all sources/seeds are documented, the table features are assigned the proper datatype and naming convention is standrdized (lower snake case since we are using a PG database)
- DC(DomainConcept)Zone is the part of the project where the Trips domain concept is created with information from all trips available in the dataset. A primary key (dw_trip_id) is generated that will also serve as a reference for all aggregations, and additional features are generated (is_local_trip,is_happy_customer etc).

dbt tests are used across all models as needed. To apply all the transformations and create all the necessary model we need to create a container using the image that will be created from the Dockerfile that is available in the dbt directory. 

To create the container we need to run the following commands:

```
cd dbt
docker build -t dbt .
docker run --net=host dbt
```
## PowerBI dashboard

A sample PBI dashboard with insights from the enriched version of the Trips model is available in the PowerBI directory.

To use the PBI dashboard we only need to connect the PG database and import the DCZone_DC_Trips model:

- Add a new source and select the Postgres connector.

![alt text](https://github.com/SokratisKouvaras/assignment/blob/assignment/images/get_data.jpg?raw=true)

- Use the default credential to connect and press "OK".

![alt text](https://github.com/SokratisKouvaras/assignment/blob/assignment/images/pg_connect.jpg?raw=true)

- Import the DCZone_DC_Trips model and press "Load".

![alt text](https://github.com/SokratisKouvaras/assignment/blob/assignment/images/DC_Trips.jpg?raw=true)

Enjoy!