# Find Your Influencer

#### Mengyao Liu 03/03/2021
#### mengyao.cecily.liu@gmail.com

## 1. Overview
*Find Your Influencer (FYI)* is a recommendation engine to recommend the right influencers to merchants based on Twitter data. The main tools used are Twitter API Standard v1.1 and the ```twint``` package for scraping the data, ```Regex```, the ```KeyBERT``` package, the ```nltk``` package for natural language processing, the ```altair``` package and the ```wordcloud``` package for visualization, and ```streamlit``` for building the app.

The link to *FYI* is https://share.streamlit.io/mengyao-liu/fyi/app.py. Now only the influncer type with "100-1k" followers is available due to limit in computing resources. The source code analyzing the data is not uploaded here.

## 2. Data Collection

### 2.1 Identifying Influencers
First we find our influencer candidates from Twitter. We define an active influencer as a candidate who has at least one tweet with the hashtag "ad" and is like by at least 10 users since 01/01/2018. We use the ```twint``` package to go through a large amount of Twitter data and retrieve their usernames without rate limit. ```twint``` can only find information about verified users, which is fine in our situation, because we would like the influencer we recommend to be reliable. There is another pitfall that some active influencers may not use the hashtag "ad" in their posts, even if it is an ad post. Thus we may miss a certain type of influencers and introduce bias. In the end, we find 375 verified active influncers with followers "100-1k", 2156 verified active influncers with followers "1k-10k", 3080 verified active followers "10k-100k", 2473 verified active influncers with followers ">100k". Since the number of each influencer category is pretty large, for now we do not consider the selection bias as a big issue. 

### 2.2 Identifying Relevant Tweets
We use the "bag of words" method to identify relevant tweets. For each product category, we have a list of keywords that we think a relevant tweet may contain. For now this list is generated mannually by going through tens of truly relevant tweets by influencers on Twitter and extracting the high-frequency words. We tried some more automatic methods like using ```word2vec``` and ```wordnet``` to find the hypernyms, hypinyms and similar words of the product name, but the results were not satisfying. So we decide to do it manually given that we do not have so many product categories for now since it proves to be the most effective way so far.

Then given a certain product category and a certain influencer category based on the number of their followers, for each influencer in that influencer category, we count how many tweets that contain at least one of those keywords belongong to that product are there in the last three months. Back at the time the code was run, we count all the tweets from 11/14/2020 to 02/14/2021. 

However, just containing some of the keywords does not necessarily mean this tweet is about that product. For the "book" category for example, one keyword is "read", and some tweet like "Have you read my message?" will be counted, even though we know it is not about books. To further improve the accuracy of the identification, we use ```KeyBERT``` to extract the keywords of a tweet itself. We adopt the minimum of 10 and the magic number 1/8 of the tweet length as the number of keyword we want to extract. If at least one of the keywords of the tweet itself lies in the keyword list of the product we give, we consider that this tweet is truly relevant.

Next we select the top 50 influencers order by the number of their relevant tweets and focus on them from now on. For the "book" category for example, the 50th influencer only has 1 tweet that may be related to books in the past three months. We think this cut is reasonable because on the one hand we still have 50 candidates to choose from, and on the other hand, it is hard to imagine that a influencer who never tweets about books would have a large number of book fan followers. Thus discarding them and believing that the best candidates are among others is a reasonale idea, especially when we have limited computing power.

### 2.3 Retrieving Follower Information
For each of the top 50 influencer, we retrieve their followers as well as their followers' tweets through Twitter API Standard v1.1. Due to limit in computing resources, for the influncer type with "100-1k" followers, we only retrieve their most recent 50 followers and the most recent 30 tweets of each follower. That is 1500 tweets from followers in total for each influencer.

### 2.4 Retrieving Tweets that Mentioned the Influencer
For each of the top 50 influencer, we retrieve the tweets that mentioned the influencer. Due to the limit of Twitter API Standard v1.1, we can only retrieve data up to one week ago, in our case, the week before 02/14/2021.


