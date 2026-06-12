Title: Vibrio
Date: 2026-6-12
Category: Science
Tags: analysis

# Introduction
I found a paper on Vibrio infection prediction:

> Campbell AM, Cabrera-Gumbau JM, Trinanes J, Baker-Austin C, Martinez-Urtaza J. Machine Learning Potential for Identifying and Forecasting Complex Environmental Drivers of Vibrio vulnificus Infections in the United States. Environ Health Perspect. 2025 Jan;133(1):17006. doi: 10.1289/EHP15593. Epub 2025 Jan 23. PMID: 39847704; PMCID: PMC11756857.

[Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC11756857/)

I wanted to try using {mvgam} to analyze the data, maybe an occupancy model; they used a random forest.

# The Hitch
I was somewhat surprised (well maybe not quite that extreme) that the processed dataset was not available online somwhere. I asked the lead author for the processed dataset, and unsurprisingly got no response. So I decided to see how regenerating it on my own would go. I could always tap out if I lost interest / my eyes hurt. Well, I failed at the first hurdle.

The paper lists [https://www.cdc.gov/vibrio/php/surveillance/](https://www.cdc.gov/vibrio/php/surveillance/) as the data source for Vibrio infections. I was able to find some data in the BEAM Dashboard, but nothing at the county-level, only the state-level. I cannot find any data at more specific than the state level. Well, I found that Florida's state health department lists infections by county, but only annually, and that's not the whole US.    

Oh well.

# Consolations
I've convinced myself that ultimately the important thing is communicating to the public that Vibrio is a hazard that they should be cautious of their exposure to. The surveillance of interest is some sort of environmental sampling method to detect/quantify Vibrio in natural waters and shellfish. 