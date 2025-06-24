Title: PA Well Water, Part 4
Date: 2025-6-10
Modified: 2025-06-18
Category: Science
Tags: analysis

# Introduction
This post continues from [Part 3]({filename}./PA_wells_3.md) and covers the
Bayesian profile regression model.

# Bayesian Profile Regression
## What Is It?
There were several resources I used to get a grasp on the method. Molitor et 
al. [^2] present kind of the founding proposal of the method, and this is a 
surprisingly readable paper. [^3] and [^4] were helpful in my understanding 
the spatial component that can be added to these models. [^5] was helpful as 
yet another writeup of the method, and especially for including a DAG of the 
full model.

There is an R package for this method, called PReMiuM, which I will
henceforth call Premium, because fuck that. 

It took me a little while to understand how this method works. The gist is
that you fit a joint model of a clustering component and a regression
component. For each observation, its cluster assignment acts as a
categorical predictor[^1] for the regression on your outcome variable. The
joint nature of the model means that the outcome variable influences 
clustering. I know that's confusing to read. Just read through those sources I 
listed. 

Molitor lists four benefits of the method, which I will summarize/combine:

  - The benefits of Bayesian methods re uncertainty and posterior analyses.
  - The clustering method that it uses lets the model figure out how many 
    there should be, rather than requiring you to pre-specify[^6].
  - "the outcome and the clusters mutually inform each other".

That last point is the crux of my issue with this SVI paper.

## Why Use It?
Molitor proposes it as a complement/alternative to standard regression:

> Standard regression analyses are often plagued with problems encountered when one tries to make meaningful inference going beyond main effects, using datasets that contain dozens of variables that are potentially correlated.

I guess one might say that the world isn't made up of convenient little 
lines. This method works around this problem by:

> adopt a more global point of view, where inference is based on clusters representing covariate patterns as opposed to individual risk factors.

Re regression vs profile regression, Molitor concludes with:

> Since the two approaches address different characteristics of association, both should be used in a complementary fashion to progress our understanding of the association between an outcome and a set of correlated covariates.

Another nice explanation is the Introduction in Belloni[^5], which also 
(briefly) compares it to other methods that might do a similar thing, such 
as random forests or principal component regression. 

## Comments
It doesn't seem to be a super popular analysis method. I noticed a lot of 
repeat names on the papers I looked at. I suspect a lot of people are 
reaching for machine learning methods.

# The Problem
Per Wamsley:

> we did not include the response model when determining clusters because domestic well prevalence is clustered by county, and the BPR does not allow for such spatial clustering effects modeling. Instead, the clusters of exposure profiles were fit in a second-stage multilevel regression model to estimate the relationship between social vulnerability profiles with domestic well prevalence

I take this to mean that there were two steps, the clustering and the 
regression, but importantly, they were separate things entirely, meaning the 
regression model had zero influence on the clustering. However, Bayesian 
profile regression is 
supposed to fit these components jointly. Per Molitor:

> [it] fits the model as a unit, allowing an individual’s outcome to 
> potentially influence cluster membership

And to hear it from another source [^5]:

> one of the principal motivations for PRM models is that the disease outcome influences cluster membership so that they can inform each other.

And to hear it from yet another source [^7] (the middle two intro paragraphs 
might be good to read):

> it may be desirable to make use of (potentially highly informative) 
> outcome information directly, in order to guide inference toward the most 
> relevant clustering structures. That is, we may wish to use the outcome 
> information during the clustering analysis itself, rather than during post-analysis validation. This
> is one of the principal motivations for Bayesian profile regression

This change can cause radically different clustering.

## Toy Example
I'll fit two models: one as a standard Bayesian profile regression, the 
second just the covariate clustering aspect as might happen in a two-phase 
modeling approach as I think Wamsley used. 

Here is some simulated data of a 
Poisson outcome with a couple of correlated predictors:

    :::r
    set.seed(3)
    
    N = 700
    x1 = rnorm(N, 8, 2)
    # get a second distinct cluster
    x2 = (x1 + rnorm(N, 1, .5)) * ifelse(rbinom(N, 1, ifelse(x1> 10, 0.8, 1)) == 0, 0.5, 1)
    y = rpois(N, x1 + x2)
    dummy_col = 1  # for "offset" (+ log(dummy_col) as pred ==> + log(1) == + 0 on rhs of glm)
    obs_dat = data.frame(y, x1, x2, dummy_col)


You can see how it looks with `pairs(obs_dat[,1:3])`:

![Figure 1]({static}/images/science/well_water/pairs_plot.png)

### Standard Bayesian Profile Regression Usage
Fitting it with Premium:

    :::r
    mod_includeY = PReMiuM::profRegr(
      yModel="Poisson",
      xModel="Normal",
      outcomeT = "dummy_col",
      nClusInit=5,
      # excludeY = TRUE,
      data=obs_dat,
      output="pois_includeY",
      covNames = c("x1", "x2"),
      outcome = "y",
      seed=12345
    )

The clustering looks like so:

![Figure 2]({static}/images/science/well_water/include_y_1.png)
![Figure 3]({static}/images/science/well_water/include_y_2.png)

This output shows the two main things about this method:

  1. The separate purple cluster in the x1 vs x2 plot shows that if the 
     covariate profiles are distinct, they will be clustered separately even 
     if the outcomes are similar (see how purple and blue/green are mixed in 
     the plot of x1 vs y).
  2. The regression component (`yModel="Poisson"`), *NOT* the y data per 
     se!,
     splits up the oblong 
     cluster into roundish 
     blobs. The 
     red/green/blue section is obviously one big cluster as viewed on x1 vs 
     x2's plot, 
     but using it as a 
     predictor for y would yield terribly wide predictions. The y data as 
     part of the linear model
     provides evidence that this one big cluster might be better off split 
     up, as happens here. 

