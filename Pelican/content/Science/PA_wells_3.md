Title: PA Well Water, Part 3
Date: 2025-6-9
Modified: 2025-06-24
Category: Science
Tags: analysis

# Introduction
This post continues from [Part 2]({filename}./PA_wells_2.md) and covers the 
model's accounting for rurality.

The authors write:

 > rural areas will have more domestic wells.
 
Which makes sense and is what I would presume, but their citation for said 
claim doesn't seem to say that(? I just did a search for "rural" and "well" 
in the reference and didn't see anything). In any case, the [CDC says so](https://www.cdc.gov/environmental-health-services/php/water/private-water-public-health.html).

With that in mind, the authors don't seem to account for rurality as a 
confounder. They use county, which I suppose is related to rurality. I'll go 
over their model, and propose adding a rurality covariate in the form of 
census tract population density. I'll also discuss population density with 
respect to their chosen outcome, count of houses using domestic wells by 
census tract.

At this point I think I should make it clear that I haven't read up on and 
am mostly unfamiliar with 
spatial data regression, so I may be doing obviously dumb things.

## What is rurality?
It's a word we all know the meaning of, but there is a rather detailed set of 
criteria for 
what constitutes an "urban 
area", per the [US Census Bureau](https://www.govinfo.
gov/content/pkg/FR-2022-03-24/pdf/2022-06180.pdf). There are a lot of 
details, but the gist is:

> The Census Bureau’s urban areas represent densely developed territory, and 
> encompass residential, commercial, and other non-residential urban land 
> uses. The boundaries of this urban footprint have been defined using 
> measures based primarily on population counts and residential population 
> density, and also on criteria that account for non-residential urban land 
> uses, such as commercial, industrial, transportation, and open space that 
> are part of the urban landscape.

