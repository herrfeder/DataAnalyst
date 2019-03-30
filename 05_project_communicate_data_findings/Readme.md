# Communicate Data Findings for PISA 2012 Studies
## by David Lassig


## Dataset

The PISA dataset of 2012 shows the effort of the OECD giving reasonable test results to argue about academic performance of school children in dependency to many different factors. This dataset is huge as it holds 485490 observations by using 636 different columns for several tests. It includes results from questionaires regarding:
  * home environment students
  * parental environment of students
  * condition of the school
  * the habits and practices of the teacher
  * test results from science-oriented tests<br/><br/>

Therefore it's crucial to cut only a few interesting columns from this dataset. I've used this [document](http://www.oecd.org/pisa/pisaproducts/PISA12_stu_codebook.pdf) to get a explanation for the     partly cryptic column names. It's one of the codebooks next to some others that are exclusively designed for the purpose to explain the different columns.


## Summary of Findings

I focused on the math achievements represented by two variables "Math Self-Efficacy" and "Math Familiarity" I calculated from seperate groups of categorical questions to get a more meaningful single number. I tried to point out several relationship to other variables:

### Are there differences in math achievement based on gender, nationality, wealth or student attitudes?

I was able to point out a very strong relationship between the nationality and the math achievements. There are some countries, whom students did perform significantly bad like Sweden and others like China that did perform very good. I didn't create a gender and math achievement exclusive plot but as this variable is included in my Multivariate plots multiple times, I assume there is nearly no difference between boys and girls for math achievements. The plot for Wealth compared to Math familiarity and the associated correlation doesn't show any correlation. For measuring the student attitudes I did only extract their commitment towards visiting school by their frequency of coming late or skipping whole school days. Obviously the distribution for students that are missing classes more often is slightly higher for the areas with bad Math Familiarity but that isn't really significant.

### Are there differences in math achievement based on teacher practices and attitudes?

Teacher practices did only affect the Interest and the Motivation for math but not the achievement represented by Math Self-Efficacy and Math Familiarity at all.

### Are there differences in math achievement based on parents education or parents job?

The dependency of the highest schooling graduation shows a small relationship to Math Achievement e.g. Math Familiarity. Especially the highest gradiuation shows distributions with higher amounts of good Math Familiarity and the lowest graduation bigger amounts of students in the lowest areas of Math Familiarity. The dependency of the parents job to Math Familiarity shows a stronger relationship. If the mother or the father have a job that are related to mathematical issues, there is a higher amount of students that have better Math Achievements. 

## Key Insights for Presentation

In my presentation I will include a visual correlation matrix to show the correlations of my main features and point out that there are only a few intermediate relationships between them. Moreover I will include the strongest relationship I was able to find, the dependency of the Math Familiarity from the Nation the student is living in. The third and last visualisation shows the influence of the parents job on the students Math Familiarity.