## 3. Recommendation
The recommendation is mainly content-based, where we analyze the influencers' profiles, tweets, as well as their followers' tweets. We use four key metrics to derive the recommendation score: first and most important, the number of relevant tweets from the influencer's followers; second, the number of relevant tweets from the influencer themselves; third, the engagement level of the influencer's relevant tweets; last, the sentiment of the tweets that mentioned the influencer.

When calculating the engage level, we count the average number of like/comment/retweet per tweet for each influencer. When calculating the mention sentiment, we use ```VADER``` in ```nltk``` to derive the sentiment score of each tweet that mentioned the influencer and adopt the mean value for the final sentiment score.

Since we do not have ground truth to learn from, we define our own weight to combine the metrics. We give the above four features a weight of 7, 5, 3, 1 respectively. When we add them togeter, we normalize each metric by dividing the value by the maximum value of that metric and times a constant 100./16., so that a candidate that has the best performance in every metric will have a score of 100.

## 4. Visualization
We use ```altair``` to make an interactive plot for each request. On the plot, the four metrics of the top 50 influencers are shown. The detailed numbers are also available, in case the clint wants to use their own weight and recalculate the rank.

Since this is unsupervised learning, we do offer a way to check if the recommendation is reasonable. The client can input the name of any of the top 50 influencers and see what their followers are talking about most recently. Once getting the name (the input format is very flexible, with or without "@", with or without space), we will show the wordcloud of their most recent 50 followers' most recent 30 tweets. If you see that their followers are talking about things related to your product frequently, you know the recommendation makes sense.

## 5. Future Plan

### 5.1 Fighting Limitation in Data Scraping and Computing Resource
The biggest limitations so far are the data scraping rate from Twitter API and the computing resource. Ideally, we will retrieve the information of every follower of a specific influencer, and retrieve their timelines in a longer time frame. We will also be able to analyze and build up the influencer categories with a larger number of followers, expand the product category, and adding new categories. 

For the sentiment analysis, originally we planned to analyze the comments of those relevant tweets from a influencer. However, Twitter API does not have this attribute to retrieve the comments of a tweet. Thus we turn to the tweets that mentioned the influencer. At first, we tried filtering the mention tweets to only those which are replies to the relevant tweets of the influencer, but the one week limit results in too few comments to analyze. This is also something that can be solved given a higher data scraping rate.

### 5.2 A/B Test

Now we use the word cloud of the recommended influencer's followers to check if our recommendation is reasonable, but there is only so much it can tell us. The best way to test the effectiveness of our recommendation engine is to carry out A/B test, i.e, using our recommendation versus randomly picking influencers or using whatever existing algorithm to choose influencers, and see if the marketing ROI with our recommendation is significantly better than other methods. 

### 5.3 Better Definition in Relevance
As mentioned in Section 2.2, now we use mannually generated keyword lists and check the overlap with a tweet to identify the relevance. We can think of a more sophisticated way to build the connection between tweets and the product, or at least a more automatic way to generate the keyword list.


### 5.4 Ground Truth 
If there were ground truth of which influencers are successful and which influencers are not, we can turn this question into a supervised learning problem and can build Classification models to derive the weights for features. We can also build Clustering models to find similar influencers to the successful ones and make the recommendation engine collaborative. However, this is hard to realize because when the ground truth data can be used to train a machine learning model, it must be a large amount of data. And in reality, it is even hard to classify "successful". 

### 5.5 More Personalization
We can add more product categories and further divide the current product categories, e.g., "books" into textbooks, magazines, literature, history, etc. We can add more dimensions to the influncer category, e.g., location. We can also add more categories in addition to the existing two (product, influencer type), e.g., customer type -- age, student or non-student, with or without kids, etc. The problem is that Twitter does not provide such information we want.

### 5.6 Others
We can try to eliminate the selection bias to identify influencers. We can also scrape and analyze data from other platforms, such as Instagram. 

