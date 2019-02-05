---
linetitle: "Udacity Data Analyst Nanodegree"
title: "02 Examine the TMDB Movie Database"
author: David Lassig 
date: 2019-01-11
subject: "Data Analyst"
tags: [udacity]
header-includes:
- \usepackage{minted}
- \usepackage{xcolor}
- \definecolor{bg}{rgb}{0.95,0.95,0.95}
- \definecolor{lin}{rgb}{0.67, 0.88, 0.69}
- \definecolor{win}{rgb}{0.6, 0.73, 0.89}
- \definecolor{met}{rgb}{0.93,0.79,0.69}
- \definecolor{att}{rgb}{0.0,1.0,0.0}
- \definecolor{vic}{rgb}{0.8,0.0,0.0}
---



# Project: Examine The TMDB Movie Database

## Introduction

I've choosen the TMDB dataset as I'm a passionated movie watcher and in the past I had doubts whether the voting results of movie database services are representative for the real quality of some movies. For example it occurs that bombastic Blockbuster movies are rated much higher on a user driven platform [IMBD](https://www.imdb.com) then on a professional critic driven platform like [Rotten Tomatoes](https://www.rottentomatoes.com). I've choosen these questions for further analysis:

  * __Question 1:__ Does movies have better ratings if they're voted more often?
  * __Question 2:__ Is there a correlation between specific actors and the associated movie rating or associated revenue?

Before doing any analysis I will import needed libraries and setting styles:


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import json
plt.style.use("seaborn-dark")

%matplotlib inline
~~~

## Data Wrangling

To answer my questions I have to look at two different datasources. __tmdb_5000_movies.csv__ contains the movie title and all movie related values. Additionally I have to look at __tmdb_5000_credits.csv__ which includes the complete cast and crew for every movie in the first source. As it includes the complete cast and crew it's size is much bigger than the first one.

### General Properties
#### Movie source


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
movie_df = pd.read_csv('tmdb_5000_movies.csv')
movie_df.head(2)
~~~

![movie_df.head(2)](table_01.png)

~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
movie_df.info()
~~~

~~~ {.text breaklines=true bgcolor=win fontsize=\footnotesize framesep=6mm frame=single rulecolor=att}
Output:


    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 4803 entries, 0 to 4802
    Data columns (total 20 columns):
    budget                  4803 non-null int64
    genres                  4803 non-null object
    homepage                1712 non-null object
    id                      4803 non-null int64
    keywords                4803 non-null object
    original_language       4803 non-null object
    original_title          4803 non-null object
    overview                4800 non-null object
    popularity              4803 non-null float64
    production_companies    4803 non-null object
    production_countries    4803 non-null object
    release_date            4802 non-null object
    revenue                 4803 non-null int64
    runtime                 4801 non-null float64
    spoken_languages        4803 non-null object
    status                  4803 non-null object
    tagline                 3959 non-null object
    title                   4803 non-null object
    vote_average            4803 non-null float64
    vote_count              4803 non-null int64
    dtypes: float64(3), int64(4), object(13)
    memory usage: 750.5+ KB
 ~~~ 

We can see many columns that have rows with NaN values. Regarding my research questions we can drop many columns and this will include every column that contains NaN values.


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
print(type(movie_df['genres'][0]))
~~~

~~~ {.text breaklines=true bgcolor=win fontsize=\footnotesize framesep=6mm frame=single rulecolor=att}
Output:

    <class 'str'>
~~~ 


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
movie_df['genres'][0]
~~~

~~~ {.text breaklines=true bgcolor=win fontsize=\tiny framesep=6mm frame=single rulecolor=att}
Output:

    '[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]'
~~~


There are multiple fields with lists of dicts to describe multiple properties. There are different ways of solving it, like creating columns for every property if it's important for the own examination. I will create functions that can be applied if needed to extract the information on call.

#### Credits source


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
credits_df = pd.read_csv('tmdb_5000_credits.csv')
credits_df.head()
~~~


![credits_df.head()](table_02.png)




~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
credits_df.info()
~~~

~~~ {.text breaklines=true bgcolor=win fontsize=\footnotesize framesep=6mm frame=single rulecolor=att}
Output:

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 4803 entries, 0 to 4802
    Data columns (total 4 columns):
    movie_id    4803 non-null int64
    title       4803 non-null object
    cast        4803 non-null object
    crew        4803 non-null object
    dtypes: int64(1), object(3)
    memory usage: 150.2+ KB

~~~

This source has less columns but much more content in every row. I will cut it down to the desired data only.

### Cleaning __movie_df__


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
movie_df.drop([ 'popularity',
		'overview',
		'tagline',
		'runtime',
		'keywords',
		'genres',
		'budget',
		'homepage',
		'original_language',
		'production_countries',
		'production_companies',
		'release_date',
		'status',
		'title',
		'spoken_languages',], axis=1,inplace=True)
movie_df.head()
~~~


![movie_df.head()](table_03.png)



### Cleaning __credits_df__

The file for this csv is much bigger although it has the same number of columns. The columns __cast__ and __crew__ are containing much more content. They include the complete cast and crew that have created a specific movie. As one question is regarding the cast I will extract only the top five of each movie and dropping the rest.


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
def extract_top_five_cast(val):
    mov_cast = json.loads(val)
    ex_cast = [] 
    for element in mov_cast[:5]:
        cast_id = element['id']
        name = element['name']
        ex_cast.append((cast_id,name))
    return ex_cast
~~~


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
credits_df['top_five'] = credits_df['cast'].apply(extract_top_five_cast)
cast_df = credits_df.drop(['title','cast','crew'],axis=1)
~~~


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
cast_df.rename(columns={'movie_id':'id'},inplace=True)
~~~


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
cast_df.head(1)
~~~


![cast_df.head(1)](table_04.png)


Now it's easy to merge or reference the movie dataframe with the cast dataframe by using the __id__ key.
Moreover I will extract all possible actor IDs for beeing able later on to query all existing actors. I will use a global variable inside the lambda function for collection all occurences of actors and the frequency:


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
actor_name = {}
actor_freq = {} 


def extract_all_ids(row,s=actor_name,m=actor_freq):
    for i in range(0,5):
        try:
            temp_id = row[i][0]
            name = row[i][1]
            if temp_id not in s.keys():
                m[temp_id] = 0
                s[temp_id] = name
            else:
                m[temp_id] = m[temp_id] + 1
        except:
            pass
        
~~~


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
temp = cast_df['top_five'].apply(extract_all_ids)
~~~

Now I will create a Dataframe from the data I extracted. I pushed the data into dicts in the first place as the speed of execution was much higher.


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
actor_df = pd.DataFrame.from_dict(list(actor_name.items()))

~~~


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
actor_df['freq'] = actor_df[0].map(actor_freq)
~~~


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
actor_df = actor_df.rename(columns={0:'actor_id',1:'name'})
~~~


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
actor_df.head(1)
~~~



![actor_df.head(1)](table_05.png)


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
len(actor_df)
~~~

~~~ {.text breaklines=true bgcolor=win fontsize=\footnotesize framesep=6mm frame=single rulecolor=att}
Output:

    9394
~~~


These are to many actors to examine. Especially actors with only a few or a single occurence in a movie could distort the statistical result in the end. Therefore I will extract only the actors with twenty or more occurences in movies.  


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
actor_o20_df = actor_df[actor_df['freq'] >= 20]
actor_o20_df.info()
~~~

~~~ {.text breaklines=true bgcolor=win fontsize=\footnotesize framesep=6mm frame=single rulecolor=att}
Output:

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 100 entries, 2 to 2128
    Data columns (total 3 columns):
    actor_id    100 non-null int64
    name        100 non-null object
    freq        100 non-null int64
    dtypes: int64(2), object(1)
    memory usage: 3.1+ KB
~~~

It's like a magic coincidence that the resulting Dataframe has exactly 100 rows. Sounds like a good result :)

## Exploratory Data Analysis
### Research Question 1: Does movies have better ratings if they're voted more often?

For comparing the __vote_count__ with the __average_rating__ it's necessary to normalize one of this values. I will choose the vote count to normalize as the rating has a defined range between zero and ten:


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
temp = 10*(movie_df['vote_count'] - movie_df['vote_count'].min())
movie_df['vote_count_normalized'] = temp / (movie_df['vote_count'].max() - movie_df['vote_count'].min())
~~~

For getting a more human friendly view into my visualisation I will order the resulting values by one of the examined data series. It will occur, that the least voted movies will have a normalized count equal zero.


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
movie_df_sc = movie_df.sort_values('vote_count')
~~~


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
movie_df_sc['vote_count_normalized'].head()
~~~

~~~ {.text breaklines=true bgcolor=win fontsize=\footnotesize framesep=6mm frame=single rulecolor=att}
Output:

    4307    0.0
    4140    0.0
    4638    0.0
    4118    0.0
    4068    0.0
    Name: vote_count_normalized, dtype: float64
~~~


#### First Plot: Bar Plot with small data extract

I will use only a few values for the bar plot as it occured that adding more values will take very long to compute and the illustration will get worse:


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
# Use this, and more code cells, to explore your data. Don't forget to add
#   Markdown cells to document your observations and findings
fig = plt.figure(figsize=(10,10))

plt.bar(range(1,len(movie_df_sc['vote_average'][-200::])+1),movie_df_sc['vote_average'][-200::])
plt.bar( range(1,len(movie_df_sc['vote_average'][-200::])+1),movie_df_sc['vote_count_normalized'][-200::],alpha=0.7)
plt.title("Correlation between Count of Votings and the associated rating for 200 movies with highest vote count")
plt.xlabel("Index (Sorted by Vote Count)")
plt.ylabel("Rating between 0-10 and Vote Count normalized to same space")

plt.gca().legend(('Vote Average','Normalized Vote Count'))
~~~

![png](output_41_1.png)


I cannot see any relationship between the two plotted series at all. I will calculate the correlation for emphasize or contradict this impression:


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
corr = movie_df_sc['vote_average'].corr(movie_df_sc['vote_count_normalized'])
corr
~~~

~~~ {.text breaklines=true bgcolor=win fontsize=\footnotesize framesep=6mm frame=single rulecolor=att}
Output:

    0.31299740399576015
~~~


#### Second Plot: Default plot with complete data

This means there should be some kind of relationship. I will continue with a default plot and all values:


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
fig = plt.figure(figsize=(10,10))

plt.plot(range(1,len(movie_df_sc)+1),movie_df_sc['vote_average'],'.')
plt.plot(range(1,len(movie_df_sc)+1),movie_df_sc['vote_count_normalized'],'.')
plt.title("Correlation between Count of Votings and the associated rating")
plt.xlabel("Index (Sorted by Vote Count)")
plt.ylabel("Rating between 0-10 and Vote Count normalized to same space")

plt.gca().legend(('Vote Average','Normalized Vote Count'))
~~~

![png](output_45_1.png)


I would say there is some kind of correlation in this visualization. For improving this I will calculate the moving average for the __vote_average__

#### Third Plot: Default Plot with complete data and moving average


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
movie_df_sc['vote_average_rm']=movie_df_sc['vote_average'].rolling(window=10,min_periods=1).mean()
~~~


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
fig = plt.figure(figsize=(10,10))

plt.plot(range(1,len(movie_df_sc)+1),movie_df_sc['vote_average_rm'],'.')
plt.plot(range(1,len(movie_df_sc)+1),movie_df_sc['vote_count_normalized'],'.')
plt.title("Correlation between Count of Votings and the associated averaged rating")
plt.xlabel("Index (Sorted by Vote Count)")
plt.ylabel("Rating between 0-10 and Vote Count normalized to same space")

plt.grid(b=None, which='major', axis='both')

plt.gca().legend(('Vote Average with moving average over 10 values','Normalized Vote Count'))
~~~

![png](output_49_1.png)


With data ordered by the count of votings, a __normalized vote count__ and a moving average over the __vote_average__ gives a clear positive correlation between the count of votings and the rating. Especially the top 300 movies with a __vote_count__ above 2700 show a significant positive correlation.

### Research Question 2:  Is there a correlation between specific actors and the associated movie rating or associated revenue?

For achieving this answer I will collect all movie occurences for the top 100 actors I extracted before:

#### Extract all existing IDs

I will extract all movie occurences by selecting them from the previously created __cast_df__ with a lambda function that will return __True__ if a actor_id exists in the tuple of the 'top_five' actors of a movie. This selection will be pushed onto a list of this selections __actor_frames__ which will be processed afterwards: 


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
type(moviecast_df['top_five'][0][0][0])
~~~

~~~ {.text breaklines=true bgcolor=win fontsize=\footnotesize framesep=6mm frame=single rulecolor=att}
Output:

    int
~~~


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
def process_actor(df_row, actor_id):
    top_five = []
    for tupl in df_row['top_five']:
        top_five.append(tupl[0])
    
    if actor_id in top_five:        
        return True
    else:
        return False
~~~


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
actor_frames = []

for actor_id in actor_o20_df['actor_id']:
    actor_frames.append(cast_df[cast_df.apply(process_actor,axis=1,actor_id=actor_id)]['id'])
    
~~~


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
actor_frames[0]
~~~

~~~ {.text breaklines=true bgcolor=win fontsize=\footnotesize framesep=6mm frame=single rulecolor=att}
Output:

    0       19995
    562      6947
    740      8078
    838      8077
    1053      926
    1178     7461
    1309    10833
    1574     8780
    1804     9092
    2103     8326
    2138     1710
    2153    38303
    2244    77948
    2361    68924
    2391    75638
    2403      679
    2500    73935
    2778     9672
    3056    52067
    3105    25350
    3158      348
    4703    39141
    Name: id, dtype: int64
~~~


The previous step is very costly in terms of needed resources. Actually I'm hosting my Jupyter Notebook on a Raspberry Pi. But this calculation convinced me to change to my personal computer. I would like to know if there are possible measures to reduce this computational cost? 

Now I will calculate the revenues and ratings over all occurences of a single actor by looping through the __actor_frames__. Important is to divide the sum of all values by the frequency of occurence of the actor:


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
actor_result_df = pd.DataFrame(columns=['name','average_rating','average_revenue'])

for i in range(0,len(actor_frames)):
        freq = actor_o20_df.iloc[i]['freq']
        all_ratings = 0
        all_revenues = 0
        for j in range(0,len(actor_frames[i])):
            all_ratings = all_ratings + float(movie_df[movie_df['id'] == actor_frames[i].iloc[j]]['vote_average'])
            all_revenues = all_revenues + float(movie_df[movie_df['id'] == actor_frames[i].iloc[j]]['revenue'])

        all_ratings = all_ratings / freq
        all_revenues = all_revenues / freq
        
        actor_result_df = actor_result_df.append({'name':actor_o20_df.iloc[i]['name'],
						  'average_rating':all_ratings,
						  'average_revenue':all_revenues},ignore_index=True)
        
        
~~~


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
actor_result_df.head(1)
~~~

![actor_result_df.head(1)](table_06.png)



~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
actor_result_df.sort_values(by='average_rating', ascending=False).iloc[0:3]
~~~


![actor_result_df.sort_values(by='average_rating', ascending=False).iloc[0:3]](table_07.md)



#### Top three actors with highest revenue


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
actor_result_df.sort_values(by='average_revenue', ascending=False).iloc[0:3]
~~~

![actor_result_df.sort_values(by='average_revenue', ascending=False).iloc[0:3]](table_08.png)

#### Visualisation of distribuation over all examined actors

Now we want to plot these two values next to each other for getting quick insights about the correlation between the __revenue__ and the __ratings__. As the revenue is much higher than the ratings value, I have to normalize again. I will use the base 10 of the rating again:


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
temp = 10*(actor_result_df['average_revenue'] - actor_result_df['average_revenue'].min())
actor_result_df['revenue_normalized'] = temp  / (actor_result_df['average_revenue'].max() - actor_result_df['average_revenue'].min())
~~~

I would like to print multiple bars for one x-tick and add a label with the actors name on top of each bar. After some research, I found a good example here [Multiple Bars](https://stackoverflow.com/questions/14270391/python-matplotlib-multiple-bars). I modified the function and the plot for my purposes:


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
def autolabel(rects1,rects2,names):
    counter =0
    for rect1,rect2 in zip(rects1,rects2):
        h1 = rect1.get_height()
        h2 = rect2.get_height()
        if h2 > h1:
            h = h2
        else:
            h = h1
        ax.text(rect1.get_x()+rect1.get_width(), 1.05*h, '%s'%names[counter],
                ha='center', va='bottom', rotation='vertical',)
        counter = counter + 1
~~~


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
import numpy

ind = numpy.arange(50)

fig = plt.figure(figsize=(25,10))
width = 0.3

ax = fig.add_subplot(111)

yvals = actor_result_df['revenue_normalized'][0:50]
rects1 = ax.bar(ind,yvals,width)

zvals = actor_result_df['average_rating'][0:50]
rects2 = ax.bar(ind+width, zvals, width)

plt.tick_params(axis='x', which='both', bottom=False, top=False,
    labelbottom=False)

plt.title("Plotting normalized revenue against averaged ratings of top hundred most frequent actors")
plt.ylabel("Rating between 0-10 and Revenue normalized to same space")

plt.gca().legend(('Average Revenue Normalized','Average Rating'))

plt.ylim(0,12)


autolabel(rects1,rects2,actor_result_df['name'])
~~~


![png](output_69_0.png)



~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
actor_result_df['average_rating'].corr(actor_result_df['revenue_normalized'])
~~~

~~~ {.text breaklines=true bgcolor=win fontsize=\footnotesize framesep=6mm frame=single rulecolor=att}
Output:

    0.18375222363390781
~~~


My plot contains only first half of the examined actors for better visibility. We can expose the following results:
  
  * The rating has a uniformly distribution over all actors
  * The average revenue is very uneven distributed, there are actors with very high revenues and actors with very low ones
  * The rating is barely correlated to the revenue. The very small positive correlation value emphasizes this impression. 

## Conclusions


After answering my research questions in full detail I got a much better insight into movie ratings associated to revenues and the involved actors. 

My first research question did show a positive correlation between the count of votings and the rating for a movie. This could mean that a movie that gets more votings will get better ratins at all.

The second research question did highlight that there isn't barely a correlation between the rating and the revenue of a movie. Actually, it just figures for me but it's nice to emphasize this impression in this examination. 
