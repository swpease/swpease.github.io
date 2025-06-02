Title: PA Well Water, Part 2
Date: 2025-6-1
Category: Science
Tags: analysis

# Introduction
This post continues from [Part 1]({filename}./PA_wells_1.md) and covers the 
standardization of the 
covariates used for the 
clustering part of their model.

I think it'll wind up pretty short. I had initially created some maps to 
show off, but decided that they didn't add anything substantial to the 
explanation.

# My Gripe
The paper reads:

> All values were rescaled into county-specific z-scores before being fit in 
> the Bayesian Profile Regression model. This normalization of indicator 
> data was done because each county has its own baseline level of values for 
> the social vulnerability indicators. Additionally, these indicators vary 
> not only between census tracts but within and between counties. If raw, unscaled values had been used, it would obscure actual inequalities between clusters that are occurring between counties. This similar rescaling was used by Coker et al. (2023) in assessing the spatial relationship between environmental exposure profiles and excess mortality risk due to COVID-19 in Lombardy, Italy.

I don't understand the logic for county-specific z-scores. What is special 
about these values on the county-relative scale? If a county has overall 
(for the state) low values, why does it make sense to have the largest value 
from that county pushed up to be with the overall (statewide) high values. 
The converse as well: a county with overall high values would have its 
smallest value pushed down to be with the overall low values.

They say the rescaling is similar to Coker et al. (2023), but that paper 
doesn't mention any sort of grouping prior to z-scoring, stating:

> We rescaled the respective values into Z-scores before fitting the Bayesian Profile Regression analysis

# A Specific Case
Data source: [PA Census Tracts SVI 2018](https://www.atsdr.cdc.
gov/place-health/php/svi/svi-data-documentation-download.html).

I arbitrarily picked EP_UNEMP (The SVI's unemployment rate estimate) to 
examine. The table below shows Snyder County, the county most impacted by 
the z-scoring (i.e. standardization) for this 
variable. The county 
has 8 census tracts, hence 8 rows. The table has crap names because I needed to fit the table 
within my blog's margins. To specify the column definitions:

  - EP_UNEMP: unemployment rate estimate. Note if you're following 
    along that I replaced -999's with NA's.
  - std_cnty: EP_UNEMP, standardized by county.
    - dplyr code: `svi_unemp |> group_by(STCNTY) |> mutate(std_by_county = 
      as.vector(scale(EP_UNEMP))) |> ungroup()`
  - std_PA: EP_UNEMP, standardized by across all of PA
    - dplyr code: `svi_unemp |> mutate(std_PA = as.vector(scale(EP_UNEMP)))`
  - cnty_qntl: Empirical quantile of std_cnty
    - dplyr code: `svi_unemp |> mutate(cnty_qntl = min_rank(std_cnty) / n())`
  - PA_qntl: Empirical quantile of std_PA
    - dplyr code: `svi_unemp |> mutate(PA_qntl = min_rank(std_PA) / n())`
  - qntl_abs_diff: Absolute difference between PA_qntl and cnty_qntl

I'm not sure if there's a standard way to compute empirical quantiles, so 
maybe my numbers there are off.

| EP_UNEMP| std_cnty| std_PA| cnty_qntl| PA_qntl| qntl_abs_diff|
|--------:|--------:|------:|---------:|-------:|-------------:|
|      1.6|    -1.11|  -0.97|      0.06|    0.04|          0.02|
|      1.9|    -0.82|  -0.91|      0.17|    0.06|          0.10|
|      2.0|    -0.73|  -0.89|      0.21|    0.07|          0.14|
|      2.1|    -0.63|  -0.87|      0.26|    0.08|          0.18|
|      2.9|     0.13|  -0.70|      0.65|    0.16|          0.49|
|      4.6|     1.75|  -0.36|      0.94|    0.42|          0.52|
|      3.3|     0.51|  -0.62|      0.77|    0.22|          0.55|
|      3.7|     0.90|  -0.54|      0.84|    0.28|          0.56|

To me, the important thing to see is how the census tracts with unemployment 
rates that are high for Snyder County are still below the median for the 
state. This yields quite large differences in where they wind up, 
relative to 
the census tracts across all of PA, when you do county-specific 
standardization vs PA-wide standardization (where standardization = z-scoring).


# Conclusion
That's about it. I could go on, but I think the idea is presented well 
enough. The researcher obviously thought about this and made the 
decision and effort to 
do this z-scoring, so maybe I'm just missing something and am the wrong one. 