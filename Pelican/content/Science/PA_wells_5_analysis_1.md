Title: PA Well Water, Part 5: Estimating the Outcome Variable
Date: 2025-6-16
Modified: 2025-06-18
Category: Science
Tags: analysis

# Introduction
This post expands on [Part 3]({filename}./PA_wells_3.md) -- specifically the 
section concerning Outcome Approximations -- and begins preparing data for 
analysis.

In this post, I will compare the estimation method used in the paper vs an 
alternative, and then look at a few other published methods. The estimation is 
for **the 
outcome variable, which 
is: the number 
of people who rely on domestic well water, i.e. who do not have coverage by 
a public water system (PWS) at their residence**. In the paper, they use 
number of 
households for some reason. I don't see what the practical difference to 
individuals vs households might be, so I'll just leave it as individuals.

## The Two Estimation Methods
Comparing their method (1) vs an alternate (2):

1. Area-based estimation: The proportion of the census tract's area that is not 
   covered by a PWS 
   equals the proportion of the census tract's population that relies on domestic 
   well water. The census tract's population is provided by the SVI data 
   (which is taken from the ACS).
2. Population density-based estimation: Use high-resolution population density 
   estimates to 
   directly count the 
   estimated number of people who rely on domestic well water, again based 
   on PWS coverage. This value 
   can be used in two ways:
    1. Directly.
    2. Use the same population density estimate data to determine the 
       estimated population for the whole census tract, take the proportion of 
       that total that is on domestic well water, and apply said proportion to 
       the ACS population estimate. This might be better, as it would -- 
       assuming the population ratio of PWS/well-water remains consistent -- 
       let us apply this proportion to what should be a better 
       population estimate: the ACS estimate. ACS data is more recent (2022 
       vs 2019).

# Methods (in the Paper-y Sense)
Getting these estimates of population relying on well water required working 
with several map datasets (Shapefiles, GeoTIFF...). I initially conducted 
much of the data processing in QGIS. I want to translate it to scripting (in 
Python) for reproducibility/defensibility/recall, but only have a part of it 
in Python so far.

## Data Sources
Firstly, the four data sources I collected:

### SVI Data
- src: https://www.atsdr.cdc.gov/place-health/php/svi/svi-data-documentation-download.html
- params:
    - Year = 2022
    - Geography = Pennsylvania
    - Geography Type = Census Tracts

### PA Public Water Systems (PA PWS)
- src: https://newdata-padep-1.opendata.arcgis.com/datasets/PADEP-1::public-water-systems-public-water-supplier-service-areas/about

### TIGER/Line Shapefile (T/L)
- src: https://www.census.gov/cgi-bin/geo/shapefiles/index.php
- params:
    - Year = 2022
    - Layer Type = Census Tracts
    - State = Pennsylvania

### Population Density Data
- src: https://data.humdata.org/dataset/united-states-high-resolution-population-density-maps-demographic-estimates#
- refs: 
    - https://dataforgood.facebook.com/dfg/tools/high-resolution-population-density-maps
    - https://ciesin.climate.columbia.edu/programs#!#cu_card_group_media-400
- files:
    - population_usa38_-80.tif.zipGeoTIFF
    - population_usa38_-90.tif.zipGeoTIFF
- citation:
    - Facebook Connectivity Lab and Center for International Earth Science 
     Information 
    Network - CIESIN - Columbia University. 2016. High Resolution Settlement 
    Layer (HRSL). Source imagery for HRSL © 2016 DigitalGlobe. Accessed 01 
    06 2025. 
    - Please note that as of 2024, Meta’s high resolution population 
    density maps are no longer being updated.

## Processing Outline
I did some of the processing in QGIS, and some in Python. I'll link to the 
Python file, and outline the QGIS steps:

  - Join SVI and T/L by census tract ID
  - Fix geometries on PA PWS
  - Reproject PA PWS to match T/L-SVI join
  - Difference T/L-SVI using PA PWS overlay
      - Yields well water region (WWR) layer
  - Create virtual raster from Pop Dens GeoTIFFs
  - Reproject T/L-SVI and WWR to match Pop Dens
  - Zonal stats (sum) using Pop Dens virtual raster and
      - T/L-SVI  => pop est of the census tract
      - WWR  => pop est of the well water reliant parts of the census tract

