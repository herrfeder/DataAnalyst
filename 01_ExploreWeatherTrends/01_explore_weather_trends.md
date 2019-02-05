---
linetitle: "Udacity Data Analyst Nanodegree"
title: "01 Explore Weather Trends"
author: David Lassig 
date: 2018-12-17
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

# Project Report

## Extracting Database Data

For extracting the required datasets from the database I used plain SQL queries.
To extract the specific city data I used the following query (my nearest city in the database is Berlin):

~~~
Select * from city_data where city='Berlin';
~~~

Extracting this data gave me the temperature values for Berlin. I placed the resulting file into a Github Repository for beeing accessible from everywhere.
For extracting the global data I simply used:

~~~
Select * from global_data;
~~~
  
I placed the resulting file into a Github Repository too.

## Creating Line Charts and calculating Moving Average
  * I'm using __Python with Pandas__ for Data Processing and __Matplotlib__ for visualizing the data
  * For creating the code and the output I'm using __Jupyter Notebook__ as it allows Visualization between lines of code
  * Advantages of Pandas for this task:
      * Allows very easy data processing and data cleaning by using builtin functions
  * Advantages of Matplotlib for this task:
      * Matplotlib works well together with Pandas specific data structures like Pandas Dataframes
      * moreover it's nicely integrated into Jupyter Notebooks which allows to output my visualization within the script
      * we are able to modify the resulting plot completely to our needs


I'm starting by imported required libraries to going further. I need pandas for data processing and matplotlib for visualizing my resulting data. Additionally I will modify Jupyter Notebook by printing Matplotlib plots inline into the notebook:

~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("ggplot")
%matplotlib inline
~~~

### Reading csv values into variables
  * uploading the data sources to a public location allows flexible data access
  * as I do the whole data processing and visualization with Python it will be the easiest way to read the files with Python too


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
berlin_csv="https://raw.githubusercontent.com/herrfeder/DataAnalyst/master/01_ExploreWeatherTrends/berlin.csv"
global_csv="https://raw.githubusercontent.com/herrfeder/DataAnalyst/master/01_ExploreWeatherTrends/global_data.csv"
berlin_df=pd.read_csv(berlin_csv)
global_df=pd.read_csv(global_csv)

~~~

### Cleaning Data
  * remove NaN values
  * remove unused columns


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
berlin_df = berlin_df.dropna()
berlin_df = berlin_df.drop(['country'],axis=1)
global_df = global_df.dropna()
~~~

### Visualize data (without moving average)


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
fig = plt.figure(figsize=(15,10))

for frame in [berlin_df, global_df]:
    plt.plot(frame['year'], frame['avg_temp'])

plt.title("Global average Temperature compared to Berlin")
plt.xlabel("Year")
plt.ylabel("Temperature in C°")
plt.gca().legend(('Berlin','Global'))
plt.ylim(0,12)
plt.show()
~~~


![First plot without Moving Average](output_8_0.png)


### Calculate moving average
  * we can see that the data without further data processing is very volatile and it's difficult to observe significant trends
  * therefore I'm using the statistical method of calculating the moving average
  * I use the pandas function __rolling__ for calculating the Moving Average by calculating the __mean()__ afterwards
  * setting window to 10 will use 10 values (n-1) to calculate Moving Average over 10 years
  * setting __min_periods__ to 1 allows for not having NaN values at the beginning of our data


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
berlin_df['avg_temp_rm']=berlin_df['avg_temp'].rolling(window=10,min_periods=1).mean()
global_df['avg_temp_rm']=global_df['avg_temp'].rolling(window=10,min_periods=1).mean()
~~~

### Visualize data with moving average


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
fig = plt.figure(figsize=(15,8))

for frame in [berlin_df, global_df]:
    plt.plot(frame['year'], frame['avg_temp_rm'])

plt.title("Global average Temperature compared to Berlin with Rolling Mean over 10 years")
plt.xlabel("Year")
plt.ylabel("Temperature in C°")
plt.gca().legend(('Berlin','Global'))
plt.ylim(4,12)
plt.xlim(1750,2020)
plt.show()
~~~


![Second plot with Moving Average](output_12_0.png)


## Observations from comparhison of Berlin to Global Temperature
  1. Since 1900 it becomes significantly warmer up to the end of the dataset at 2008
      * this observation is valid for Berlin and the global temperature
  2. In Berlin it's circa one degree warmer than in the global average
      * it seems like a relative constant offset between both gradients
  3. From the beginning of the dataset at 1750 to circa 1850 the average temperature is very volatile despite the used moving average
      * this observation is valid for Berlin and the global temperature
  4. In general the city data is more volatile than the global data
      * as the global data is already averaged it has a more smooth gradient
      
## Adding other cities


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
tokyo_csv = "https://raw.githubusercontent.com/herrfeder/DataAnalyst/master/01_ExploreWeatherTrends/tokyo.csv"
newyork_csv ="https://raw.githubusercontent.com/herrfeder/DataAnalyst/master/01_ExploreWeatherTrends/new_york.csv"

tokyo_df = pd.read_csv(tokyo_csv)
newyork_df = pd.read_csv(newyork_csv)

tokyo_df = tokyo_df.dropna()
tokyo_df = tokyo_df.drop(['country'],axis=1)
newyork_df = newyork_df.dropna()
newyork_df = newyork_df.drop(['country'],axis=1)

tokyo_df['avg_temp_rm']=tokyo_df['avg_temp'].rolling(window=10,min_periods=1).mean()
newyork_df['avg_temp_rm']=newyork_df['avg_temp'].rolling(window=10,min_periods=1).mean()

