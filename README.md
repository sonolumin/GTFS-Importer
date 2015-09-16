Test Move to Github

# GTFS Postgis ETL

This script pulls data from a GTFS api and saves that data into the PostgreSQL server also provided by the db/ directory (with docker).

## Agencies `gtfs_agencies`

Agencies are known Public Transit agencies, which provide services such as trains, buses, and trams to public for a fare. These can either be government or private entities.

| Name   | Column Name |
| ------ | ----------- |
| ID     | agency_id   |
| Name   | agency_name |
| URL    | agency_url  |
| Routes | N/A |

## Routes `gtfs_routes`

A route is a known path along the ground, which an agency provides it's services.

| Name       | Column Name      |
| ---------- | ---------------- |
| ID         | route_id         |
| Short Name | route_short_name |
| Long Name  | route_long_name  |
| Color      | route_color      |

## Stops `gtfs_stops`

A stop is a known location that an agency will stop to pick up customers, which will typically reside on any and potentially multiple routes that agency may have.

Properties:

| Name       | Column Name      |
| ---------- | ---------------- |
| ID         | stop_id          |
| Name       | stop_name        |
| Code       | stop_code        |
| Latitude   | stop_lat         |
| Longitude  | stop_lon         |
| Position   | the_geom         |

# Running

## Database

The db folder contains two files: the Dockerfile and the schema file. These files are used for building the proper setup for containing the GTFS data with PostGIS installed.

### Quickstart

```
cd db
## Build the docker image
docker build -t gtfs-db .
## Start the postgresql server
docker run --name gtfs-db gtfs-db -d
```

## ETL Script

The `main.py` file is the entrypoint into running the ETL script, but a Dockerfile is created to allow running the process inside a docker container.

### Quickstart

```
## Build the docker image
docker build -t gtfs-etl .
## Start the script with live output streaming
docker run --rm --link gtfs-db:postgres gtfs-etl
```