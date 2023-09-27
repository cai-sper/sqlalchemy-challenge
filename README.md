# Climate Analysis and Flask API Development

## Overview

This project involves a climate analysis of Honolulu, Hawaii, using Python, SQLAlchemy, and Flask. The objective is to analyze historical climate data, covering both precipitation and station data, and a Flask API is developed for users to access this data.

## Table of Contents
- [Part 1: Analyze and Explore the Climate Data](#part-1-analyze-and-explore-the-climate-data)
  - [Database Connection](#database-connection)
  - [Precipitation Analysis](#precipitation-analysis)
  - [Station Analysis](#station-analysis)
- [Part 2: Flask App](#part-2-flask-app)
  - [API Routes](#api-routes)

## Part 1: Analyze and Explore the Climate Data

### Database Connection

To connect to the SQLite database, the SQLAlchemy `create_engine()` function is employed. The database schema is reflected using `automap_base()`, resulting in the creation of class references for the `station` and `measurement` tables. A SQLAlchemy session is established to interact with the database.

### Precipitation Analysis

- The most recent date in the dataset is determined (August 23, 2017).
- A query retrieves the previous 12 months of precipitation data, focusing on "date" and "prcp" values.
- The query results are loaded into a Pandas DataFrame, where missing values are filled with zeros.
- The DataFrame is sorted by date and utilized to generate a precipitation plot.
- Summary statistics for the precipitation data are calculated and presented.

### Station Analysis

- The total number of stations in the dataset (9 stations) is calculated.
- To identify the most active station, a query lists stations and their observation counts, with USC00519281 being identified as the most active station.
- Queries are executed to determine the lowest, highest, and average temperatures for the most active station (USC00519281).
- A histogram is generated to visualize temperature observations for the most active station over the previous 12 months.

## Part 2: Flask App

### API Routes

A Flask API is designed with the following routes:

- `/`: This is the homepage that lists all available routes. It serves as the entry point to the API.
- `/api/v1.0/precipitation`: This route returns the last 12 months of precipitation data in JSON format. It provides users with access to recent rainfall information.
- `/api/v1.0/stations`: This route returns a JSON list of weather stations in the dataset. Users can view available weather station information.
- `/api/v1.0/tobs`: This route returns temperature observations for the most active weather station over the last 12 months. Users can access recent temperature data.
- `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`: These routes allow users to specify a start date and an optional end date to retrieve temperature statistics (minimum, maximum, and average) for the specified date range. Users can explore temperature trends within a timeframe.

These API routes provide easy access to climate data and temperature statistics, making it convenient for users to plan their trips and understand the climate in Honolulu, Hawaii.
