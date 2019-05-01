# Aloha, cli-mate 
Let's analyze climate data to explore climate conditions before our upcoming Hawaii trip in February! 

With the climate data, let's create an API to show precipitation and temperature data in JSON using Flask.

## Resources 
- Data has been kindly provided by UC Berkeley's Data Analytics and Visualization

## Running Jupyter Notebook 
- In terminal, go to the project directory and run the jupyter notebook file for climate analysis 
```
$ cd climate
$ jupyter notebook 
```

## Running Flask app
- To run the flaskapp, type in terminal:
```
$ python flaskapp.py
```

- Open a new window and type localhost:5000/ and you should see the <b>available routes</b> listed:
<img src="https://github.com/ying-li-python/climate/blob/master/Images/homepage.png"> 

## Flask App
While the app is running, let's navigate to the different API routes! 

#### Precipitation API example @ http://localhost:5000/api/v1.0/precipitation  

<img src="https://github.com/ying-li-python/climate/blob/master/Images/precipitation_json.png"> 

#### Temperature API example @ http://localhost:5000/api/v1.0/tobs

<img src="https://github.com/ying-li-python/climate/blob/master/Images/temp_json.png">

#### tmin, tavg, and tmax for 2017-01-01 @ http://localhost:5000/api/v1.0/2017-01-01

<img src="https://github.com/ying-li-python/climate/blob/master/Images/start_date_json.png">

#### tmin, tavg, and tmax for dates 2017-02-28 to 2017-03-05 @ http://localhost:5000/api/v1.0/2017-02-28/2017-03-05

<img src="https://github.com/ying-li-python/climate/blob/master/Images/start_end_date_json.png">

## Climate Analysis

#### Figure 1 
<img src="https://github.com/ying-li-python/climate/blob/master/Images/precipitation.png">

- Overall, precipitation falls to a range of 0-6 inches, depending on the month. On average, precipitation is less than 1 inch.

#### Figure 2
<img src="https://github.com/ying-li-python/climate/blob/master/Images/temperature.png">

- The average temperature, for the station with the highest number of records, generally spans around the mid-70s, with lows at 60 and highs at 80.

#### Figure 3
<img src="https://github.com/ying-li-python/climate/blob/master/Images/trip_temperature_average.png">

- Considering the daily normals based on historic data, the average temperature is at around 70 degrees, with lows at 57 degrees and highs at 80 degrees. 

- Based these data obeservations, the climate is likely to be comfortably warm during our trip!

## Author 
Ying Li