### Excluding the y Linear Model Component
Now we use the `excludeY` argument to essentially just cluster via the 
covariates ([I think](https://github.com/silvialiverani/PReMiuM-R-package/issues/13)):

    :::r
     mod_excludeY = PReMiuM::profRegr(
       yModel="Poisson",
       xModel="Normal",
       outcomeT = "dummy_col",
       nClusInit=5,
       excludeY = TRUE,
       data=obs_dat,
       output="pois_excludeY",
       covNames = c("x1", "x2"),
       outcome = "y",
       seed=12345)

Which yields:

![Figure 4]({static}/images/science/well_water/exclude_y_1.png)
![Figure 5]({static}/images/science/well_water/exclude_y_2.png)

So now we see that the big oblong cluster stays in one piece. y's linear model 
isn't there 
to influence it to split up. Note that this clustering remains (in this case)
even if we add y into `covNames` like `covNames = c("x1", "x2", "y")`: the clustering just says "yep, that's a 
cluster", because it doesn't have the linear model to tell it that this 
clustering yields poor predictions. I didn't include that output because it 
looks the same as this.

## So.. What's the Issue in This Case?
Cluster 15.

Cluster 15 winds up having the highest expected users of well water per 
their model. However,
empirically it is comprised of census tracts with:

  - A median of 0 houses with wells.
  - A 3rd quartile of 12 houses with wells.

In Bayesian profile regression, those census tracts in Cluster 15 with high 
well usage (which is at most a 
quarter of said tracts) ought to be a separate cluster, and would be under a 
joint model as Bayesian profile regression implements. They might have 
similar covariate profiles, but the clustering would be (probably quite) 
different.

I think that the adjustment for county must have done some heavy lifting to 
get Cluster 15 into the top spot. Maybe something like the tracts with lots 
of well users were in counties with generally low well usage? 

# Conclusion
I think I've made a good argument for there being a mistake in the analysis. 
At least, for them not yielding results that Bayesian profile regression 
should yield (not that profile regression is "the truth").
Perhaps I've misread/misinterpreted their methods, but the wonkiness of 
Cluster 15 matches with what would go differently in a joint vs 2-phase model.

Next I suppose I ought to try and do the analysis with a joint model. See 
how that goes.



[^1]: Well, Molitor in [^2] says "The previously described assignment model 
clusters individuals into groups and these cluster assignments can be 
simultaneously used as categorical predictors of an outcome.", however when 
I said this to *the* Liverani of Premium fame, she said [that I was wrong](https://github.com/silvialiverani/PReMiuM-R-package/issues/13#issuecomment-2838078844). I'm sticking with Molitor on this one.
[^2]: Molitor, J., Papathomas, M., Jerrett, M., Richardson, S., 2010. 
Bayesian profile
regression with an application to the National survey of children’s health.
Biostatistics 11, 484–498. https://doi.org/10.1093/biostatistics/kxq013.
[^3]: Silvia Liverani, Aurore Lavigne, Marta Blangiardo, Modelling collinear and spatially correlated data, Spatial and Spatio-temporal Epidemiology, Volume 18, 2016, Pages 63-73, ISSN 1877-5845, https://doi.org/10.1016/j.sste.2016.04.003. (https://www.sciencedirect.com/science/article/pii/S1877584515300411)
[^4]: Coker ES, Molitor J, Liverani S, Martin J, Maranzano P, Pontarollo N, et al. Bayesian profile regression to study the ecologic associations of correlated environmental exposures with excess mortality risk during the first year of the Covid-19 epidemic in lombardy, Italy. Environ Res 216(Pt 1):114484. Available from: https://europepmc.org/articles/PMC9547389 https:// doi.org/10.1016/j.envres.2022.114484 PMID: 36220446
[^5]: Belloni M, Laurent O, Guihenneuc C and Ancelet S (2020) Bayesian 
Profile Regression to Deal With Multiple Highly Correlated Exposures and a Censored Survival Outcome. First Application in Ionizing Radiation Epidemiology. Front. Public Health 8:557006. doi: 10.3389/fpubh.2020.557006 
[^6]: The Dirichlet process mixture model (DPMM), which you can learn about 
on [PyMC](https://www.pymc.io/projects/examples/en/latest/mixture_models
/dp_mix.html) or see a detailed mathematical walkthrough for the 
non-statistician [here](https://pmc.ncbi.nlm.nih.gov/articles/PMC6583910/). 
Those resources helped me, at least.
[^7]: Anaïs Rouanet, Rob Johnson, Magdalena Strauss, Sylvia Richardson, Brian D Tom, Simon R White, Paul D W Kirk, Bayesian profile regression for clustering analysis involving a longitudinal response and explanatory variables, Journal of the Royal Statistical Society Series C: Applied Statistics, Volume 73, Issue 2, March 2024, Pages 314–339, https://doi.org/10.1093/jrsssc/qlad097

## Links
[Part 1]({filename}./PA_wells_1.md) [Part 2]({filename}./PA_wells_2.md)
[Part 3]({filename}./PA_wells_3.md) [Part 5]({filename}./PA_wells_5_analysis_1.md)
[Part 6]({filename}./PA_wells_6_analysis_2.md)