From there, I used Python (see the [repository](https://github. com/swpease/well_water/tree/master/python)).

# Results
Note that I am comparing method 1 to method 2.2 (above).

## Total Well Water Population
Firstly, what do these methods say the total PA well water population is?

  - Area based: 3.92 million
  - Pop density based: 2.42 million
    - Note: the two alternative methods I outlined above were within 50k of 
      each other (~2%), as method 2.1 (direct usage of pop #) was 2.38M.

These are way different! Are either of these more likely to be accurate? Is 
there a third party? (Yes). It didn't occur to me to see if someone had 
already estimated these values until just now, so I'll have to see what they 
say after I finish this next part.

Continuing on this specific comparison...

## Comparative Plots
We've already established that these estimates are way different. Is there 
any patten to the difference?

First, let's see the numbers at the census tract level as proportions of the 
total population:

![Figure 1]({static}/images/science/well_water/ww_pop_comp_prop.png)

And second, as total population estimates:

![Figure 2]({static}/images/science/well_water/ww_pop_comp_popul.png)

We already knew the area-based values were going to generally exceed the 
population-density-based values. I was just kind of hoping there might be a 
pattern to it.

# Discussion
## Total Well Water Population (Now with 3rd Parties)
The PA Dept of 
Conservation and Natural Resources states that [over 1 million](https://www.pa.gov/agencies/dcnr/conservation/water/groundwater.html) homeowners depend on 
private wells for drinking water. I suppose then the question is: how big is 
a home? The US Census Bureau's estimate for PA in 2019-2023 is [2.40 persons 
per household](https://www.census.gov/quickfacts/fact/table/PA/INC110223). 
So a rough estimate is **2.4 million** well users, though there are factors 
like 
rural areas having larger average household sizes.  

Penn State estimates [3.5 million](https://extension.psu.edu/private-water-systems-faqs), though I don't see 
their source. Penn State also estimates [1-3.5 million](https://extension.psu.edu/social-science-of-drinking-water), this time with some good sources 
that I'll look into and discuss later, though I'm wondering if they 
subconsciously misread "homes" as "people" for the 1M case.

It turns out that "later" is now.

### Johnson Papers
There were a couple of related papers [^1] [^2] that estimated the well water 
reliant population across the entire contiguous US, at a 1km^2 resolution, 
for 1990, 2000, and 2010. Apparently 1990 is the last time the US Census 
asked people about their water sources, so they extrapolated from there. 
I've read through the first only, but it presents some interesting 
information:
  > it appears that the number of people supplied by domestic-wells has plateaued and may in fact be dropping.

and
  > The proportion of the population dependent upon domestic wells (domestic ratio) is slowly decreasing nationally.

Their own estimates for Pennsylvania's well water reliant populations are:

  - 1990: 2.43 million [^2] (see Table 3)
  - 2000: 2.29 million (calculated via Zonal statistics (sum) of the PA 
    TIGER/Line 
    shapefile, dissolved to all of PA, on their REM 
    map [^3])
  - 2010: **2.20 million** (same calculation)

### Murray
Murray [^4] provides yet another national estimate of well water reliance, 
but looking at housing units. I haven't even skimmed this one yet, but it 
estimates that in 2010, **1.25 million housing units** had private wells in PA 
(Figure 9). This doesn't disagree with the estimate by the PA Dept of 
Conservation and Natural Resources.

In trying to compare the population-density-based estimates to this, which was 
easy 
enough because ACS (in the SVI) has housing unit estimates as well, I wound 
up with an estimated 1.75 million housing units. That number seems high, 
especially considering my population estimate of 2.4 million, but it's what 
the ACS says, so... 

## So Which Estimate to Use?
Given the results by Murray and Johnson, my inclination is that the 
population-density-based estimates of well water 
users might be an overestimate, while the area-based estimate is 
likely a huge overestimate.

While the population-density-based estimates can be converted to either 
population or housing units, I am leaning towards population because:

  - (I know 
this is dumb) it's what I first thought of.
  - I am interested in people, not housing.
  - I'm concerned converting to housing units might lead to some extra 
    uncertainty, whereas the CEISIN-direct population estimates (method 2.2) 
    closely 
    align with the ACS-based ones (method 2.1) (see supplemental graphs [^5]).
  - It seems to more closely align with a third party (Johnson).

How is the alignment exactly? Let's do another scatter plot:

![Figure 3]({static}/images/science/well_water/ww_pop_comp_Johnson.png)

A spot check of some of the largest discrepancies seems to indicate that the 
population-density-based estimates are better: 

  - cases with large Johnson 
estimates and small population-density-based estimates seem to be tracts 
that are covered by a PWS. 
  - cases with small Johnson 
estimates and large population-density-based estimates have little to no PWS 
    coverage, so I think it's just a question of population estimates, which 
    I'll go with the recent ACS data for.

Factoring all of this together, I want to **first just use the 
population-density-based estimates**. I will want to also try the Johnson 
numbers, to see how that compares.

# Conclusion
I have some estimates for the outcome variable now. That's good! I think I'm 
ready to fire up Premium and see what this baby can do.

[^1]: Johnson, Tyler & Belitz, Kenneth & Lombard, Melissa. (2019). 
Estimating domestic well locations and populations served in the contiguous 
U.S. for years 2000 and 2010. Science of The Total Environment. 687. 10.
1016/j.scitotenv.2019.06.036. [open source](https://www.researchgate.net/publication/333728321_Estimating_domestic_well_locations_and_populations_served_in_the_contiguous_US_for_years_2000_and_2010)

[^2]: Tyler D. Johnson, Kenneth Belitz, Domestic well locations and 
populations served in the contiguous U.S.: 1990, Science of The Total 
Environment, Volumes 607–608, 2017, Pages 658-668, ISSN 0048-9697. https://doi.org/10.1016/j.scitotenv.2017.07.018. [open source](https://www.researchgate.net/publication/318446309_Domestic_well_locations_and_populations_served_in_the_contiguous_US_1990)

[^3]: Johnson, T.D., and Belitz, K., 2019, Domestic well locations and populations served in the contiguous U.S.: datasets for decadal years 2000 and 2010: U.S. Geological Survey data release, https://doi.org/10.5066/P9FSLU3B. 

[^4]: Murray, A., A. Hall, J. Weaver, and F. Kremer. 2021. "Methods for Estimating Locations of Housing Units Served by Private Domestic Wells in the United States Applied to 2010." Journal of the American Water Resources Association 57 (5): 828–843. https://doi.org/10.1111/1752-1688.12937.

[^5]: 
![Figure 4]({static}/images/science/well_water/ww_pop_comp_CEISIN_methods.png)
![Figure 5]({static}/images/science/well_water/ww_CEISIN_HU_vs_pop.png)

## Links
[Part 1]({filename}./PA_wells_1.md) [Part 2]({filename}./PA_wells_2.md)
[Part 3]({filename}./PA_wells_3.md) [Part 4]({filename}./PA_wells_4.md)
[Part 6]({filename}./PA_wells_6_analysis_2.md)
