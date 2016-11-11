FourSquare dataset descroptions:

1. catergories.txt is a json file contains the tree information of all the categories in Foursquare.

2. Venues fold contains the Venues visited by the users in LA and NYC with the following fields:
Venue id | venue name| latitude| longitude| address|city|state| checkin #| checked user#| current user#| todo# |category # | category id 0| category id 1| ?
 
3. Users fold contains the user profiles of users who visited LA and NYC from foursquare, with the following fields:
User id| first name| lastname| profile pic| gender| home city|
 
4. Tips fold contains the series of tips from single user, with the following format:
User id| tip| tip|?
For each tip has the following format:
Venue id | 0 | null|  text| created time |todo#| done #| category # | category id 0| category id 1| ?

5. Friendship fold constains the user friendships with the following format:
userid | userid.


Please cite the following two papers when using the dataset:

[1] Jie Bao, Yu Zheng and Mohamed F. Mokbel. "Location-based and Preference-Aware Recommendation Using Sparse Geo-Social Networking Data". In ACM SIGSPATIAL (GIS 2012), Redondo Beach, CA, US, 2012

[2] Ling-Yin Wei,Yu Zheng, Wen-Chih Peng. "Constructing Popular Routes from Uncertain Trajectories". In 18th SIGKDD conference on Knowledge Discovery and Data Mining (KDD 2012).

Thanks.
