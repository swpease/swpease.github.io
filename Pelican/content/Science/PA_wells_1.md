Title: PA Well Water, Part 1
Date: 2025-5-29
Category: Science
Tags: analysis

# Introduction
I found a paper on PLOS Water:

Wamsley M, Coker ES, Wilson RT, Henry K, Murphy HM (2024) Social 
vulnerability and exposure to private well water. PLOS Water 3(12): e0000303.
[https://doi.org/10.1371/journal.pwat.0000303](https://doi.org/10.1371/journal.pwat.0000303)

I can't do a better job than the authors of summarizing the purpose, so 
here's the first few sentences of the abstract:

> One quarter of the population of Pennsylvania relies on private domestic well water: two-fold greater than the US average. Private well owners are responsible for the maintenance and treatment of their water supply. Targeted interventions are needed to support these well owners to ensure they have access to safe drinking water, free of contaminants. To develop appropriate interventions, an understanding of the characteristics and social vulnerability of communities with high well water use is needed. The purpose of this study was to determine the spatial patterning of social vulnerability in Pennsylvania and assess the association between social vulnerability and private domestic wells using profile regression.

I think the paper is interesting, but I found a few issues with it that I 
wanted to go over. This has largely served as a great learning resource for 
me in a number of respects: mapping, Bayesian stats, epidemiology, stats in 
general, demographics... I'll go over the different issues I had over 
several posts. But first, what is "social vulnerability"?

# Social Vulnerability / Social Vulnerability Index (SVI)
"Social vulnerability" has a few definitions that try to get at the same 
meaning, to varying success. I think that the Vermont public health 
department does the best job of explaining social vulnerability and the SVI: 
[ref](https://www.healthvermont.
gov/sites/default/files/documents/2016/12/ENV_EPHT_SocialVulnerabilityIndex.
pdf). The [ATSDR site](https://www.atsdr.cdc.gov/place-health/php/svi/index.
html) has a definition that made me go, "What?", but its definition within 
its detailed [documentation](https://www.atsdr.cdc.
gov/place-health/php/svi/svi-data-documentation-download.html) is much 
more sensible in my view. Vermont's 
definition is: 

> Social vulnerability refers to the resilience of communities when
responding to or recovering from threats to public health.

The ATSDR documentation's is:

> Every community must prepare for and respond to hazardous events, whether a natural disaster like a tornado or a disease outbreak, or an anthropogenic event such as a harmful chemical spill. The degree to which a community exhibits certain social conditions, including high poverty, low percentage of vehicle access, or crowded households, among others, may affect that community’s ability to prevent human suffering and financial loss in the event of a disaster. These factors describe a community’s social vulnerability.

Similarly, Social Vulnerability Index (SVI) per Vermont is:

> a planning tool to evaluate the relative social vulnerability across the 
> state. It can be used if there is a disease outbreak or in the event of an 
> emergency—either natural or human-caused—to identify populations that may 
> need more help.

And for ATSDR is:

> to help public health officials and emergency response planners identify 
> and map the communities that will most likely need support before, during, 
> and after a hazardous event.

In general, I thought the Vermont reference was the best, both for being 
concise, and importantly for highlighting the SVI's limitations. I'd read 
that if I were you.

## A Brief Aside
Going to the ATSDR website shows a banner:

![Figure 1]({static}/images/science/well_water/ATSDR_site.png)

I don't really go on government sites much, so I was astounded.

# My Issues With This Paper
## Re Its Premise
I'm actually fine with its premise. A few relevant excerpts:

>Since upkeep of private water supplies falls completely on the well-owner, community-level and individual-level social deprivation/vulnerability is likely to be an important determinant of whether well-owners can keep up with the requirements to ensure safe drinking water.

>the socioeconomic and demographic characteristics of the population using domestic wells (that are excluded from public water supplies) are not well described.

However, I do wonder if in a real situation you might not just ask the 
regional/local government for information on the local well users, giving 
better information than this study could? The aforementioned Vermont user's 
guide seems to agree, referring to the SVI as a "first step" in screening 
populations and adding:

> Local information might be more accurate than these
estimates and should always be considered if it is available.

If you want to know more, just read the paper's intro.

## Re Its Conclusions
Their analysis indicated that well users were across the gamut of SVI, 
yielding a fairly broad conclusion. Some groups had high SVI (well, I'll argue 
that point later), some low. They say that the high SVI groups comprised a 
large population (1.1 million, ~1/3 of PA well users), but do not provide a 
list of populations for each group, which would have been nice.

A few instances of trying to work around this nebulousness:

> it seems reasonable to focus education interventions on all high private well use areas

Well I could've told you that.

> The knowledge gained from our analysis in PA informs us that interventions and education campaigns need to be targeted towards homeowners (and some renters), and populations that are more socially vulnerable (have a low level of education, with an annual income less than $30k, are elderly or have children) as well as those that are less socially vulnerable (those with higher levels of education, an annual income over $30k, and are not a sensitive age).

Again, that's a pretty wide net.

## Re Its Methods
This is where problems arose, I think. I want to be clear that I am not 
trying to be mean, that I might be wrong in some respects in my criticisms, 
and that I've been there as a grad student.

My first doubts arose when looking at the regression formula in the section 
"Multilevel risk model". It is a mess. The indexing is wrong and there is a 
dummy variable trap. I think there might be other issues, but it could just 
be unfamiliar notation.

I have three primary issues:

  1. They z-scored by county.
  2. They didn't include a good "rurality" covariate. 
  3. They didn't actually do Bayesian Profile Regression.

I'll go over each of these in separate posts. I think it's good to have a 
grasp on the "units" in this study: census tracts.

# Census Tracts
This paper references a data source as the US Census Bureau's TIGER/Line 
Shapefiles [here](https://www.census.
gov/geographies/mapping-files/time-series/geo/tiger-line-file.html). If you 
download a Shapefile, the dataset's abstract reads in part (emphasis mine):

> Census tracts are small, relatively permanent statistical subdivisions of 
> a county or equivalent entity, and were defined by local participants as 
> part of the Census 2000 Participant Statistical Areas Program (PSAP). The 
> Census Bureau delineated the census tracts in situations where no local 
> participant existed or where all the potential participants declined to participate. The primary purpose of census tracts is to provide a stable set of geographic units for the presentation of census data and comparison back to previous decennial censuses. Census tracts generally have a population size between 1,500 and 8,000 people, with an optimum size of 4,000 people. **When first delineated, census tracts were designed to be homogeneous with respect to population characteristics, economic status, and living conditions**. The spatial size of census tracts varies widely depending on the density of settlement. Physical changes in street patterns caused by highway construction, new development, etc. may require boundary revisions before a census. In addition, census tracts occasionally are split due to population growth, or combined as a result of substantial population decline. Census tract boundaries generally follow visible and identifiable features. They may follow legal boundaries such as minor civil division (MCD) or incorporated place boundaries in some States and situations to allow for census tract-to-governmental unit relationships where the governmental boundaries tend to remain unchanged between censuses. State and county boundaries are always census tract boundaries in the standard census geographic hierarchy. In a few rare instances, a census tract may consist of noncontiguous areas. These noncontiguous areas may occur where the census tracts are coextensive with all or parts of legal entities that are themselves noncontiguous. 

Also, looking at the [technical documentation](https://www.census.
gov/programs-surveys/geography/technical-documentation/complete-technical
-documentation/tiger-geo-line.html) I feel is helpful. For instance, the 
[2010 documentation](https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2010/TGRSHP10SF1.pdf) 
provides a visual hierarchy of census entities in its Figure 1.

# Simple Issues
## Classification
### Cluster 14
Cluster 14 was classified by the author as having "suggested social 
vulnerability". However, per Fig 5, for the 10 social vulnerability 
covariates, the median quartiles for Cluster 14 were comprised of 5 in 
quartile 2 and 5 in quartile 3, which should indicate a remarkably 
middle-of-the-road social vulnerability level. You might be thinking, "well, 
you have to see the full distributions to know for sure." Well, that's what 
I thought, too. The odd thing is, full distributions are a built-in 
visualization function provided by the R package that I'm guessing they used 
for their analysis.

## Nitpicks
Beyond the aforementioned formula confusion, I found some other errors.

### Table 1
1. Columns are mis-aligned.
2. Cluster 1's Poisson model estimate should be 0.28, not 1.28.
3. Cluster 12's mean # households should be 1140 or 1149 I'm guessing. They 
   probably fat-fingered 90.

### Fig 6
1. The y-axis is cut-off.
2. "The random effects due to county are shown in Fig 6." No, they aren't.

# Future Writing
I'll write separate posts at least on each of my 3 beefs(?) with this paper, 
and want to write some more about Bayesian Profile Regression afterwards.