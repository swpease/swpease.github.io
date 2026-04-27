Title: Count Data Model Options
Date: 2025-7-9
Category: Statistics
Tags: statistics

# Introduction
In going through that ill-fated analysis of [Pennsylvania well water](
{filename}./PA_wells_1.md), I plotted the actual count data of (# of well users) in each census tract. There were an awful lot of zeroes: overall 46% of census tracts, more specifically 14% of rural and 59% of urban tracts. The histograms look like:

![Figure 1]({static}/images/statistics/count_data/PA_wells_hists.png)

Clearly a lot of small numbers.

With that in mind, I started looking into the various count models. 
Specifically, Poisson, negative binomial, and zero inflations of those, plus 
I learned about the existence of hurdle models. I am mostly just putting 
together some resources here for reference in case I need to use such models 
in the future.

Speaking of the PA well water analysis, the profile regression in Premium 
provides only an overdispered Poisson (i.e. negative binomial) model. That 
is, it does not have a model for excess zeroes. It appears that making new 
variations of a profile regression is non-trivial (e.g. [here](https://academic.oup.com/jrsssc/article/73/2/314/7382190) and [here](https://pmc.ncbi.nlm.nih.gov/articles/PMC7652768/)), but based on my 
attempting to fit a model without any of the zero cases, the unsuitability 
of the available models was not what derailed the analysis.

# References
1. [Zero-inflated and Hurdle Models of Count Data with Extra Zeros: Examples 
   from an HIV-Risk Reduction Intervention Trial](https://pmc.ncbi.nlm.nih.gov/articles/PMC3238139/)
2. [Standard negative binomial regression when counts are mainly zeros?](https://stats.stackexchange.com/questions/651155/standard-negative-binomial-regression-when-counts-are-mainly-zeros)
3. [What is the difference between zero-inflated and hurdle models?](https://stats.stackexchange.com/questions/81457/what-is-the-difference-between-zero-inflated-and-hurdle-models)
4. [Is a "hurdle model" really one model? Or just two separate, sequential models?](https://stats.stackexchange.com/questions/320924/is-a-hurdle-model-really-one-model-or-just-two-separate-sequential-models)
5. [Gavin Simpson blog: rootograms](https://fromthebottomoftheheap.net/2016/06/07/rootograms/)

