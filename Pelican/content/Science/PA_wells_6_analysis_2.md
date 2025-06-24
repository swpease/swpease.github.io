Title: PA Well Water, Part 6: Analyzing the Data
Date: 2025-6-23
Category: Science
Tags: analysis

# Introduction
This post continues from [Part 5]({filename}./PA_wells_5_analysis_1.md). At 
long last, we've got our pieces in place. Time to plug it into our 
processing method!

# Method
The actual code for what follows is [here](https://github.com/swpease/well_water/blob/master/R/BPR_CAR.Rmd).

I used the following clustering covariates: "EP_POV150", "EP_UNEMP", 
"EP_NOHSDP", "EP_AGE65", "EP_AGE17", "EP_MINRTY", "EP_HBURD". These are the 
Estimated Percentage of the population that is: below 150% poverty, 
unemployed, without a high school diploma, over 65, under 17, minority, and housing cost-burdened
occupied housing units with annual income less than $75,000 (30%+ of income 
spent on housing costs). The housing burden is new, and replaces the median 
income component that was used in Wamsley, and poverty has changed from 100% 
to 150% federal poverty level. See the SVI 2020 documentation for 
details (SVI 2020 Updates section).

The outcome variable (estimated # of well water users) and confounder (population density) are 
described in the bulleted list, below.

I diverged from Wamsley in a few places. First, some SVI indicators changed 
(see above). I also excluded the three non-SVI ACS covariates, since they were 
non-SVI. I also considered the population density to be an alternative to 
county, so excluded county.

I used the Premium package (officially spelled obnoxiously) for the Bayesian 
profile regression with conditional autocorrelation. I performed the 
following preprocessing:

  - removed census tracts with estimated populations of zero (both via ACS 
    and via CEISIN)
  - generated an INLA file for the CAR component
  - created the outcome, estimated # of well water users, by multiplying the 
    ACS population estimate (`E_TOTPOP`) by the fraction of the 
    population-as-calculated-by-CEISIN-maps (see prior blog post) that 
    relies on well water
  - created the population density, as tract population divided by land area 
    (`E_TOTPOP` / `ALAND`), to use as a confounder for the outcome component 
    of the model
  - replaced the `-999` encodings for missing clustering covariates data with 
    `NA`s
  - converted the clustering covariates into quartiles
    - Premium can handle discrete or Gaussian cases, and these are not Gaussian.

So the final model's outcome component (i.e. excluding the clustering bit) 
looks like:

$$ 
  y_i \sim Poisson(\mu_i) \\
  log(\mu_i) = \theta_{Z_i} + \beta\rho_i + log(n_i) + u_i
$$

Well, I actually used a negative binomial model, but whatever. Anyway, so 
$\mu_i$ is the expected number of well water users. 
$\theta_{Z_i}$ is a categorical predictor (a random/varying intercept I 
think), with $Z_i$ indicating the group to which $y_i$ belongs. 
$\beta\rho_i$ is the confounder, population density acting to capture rurality. 
$log
(n_i)$ 
is the offset ($n_i$ is the total census tract population). $u_i$ is 
the 
spatially structured error term. 

# Results
Tada!... :(

![Figure 1]({static}/images/science/well_water/clusters.png)

Wait, what? Did I do something wrong? Well, I can't for sure say "No.", but I 
subsequently tried a [bunch of different modifications](https://github.com/swpease/well_water/tree/master/R) to the BPR to try and 
get some sort of clustering. No luck.

# What Happened?
So I finally did what I'd ordinarily do right off the bat: plot my data. 
I'll look at the clustering covariates each against the fraction of the 
census tract that is thought to rely on well water. That should do the trick!
Let's see:

![Figure 2]({static}/images/science/well_water/eppov150.png)

Oh dear. Well, maybe the other covariates look better?

![Figure 3]({static}/images/science/well_water/other_clustering_covs.png)

Hm. Not exactly the "complex and non-linear" relationships I was led to 
believe existed. Well maybe it's something 
that takes multiple 
dimensions to see. How about a PCA biplot [^1]?

![Figure 4]({static}/images/science/well_water/biplot.png)

It's quite blobby. I suppose it at least indicates that there's some 
positive relationship between being old and using well water. That ties out 
with rural populations being a bit older.

All I can really see in the plots against the proportion of well water users 
("frac_WW_CEISIN") is that the boundaries are driving any correlations. The 
fully urban (fully on a PWS) areas span the range of values for every 
predictor, and the 
fully rural (fully on well water) areas also have a somewhat wider range of 
values compared to the intermediate values.

# Discussion
Well that was a let-down. I'm not sure where I might have gone wrong. If I 
didn't make any mistakes, then how the heck did they pull off their results? 
I keep double checking my variables. Like in this post, I keep thinking, "the 
fraction of well water users is the right y-axis variable, right?".

I suppose it's of interest that well water users in PA run the gamut with 
respect to social vulnerability indicators.

Um... I guess at least I learned some things.

[^1]: I haven't use one of these in a while, so had to refresh on the 
details. I found two good sources were a [SAS blog post](https://blogs.sas.com/content/iml/2019/11/06/what-are-biplots.html) and the [{ggbiplot} docs](https://friendly.github.io/ggbiplot/reference/ggbiplot.html). The displayed 
plot is actually from {ggfortify}, using its autoplot, 
but all the plots I toyed around with look virtually the same.

## Links
[Part 1]({filename}./PA_wells_1.md) [Part 2]({filename}./PA_wells_2.md)
[Part 3]({filename}./PA_wells_3.md) [Part 4]({filename}./PA_wells_4.md)
[Part 5]({filename}./PA_wells_5_analysis_1.md)