fig = plt.figure(figsize=(15,8))

for frame in [berlin_df,tokyo_df, newyork_df, global_df]:
    plt.plot(frame['year'], frame['avg_temp_rm'])

plt.title("Global average Temperature compared to Berlin, Tokyo and New York with Rolling Mean over 10 years")
plt.xlabel("Year")
plt.ylabel("Temperature in C°")
plt.gca().legend(('Berlin','Tokyo','New York','Global'))
plt.ylim(4,14)
plt.xlim(1750,2020)
plt.show()
~~~


![Comparing multiple cities](output_14_0.png)

 

## Correlation Coefficient between Berlin and other cities
  * we can calculate the correlation coefficients for exposing similarities between several trends
  * a higher Coefficient means a higher similarty


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
berlin_df.corrwith(global_df)
~~~

~~~ {.text breaklines=true bgcolor=win fontsize=\footnotesize framesep=6mm frame=single rulecolor=att}
Output:

    year           1.000000
    avg_temp       0.388924
    avg_temp_rm    0.653210
    dtype: float64

~~~



~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
berlin_df.corrwith(newyork_df)
~~~


~~~ {.text breaklines=true bgcolor=win fontsize=\footnotesize framesep=6mm frame=single rulecolor=att}
Output:

    year           1.000000
    avg_temp       0.484634
    avg_temp_rm    0.824458
    dtype: float64
~~~


~~~ {.python breaklines=rue bgcolor=bg fontsize=\tiny}
berlin_df[107::].corrwith(tokyo_df)
~~~

~~~ {.text breaklines=true bgcolor=win fontsize=\footnotesize framesep=6mm frame=single rulecolor=att}
Output:

    year           1.000000
    avg_temp      -0.155808
    avg_temp_rm    0.028070
    dtype: float64
~~~



## Observation over multiple Cities to Global Temperature
  1. The gradients for Berlin and New York have many similar peaks but especially before 1900 they are very different.
      * we have to notice a general offset of one degree between New York and Berlin
  2. Regarding the Correlation we can see that New York has the most similar temperature trend compared to Berlin.
  3. Tokyo has the most different temperature trend compared to Berlin


# Appendix

## Full code 

~~~ {.python breaklines=true bgcolor=bg fontsize=\tiny linenos=true}
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("ggplot")
get_ipython().run_line_magic('matplotlib', 'inline')


berlin_csv="https://raw.githubusercontent.com/herrfeder/DataAnalyst/master/01_ExploreWeatherTrends/berlin.csv"
global_csv="https://raw.githubusercontent.com/herrfeder/DataAnalyst/master/01_ExploreWeatherTrends/global_data.csv"
berlin_df=pd.read_csv(berlin_csv)
global_df=pd.read_csv(global_csv)

berlin_df = berlin_df.dropna()
berlin_df = berlin_df.drop(['country'],axis=1)
global_df = global_df.dropna()


fig = plt.figure(figsize=(15,10))

for frame in [berlin_df, global_df]:
    plt.plot(frame['year'], frame['avg_temp'])

plt.title("Global average Temperature compared to Berlin")
plt.xlabel("Year")
plt.ylabel("Temperature in C°")
plt.gca().legend(('Berlin','Global'))
plt.ylim(0,12)
plt.show()


berlin_df['avg_temp_rm']=berlin_df['avg_temp'].rolling(window=10,min_periods=1).mean()
global_df['avg_temp_rm']=global_df['avg_temp'].rolling(window=10,min_periods=1).mean()

fig = plt.figure(figsize=(15,8))

for frame in [berlin_df, global_df]:
    plt.plot(frame['year'], frame['avg_temp_rm'])

plt.title("Global average Temperature compared to Berlin with Rolling Mean over 10 years")
plt.xlabel("Year")
plt.ylabel("Temperature in C°")
plt.gca().legend(('Berlin','Global'))
plt.ylim(4,12)
plt.xlim(1750,2020)
plt.show()



tokyo_csv = "https://raw.githubusercontent.com/herrfeder/DataAnalyst/master/01_ExploreWeatherTrends/tokyo.csv"
newyork_csv ="https://raw.githubusercontent.com/herrfeder/DataAnalyst/master/01_ExploreWeatherTrends/new_york.csv"

tokyo_df = pd.read_csv(tokyo_csv)
newyork_df = pd.read_csv(newyork_csv)

tokyo_df = tokyo_df.dropna()
tokyo_df = tokyo_df.drop(['country'],axis=1)
newyork_df = newyork_df.dropna()
newyork_df = newyork_df.drop(['country'],axis=1)

tokyo_df['avg_temp_rm']=tokyo_df['avg_temp'].rolling(window=10,min_periods=1).mean()
newyork_df['avg_temp_rm']=newyork_df['avg_temp'].rolling(window=10,min_periods=1).mean()

fig = plt.figure(figsize=(15,8))

for frame in [berlin_df,tokyo_df, newyork_df, global_df]:
    plt.plot(frame['year'], frame['avg_temp_rm'])

plt.title("Global average Temperature compared to Berlin, Tokyo and New York with Rolling Mean over 10 years")
plt.xlabel("Year")
plt.ylabel("Temperature in C°")
plt.gca().legend(('Berlin','Tokyo','New York','Global'))
plt.ylim(4,14)
plt.xlim(1750,2020)
plt.show()


berlin_df.corrwith(global_df)
berlin_df.corrwith(newyork_df)
berlin_df[107::].corrwith(tokyo_df)

~~~

