Title: Randomized Quantile Residuals
Date: 2024-12-11
Category: Statistics
Tags: statistics

# Introduction
This post should hopefully be helpful for people like me who aren't 
statisticians, but can work with R decently.

While working with count data, I encountered a new type of residual 
(apparently there's different types) 
called the "randomized quantile residual" (RQR).
RQRs essentially convert your residuals such that you can interpret them 
just like plain old residuals from a regular old linear model.

I tried reading the [original paper](https://www.researchgate.
net/publication/2647151_Randomized_Quantile_Residuals) and was left confused 
by the math notation. So I found a [second paper](https://pubmed.ncbi.nlm.
nih.gov/32611379/) yet remained unenlightened. So I finally just looked at 
the [implementation](https://rdrr.io/cran/statmod/src/R/qres.R) and thought, 
"That's it?" So I understood how it worked, but not *why* it worked. Until 
now (I think), when I played around with distributions in R some.

# The Underlying Principle
What percent of the time do you expect to see something in the bottom 0-10th 
percentile? The 80-90th percentile? The 30-60th percentile? If you answered 
"10. 10. 30.", congratulations, you understand the underlying principle. Put 
another way, **if you bin your data into [quantiles](https://en.wikipedia.
org/wiki/Quantile), 
each quantile should have about the same number of observations in it.** In 
retrospect, this is basic stats, but it's the type of thing you forget about 
after years of it never coming up. 

In 
small enough bins and infinite data, you should wind up with a **Uniform 
distribution.**

## Converting to Uniform
Here are a couple of examples of going from some continuous distribution to 
these equal bins.

First, simulated Exponentially distributed data, binned into however many bins 
`hist` uses by default. If you forget / don't know `rexp` vs `pexp` vs 
`qexp`, etc., [here](https://www.reddit.
com/r/RStudio/comments/1bwthox/can_anyone_please_explain_to_me_the_difference
/) is a useful explanation.

```{r}
simdat = rexp(n=10000, rate = 3)
hist(pexp(simdat, rate = 3))
```

![Figure 1]({static}/images/statistics/rqrs/basic_uniform_ex.png)

Second, simulated Beta distributed data:

```{r}
simdat = rbeta(n=10000, 8, 13)
hist(pbeta(simdat, 8, 13))
```

![Figure 2]({static}/images/statistics/rqrs/basic_uniform_ex2.png)

## Converting Back
Once you're at the uniform distribution, you can go back to your starting 
distribution, or any other continuous distribution (it's not like 
the uniform distribution knows where it came from). **The second option is 
used in RQRs: they're converted to Normal from some unfriendly distribution 
(e.g. Poisson) via the Uniform.**

These two histograms are equal (not shown):

```{r}
simdat = rbeta(n=10000, 8, 3)
hist(simdat)
hist(qbeta(pbeta(simdat, 8, 3), 8, 3))
```

Going to a different distribution:

```{r}
simdat = rbeta(n=10000, 8, 3)
simdat2 = rexp(n=10000, rate = 3)
hist(simdat2)
hist(qexp(pbeta(simdat, 8, 3), rate = 3))
```

![Figure 3]({static}/images/statistics/rqrs/exp_rate_3.png)

![Figure 4]({static}/images/statistics/rqrs/beta_to_exp.png)

# Misspecification
This uniformness only happens if your data is accurately represented by the 
CDF you choose (i.e. the `p` functions in R). For instance, in the first 
example, my data came from an Exponential distribution with a rate of 3, and 
the CDF I used just copied over that knowledge. But what if it was different?

What if our CDF was off?

```{r}
simdat = rexp(n=10000, rate = 3)
hist(pexp(simdat, rate = 4))
```

![Figure 5]({static}/images/statistics/rqrs/exp_misspec1.png)

Not so good.

What if we picked an entire wrong distribution?

```{r}
simdat = rexp(n=10000, rate = 3)
hist(pnorm(simdat))
```

![Figure 6]({static}/images/statistics/rqrs/exp_misspec2.png)

Woof.

**The RQRs pick up this non-uniformity so your residuals will look off when 
you convert them to Normal.**

# What About Discrete Data?

The main purpose of using RQRs! Let's see what happens when we do that CDF 
conversion with Poisson data:

```{r}
library(ggplot2)

simdat = rpois(n=10000, lambda = 3)
cdf_dat = ppois(simdat, lambda = 3)
plot_dat = data.frame(table(cdf_dat))
# https://stackoverflow.com/questions/3418128/how-to-convert-a-factor-to-integer-numeric-without-loss-of-information
plot_dat$cdf_dat = as.numeric(as.character(plot_dat$cdf_dat))

ggplot(plot_dat, aes(x=cdf_dat, y=Freq)) +
  geom_point() +
  geom_segment(aes(x=cdf_dat, xend=cdf_dat, y=0, yend=Freq))
```

![Figure 7]({static}/images/statistics/rqrs/pois_cdf_hist.png)

That's not flat. But, the counts of each bin are proportional to the 
proportion of the [0,1] range they encompass. **RQRs work around this by 
taking a random number between the CDF at the observed value and CDF at one 
less than the 
observed value.** For instance, if you observe 1 (corresponding to the line at 
~0.2), which should happen about (0.2 - 0.05) proportion of the time (note 
the count (Freq) is 1500, i.e. 15% of the total 10,000 samples drawn. Also, 
0.05 
is roughly the CDF value for observed = 0, the leftmost line), you get a random 
number between 
roughly 0.05-0.2. So, ~15% of the time you get randomly selected values in this 
~15% range.

Again, this is predicated on a Poisson distribution being appropriate for 
your data, and deviations will show up via non-Normal looking RQRs.

Here is some code that might help to play around with:

```{r}
library(tibble)

n = 100000
lambda = 3

simdat = tibble(
  draw = rpois(n = n, lambda = lambda),
  quantile = ppois(draw, lambda = lambda),
  quantile_q_minus_1 = ppois(draw - 1, lambda = lambda),
  quantile_diff = quantile - quantile_q_minus_1,
  random_quantile = runif(n = n, quantile_q_minus_1, quantile),
  corresponding_normal_val = qnorm(random_quantile)
)
```