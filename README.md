# MapReduce sentiment analysis system
Simple MapReduce program, based on Hadoop framework

## Crawler
This program is provide tweets downloading, using Twitter streaming API and tweepy library.
Program runs during one hour and gets tweets stream filtered by interesting places.
Crawler require special config file, named `config.json`

###### Usage
`python3 crawler/main.py`

###### config.json syntax
```json
{
  "consumer_key": "replace API key here",
  "consumer_secret": "replace API secret here",
  "access_token": "replace token here",
  "access_token_secret": "replace token secret here",
  "places": [
    {
        "name": "New York, NY, USA", 
        "northeast": {"lat": 40.91525559999999, "lng": -73.70027209999999},
        "southwest": {"lat": 40.4913699, "lng": -74.25908989999999}}
  ],
  "output": "/media/external/big_data/twitter.txt"
}
```
`places` parameter contains list of places, which will be using to filter.


## Mapper
`mapper.py` script is responds for Map phase of MapReduce program  
* The first step is to process hashtags and split it to separate words.
* Second step is removing of users links and http links from tweet
* Third step is separating of tweet terms. Terms includes emoticons
After this simple steps script count sentiment value of tweets, using special dictionary
and returns 1 if tweet positive or 0 if tweet negative.


## Reducer
`reducer.py` script is responds for reduce phase of MapReduce program.
The logic of script is simple. Script read stdin, and process every line.
It split line by tabulation symbol and then count sentiment values of tweets from every place

## Usage
$HADOOP_INSTALL/bin/hadoop jar $HADOOP_INSTALL/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar \  
-input /hdfs_folder/input.txt \  
-output /hdfs_folder/output.txt \  
-file "mapper.py" \  
-mapper "mapper.py" \  
-file "reducer.py" \  
-reducer "reducer.py"  

## Dictionary
MongoDB is used to store dictionary. In this project I used dictionary, that was created by Alex Davies, 
[visit his site](http://alexdavies.net/twitter-sentiment-analysis/)