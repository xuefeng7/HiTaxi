#<img src="https://github.com/xuefeng7/HiTaxi/blob/master/figure/hitaxi.png" width="240"><img src="https://github.com/xuefeng7/HiTaxi/blob/master/figure/name.png" width="100">
## High Taxi Demanding Prediction in NYC by Time, Region, Facility, Event and Weather.
##### A University of Rochester VISTA Lab project dedicated to urban computing research

### Intro
Heavy traffic, untampered energy waste, deteriorating public safety, illegal drug dealings, and etc., all of those issues are ineluctable for a growing city. With more and more concerns towards those issues, people are determined to seek solutions that are able to not only ease them but also eradicate them. This determination finally leads people to urban computing --- a solution empowered by massive computing capabilities. This new way is not limited to solely solve those common issues a developing city may encounter, it aims to plan the city to be more intelligent in various aspects. Many researches are conducted with the goal of making cities smarter, some of them endeavor to improve the city traffic by proposing a large-scale taxi/bike ridesharing service, some of them endeavor to monitor and predict the air/water quality of certain city regions, and some of them are interested in energy consumption control via supervising urbane refueling behaviors. Those researches show numerous promising potentialities of urban computing.

With the same goal of creating smarter cities, we are particularly interested in the traffic aspect.  Many city dwellers would complain that sometimes in certain areas of the city, it is extremely hard to catch a taxi or it takes too long to wait a bus/subway to come. On the other hand, taxi drivers are complaining that sometimes they are not aware of which part of the city is demanding the rides so as to lose their potential revenues. Imaging what if we can predict which region of a city would encounter an increasing demand of taxi or transportation in advance, then we can solve the complains from both sides by allocating the taxi drivers or schedule more public rides to those areas beforehand.

In this project, We aim not only to suggest taxi drivers with high taxi demanding regions in real-time, but also to uncover some insightful taxi demanding patterns given NYC's extraordinarily high density.

### Fun Fact
* The super popluar regions in NYC according to 200,000 check-ins from FourSquare
  
  
  <img src="https://github.com/xuefeng7/HiTaxi/blob/master/figure/super_popular_venus_NYC.png" width="480">

* To make the area prediction as informative as possible, we have clustered 0.2-million check-in into 500 regions in NYC according to those check-ins
  
  
  <img src="https://github.com/xuefeng7/HiTaxi/blob/master/figure/nyc_popular_region_clustering_500.png" width="480">

* The cluster centers in NYC,  the cluster method we have employed is k-means++
  
  
  <img src="https://github.com/xuefeng7/HiTaxi/blob/master/figure/cluster_centers.png" width="480">

* The monthly demand/trip


 <img src="https://github.com/xuefeng7/HiTaxi/blob/master/figure/monthly demand.png" width="480">

* The demand/trip and hour distribution


 <img src="https://github.com/xuefeng7/HiTaxi/blob/master/figure/demand:hr.png" width="480">

* The demand/trip and weekday distribution


 <img src="https://github.com/xuefeng7/HiTaxi/blob/master/figure/demand:weekday.png" width="480">

* The demand/trip and temperature distribution


 <img src="https://github.com/xuefeng7/HiTaxi/blob/master/figure/demand:temp.png" width="480">

* The demand/trip and weather condition  distribution


 <img src="https://github.com/xuefeng7/HiTaxi/blob/master/figure/demand:wc.png" width="480">

Note: Demand indicates the total passenger count, whereas the trip indicates one single taxi trip.

### Region Refinement   
we have clustered all popular checkin points into 500 regions so that they cover almost every popular region in the city of New York. However, we want to further classify those 500 regions into several clusters so that each one of them could represent some special and unique characters. To achieve this goal, our firs task is to identify how many type of venues are inside each region. According to the type of checkin points provided by Foursquare, we assign each region with eight venue types, they are Arts & Entertainment, College & University, Food, Great Outdoors, Home & Work, Nightlife Spot, Shop, and Travel Spot. If a checkin point, whose venue type is Food, falls into the region, then Food venue type of this specific region will be incremented by one. By doing this, we will have a venue feature vector for each region, and then we again run k-means++ on those 500 regions again and separate them by their venue feature vectors.


### Update
1. We have collected 220 million yellow cab trip data (2014)  from *nyc opendata*, we are trying our best to process and analyze them.
2. we will keep updating our progresses...

 