## Some Useful References
The [Center for Rural Pennsylvania](https://www.rural.pa.gov/home) 
(apparently that's a thing) has some nice resources about rural PA, and in 
comparison to urban PA, for instance [Quick Facts](https://www.rural.pa.gov/data/rural-quick-facts) is good to look through, and [A Report on PA 
Population Decline](https://www.rural.pa.gov/download.cfm?file=Resources/PDFs/Pennsylvania%27s%20Population%20is%20Declining%20Faster%20Than%20Expected%20Fact%20Sheet%20Web.pdf).

# DAGs
I think it's worthwhile to explicitly make some DAGs (using [daggity](https://www.dagitty.net)) to 
get an 
idea of 
causality and confounding possibilities. For an introduction on the subject, 
the [Statistical Rethinking](https://github.
com/rmcelreath/stat_rethinking_2024/tree/main?tab=readme-ov-file) lectures 
go over it (especially lectures 5 and 6). I'll build up from the simplest 
ones, piece by piece.

As a reminder, the primary aim of the statistical analysis in this paper is 
to find "profiles" of SVI (as determined by clustering in a Bayesian profile 
regression) that are used to predict reliance on well water, and to 
characterize those profiles.

## DAG 1: Adding County
The first DAG is just the predictor of interest (SVI cluster), the outcome 
(well water), and the confounder "county" that they use in the paper:

![Figure 1]({static}/images/science/well_water/dag1.png)

To be explicit about some possible causal mechanisms, I'll propose that:
  
  - County => SVI: characteristics of a county (e.g. laws) 
    can alter demographic profiles.
  - County => Well water: counties may have different regulations on water 
    rights.


## DAG 2: Adding Spatial Correlation
The second DAG adds in a spatial autocorellation term, as they did in the 
paper. See [^1] and [^2]. Per [^1], the purpose of such a term is:

> space is used as a proxy for any unmeasured variable; the common 
> assumption is that areas which are close to each other are more similar 
> than those further apart, suggesting that an additional source of 
> correlation, namely spatial correlation needs to be accommodated in the models.

In this case, I'm thinking of underlying geology (aquifers, aquitards, etc.).
The DAG might look like:

![Figure 2]({static}/images/science/well_water/dag2.png)

Again, to be explicit about some possible causal mechanisms, I'll propose that:

- Location => SVI: location, location, location. It can alter demographic profiles.
- Location => Well water: The aforementioned geology issues (e.g. aquifers, 
  are you in a desert?).

## DAG 3 (Proposal): Adding Population Density
I propose adding in census tract population density as another confounder 
for which to 
control, acting as a measure of rurality. It probably correlates with 
county, but I think should do a 
better job of addressing rurality. I wonder how a model with both, one with 
only population density, and one with only county would compare.

The DAG might look like:

![Figure 3]({static}/images/science/well_water/dag3.png)

Again, to be explicit about some possible causal mechanisms, I'll propose that:

- Pop density => SVI: People may move to/from urban/rural areas, yielding 
  distinct demographics. e.g. young people may want to move to the big city, 
  or old people may want a quiet retirement.
- Pop density => Well water: As mentioned in the CDC reference. I suppose 
  less densely populated areas can more likely support well users. Though my 
  brother gets well water for watering his garden (but is on municipal 
  drinking water) in a Florida suburb.

# Outcome Approximations
Some census tracts are fully or not at all served by municipal water sources.
Some are partially served by them. For these partial cases, we need to 
estimate values for their chosen outcome, count of houses using domestic wells by 
census tract. The authors state:

> For each census tract we estimated the proportion of the population using 
> a domestic well using the following assumptions: 1) census tracks without publicly supplied water
> rely on domestic wells, 2) the proportional area served by a public water supply is the same as the
> proportion of homes served by a PWS. To verify whether our assumptions were valid, we compared our
> maps of proportion of homes served by private well water to population density maps of the state of
> PA (S1 Fig).

However, given the relationship between rurality and well water usage, this 
area-based approximation will likely overestimate well reliance. A reviewer 
of the manuscript notes this:

> I realize this is a pragmatic assumption and you later note that the areas with the public water supply may have a higher population density (whereas as the analysis assumes equal population density). I expect there would be a way to ‘weight’ the population in the areas inside and outside the public water supply so as to overcome this potential source of bias. e.g. I imagine there are reasonable shape files of population density that would enable this.

I'll discuss it in more detail later, but thanks to [^2], I was able to find 
such population density maps thanks to [Facebook and CIESIN](https://dataforgood.facebook.com/dfg/tools/high-resolution-population-density-maps). I'm not sure why 
this information wasn't incorporated, given that Coker is an author on this 
paper. I guess it was considered a good enough approximation as per S1 Fig.

# Conclusion
I've argued that population density should be included in their model as a 
rurality metric, acting to account for this potential confounding. I also am 
interested in seeing what, if any, difference using population density in 
estimating well usage might have.

In the next post, I'll go over my main issue with the analysis: the (non)
use of Bayesian profile regression.


[^1]: Liverani, S, Lavigne, A, Blangiardo, M, 2016. Modelling collinear and spatially
correlated data. Spatial and Spatio-temporal Epidemiology 18, 63–73. https://doi.org/10.1016/j.sste.2016.04.003.
[^2]: Coker ES, Molitor J, Liverani S, Martin J, Maranzano P, Pontarollo N, et al. Bayesian profile regression to study the ecologic associations of correlated environmental exposures with excess mortality risk during the first year of the Covid-19 epidemic in lombardy, Italy. Environ Res 216(Pt 1):114484. Available from: https://europepmc.org/articles/PMC9547389 https:// doi.org/10.1016/j.envres.2022.114484 PMID: 36220446

## Links
[Part 1]({filename}./PA_wells_1.md) [Part 2]({filename}./PA_wells_2.md)
[Part 4]({filename}./PA_wells_4.md) [Part 5]({filename}./PA_wells_5_analysis_1.md)
[Part 6]({filename}./PA_wells_6_analysis_2.md)
