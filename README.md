# Find Your Influencer

#### Mengyao Liu 03/03/2021
#### mengyao.cecily.liu@gmail.com

## 1. Overview
*Find Your Influencer (FYI)* is a recommendation engine to recommend the right influencers to merchants based on Twitter data. The main tools used are the Twitter API and the ```twint``` package for scraping the data, ```Regex```, the ```KeyBERT``` package, the ```nltk``` package for natural language processing, and ```streamlit``` for building the app.

Now only the influncer type with "100-1k" followers is available due to limit in computing resources. The source code analyzing the data is not uploaded here.

## 2. Data Collection

### 2.1 Identifying Influencers
First we find our influencer candidates from Twitter. We define an active influencer as a candidate who has at least one tweet with the hashtag "ad" and is like by at least 10 users since 01/01/2018. We use the ```twint``` package to go through a large amount of Twitter data and retrieve their usernames without rate limit. ```twint``` can only find information about verified users, which is fine in our situation, because we would like the influencer we recommend to be reliable. There is another pitfall that some active influencers may not use the hashtag "ad" in their posts, even if it is an ad post. Thus we may miss a certain type of influencers and introduce bias. In the end, we find 375 verified active influncers with followers "100-1k", 2156 verified active influncers with followers "1k-10k", 3080 verified active followers "10k-100k", 2473 verified active influncers with followers ">100k". Since the number of each influencer category is pretty large, for now we do not consider the selection bias as a big issue. 

### 2.2 Identifying Relevant Tweets
For each product category, we have a list of keywords that we think a relevant tweet may contain. For now this list is generated mannually by going through tens of truly relevant tweets by influencers on Twitter and extracting the high-frequency words. We tried some more automatic methods like using ```word2vec``` and ```wordnet``` to find the hypernyms, hypinyms and similar words of the product name, but the results were not satisfying. So we decide to do it manually given that we do not have so many product categories for now since it proves to be the most effective way so far.

Then given a certain product category and a certain influencer category based on the number of their followers, for each influencer in that influencer category, we count how many tweets that contain at least one of those keywords belongong to that product are there in the last three months. Back at the time the code was run, we count all the tweets from 11/14/2020 to 02/14/2021. 

However, just containing some of the keywords does not necessarily mean this tweet is about that product. For the "book" category for example, one keyword is "read", and some tweet like "Have you read my message?" will be counted, even though we know it is not about books. To further improve the accuracy of the identification, we use ```KeyBERT``` to extract the keywords of a tweet itself. We adopt the minimum of 10 and the magic number 1/8 of the tweet length as the number of keyword we want to extract. If at least one of the keywords of the tweet itself lies in the keyword list of the product we give, we consider that this tweet is truly relevant.

Next we select the top 50 influencers order by the number of their relevant tweets and focus on them from now on. For the "book" category for example, the 50th influencer only has 1 tweet that may be related to books in the past three months. We think this cut is reasonable because on the one hand we still have 50 candidates to choose from, and on the other hand, it is hard to imagine that a influencer who never tweets about books would have a large number of book fan followers. Thus discarding them and believing that the best candidates are among others is a reasonale idea, especially when we have limited computing power.

### 2.3 Retrieving Follower Information








