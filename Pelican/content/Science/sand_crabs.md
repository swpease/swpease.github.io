Title: Sand Crabs Eating Bits of Plastic String
Date: 2024-10-15
Category: Science
Tags: analysis

# Introduction
I read a paper, ["Effects of environmentally relevant concentrations of 
microplastic fibers on Pacific mole crab (Emerita analoga) mortality and
reproduction." Horn DA; Granek EF; Steele CL. 2019.](https://aslopubs.
onlinelibrary.wiley.com/doi/10.1002/lol2.10137) as part of reading up on 
stuff for a job I applied to. I had been learning how to use Bayesian 
methods, so this seemed like a good way to try our using real data from the 
wild. I'll link throughout to files in a repository that shows my work.

The gist of the experiment was they set up 64 jars of sand + sea water, with a 
crab in 
each.
32 
were subject to the addition of three plastic fibers (1mm long) every four 
days, for up to 71 days. Dead crabs were frozen for later analysis.

I have been a bit confused by their analysis methods. They use a linear 
mixed effects model, which is all well and good, but there seems to be a few 
things that don't make sense.


# Data Discrepancies
The paper provides the data at two sites: [Zenodo](https://zenodo.
org/records/3564736) and [GitHub](https://github.
com/cwgrldotty/Sand-Crab-PSU-Data). The problem is they don't line up: 

  - The GitHub data is missing rows.
  - The Zenodo data is missing columns.
  - Some of the data is different:
    - environmental plastics present
    - egg stage at end of experiment

I think that the "egg stage at end of experiment" data is correct for GitHub,
and wrong for Zenodo, because there is a "# of egg stages" column as well 
that on the Zenodo dataset sometimes exceeds "egg stage at end of 
experiment", which would mean starting at negative egg stages.

I don't think they used junk data for their analyses; I just think the 
uploads are wonky. Well, there is one possible data error: I think crab 15's 
days alive number should be 21, not 71, based on the 
recorded date of death. As someone with terrible handwriting, I could 
totally see mixing up a 2 and a 7. 

I made the presumed correction to crab 15 for my analyses. I used the Zenodo 
data for 
survival times because it wasn't missing crabs.

# Survival Curve
[R Markdown Notebook](https://github.
com/swpease/sand-crabs/blob/master/sand_crab_mortality.Rmd)

The lack of a survival curve surprised me. Instead, they have a boxplot that 
I can't figure out. It doesn't match the data. My guess is that it's the 
fitted survival times post-linear mixed effects model, i.e. it's the 
shrunken (via partial pooling) survival times. As it is, here is the 
survival curves, with 50% CI's:

![Figure 1]({static}/images/science/sand_crabs/survival_curves.png)

I used a log-rank test to compare the treatment vs control groups' survival 
curves. The p-value of the (presumed) corrected data was 0.10, which is higher 
than the publication's value of 
0.03 for their assessment of difference in mortality. Though,
the (presumed) wrong data yielded a p-value for 
the log-rank test of 0.05, which is obviously much closer. 

10 vs 17 
deaths does seem quite a bit different. I always find myself mentally replacing 
something below some subconsciously-determined p-value threshold as 
"definitely", but 0.1 just means, well there's evidence. Unless I want it 
*not* to be true, in which case I think, "yeah it's totally a case of that 
10%". I do 
think it's slightly interesting 
that 
the curves are the same for the first three weeks. I wonder if there's 
anything to that. Maybe it lends credence to the authors' idea that the 
mechanism of harm is the dyes in the plastics. I could imagine that 
the body burden of dye is 
steadily increasing over time.


# "Number of PP Fibers Internalized"

I don't like this name for this variable. At the end of the experiment 
(crabs that died before the end were frozen), they 
dissolved the crabs and counted the number of plastic fibers they filtered 
out of that. That gives you the body burden at death/censoring, not 
necessarily the total number of fibers they internalized. What if they 
could expel the fibers somehow? Also, what if some of the fibers were stuck 
to their outside? I'm guessing they washed them or something to account for 
this, since they were meticulous in preventing contamination at all the 
other phases, but didn't mention anything. Or maybe it's a non-issue.

This variable is used for regressions to explain mortality, the number of 
days that a crab held live/viable eggs, and other outcomes. I don't think 
it's an accurate representation of what it claims to be. Here is a graph of 
number of fibers collected out of each crab at the end of the experiment vs 
when they died:

![Figure 2]({static}/images/science/sand_crabs/body_burden.png)

The horizontal axis has ticks every 20 because I couldn't figure out how to get 
ggplot to make it how I wanted in the amount of time it took for me to get 
mad at The Grammar of Graphics&trade;.

Anyway, it seems highly unlikely in looking at this graph that every fiber a 
crab intakes stays in it until death. The number never exceeds five, in 
spite of reaching five in one crab after one third of the experiment's 
duration, and three in one crab after nine days.

I tried a statistical test to get at this being the case, by looking for an 
association between exposure duration (i.e. days alive in the experiment) and 
number of fibers internalized. I 
used a Poisson regression on $log(days)$, because I read that doing so lets 
you combine data with different exposure durations, with the $log(days)$'s 
coefficient indicating the change in rate over time. As it is, I feel like 
it would be difficult to find a statistical test that *did* show some sort 
of relationship between counts and duration of exposure. So my model (in R 
code) was essentially (names changed for clarity): 

`glm(fibers ~ log(days 
alive), family = poisson(), data = 
treatment crabs)`

Which yielded:

| param | Estimate | Std. Error | z value | Pr(>\|z\|) |
| - | - | - | - | - |
|(Intercept) | 0.87576 | 0.69172 | 1.266 |  0.205 |
|log(num_of_days_alive) | -0.07686 | 0.18669 | -0.412 | 0.681 |

Which I interpret as "no, there isn't much of an association between counts and the different durations over which the counts accumulated", because of the small Estimate, relatively large Std. Error, and small Pr() for log(num_of_days_alive)."

I kinda wish they'd checked the number of fibers suspended in the water of 
the jars somehow.

I also wonder if sand crabs can vomit. This paper on decapod crustacean 
welfare in experiments [[^1]] references a study on red rock crab digestive 
processes [[^2]] that observed regurgitation/vomiting. So maybe?

Back to the statistics, the authors report a relationship between fibers 
internalized and a 
decrease 
in days alive. I'm skeptical that there's anything to it. If they 
incorporated some sort of accounting for censored observations (maybe `lme4` 
handles things somehow?) they don't mention it in the publication.


# Wait, what happened to Bayes?
Oh.

## Exponentially Distributed Survival
[Jupyter Notebook](https://github.com/swpease/sand-crabs/blob/master/sand_crabs.ipynb)

Well, I tried fitting an Exponential distribution to the mortality data, per 
the suggestion found in this lecture from [Statistical Rethinking](https://youtu.be/Zi6N3GLUJmw?si=AowaUikcftuAtCCk&t=4882). I 
think it looks okay?

![Figure 3]({static}/images/science/sand_crabs/exponential_72d.png)

and to see where these curves go:

![Figure 4]({static}/images/science/sand_crabs/exponential_730d.png)

My biggest concern is: what would the data have wound up looking like if the 
experiment went on for longer?

The graphs get a bit muddled where the treatment and control fits overlap, 
but there's nothing fascinating going on at the overlaps, so I just left it 
as is rather than double the number of graphs.

### Picking a prior
The exponential model only has one parameter, $\lambda$. The mean of an 
exponential distribution is $1 / 
\lambda$, so what's the expected mean?

As far as expected survival times, [according to Wikipedia](https://en.
wikipedia.org/wiki/Emerita_analoga), most sand crabs 
die in the autumn of their second year. These crabs were collected on August 4,
so I guess I'll assume ~400 days survival time for crabs in their first year,
maybe just ~50 for crabs in their second year,
and I guess half in their first v second year,
so ~200+ days average survival time. Can you age crabs? I don't suppose 
they've got otoliths.

With that in mind, and per the suggestion of the [al ighty cElreath](https://youtu.be/Zi6N3GLUJmw?si=apBRHdMb0lCodpNI&t=5366) to set the priors on the log 
of the inverse of $\lambda$, so that they are easier to define, I went with 
a prior on said log inverse of $log(1/\lambda) \sim N(5, 1)$, because $e^5 = 
148$ (and $e^4 = 55$ and $e^6 = 400$). [R Markdown Notebook](https://github.com/swpease/sand-crabs/blob/master/simulated_exp_data.Rmd)

### Expected Survival Times
So speaking of expected survival time, what does the Bayesian approach say 
it might be?

![Figure 5]({static}/images/science/sand_crabs/forest_ridgeplot_90hdi.png)

The posterior means of the mean survival time are 195 days for the control 
and 98 days for the treatment, but 
obviously 
it's pretty uncertain about the control, which makes sense given how few of 
the crabs died. You can see the uncertainty in the previous plot as well: those 
orange curves are pretty spread out. It's at least mildly encouraging that 
the control's posterior mean of the mean survival is fairly 
close to what I presumed 
based on the Wikipedia article. And the treatment mean survival time seems 
reasonable as well.

And as for the contrast of $control - treatment$ expected survival times,
most of the 
probability 
mass is above zero, with a mean of 98 days (no, I didn't mistake it for the 
treatment's mean):

![Figure 6]({static}/images/science/sand_crabs/forest_90hdi_contrast.png)

So the treatment crabs probably don't live as long as the control crabs on 
average, but it's pretty uncertain what exactly the difference is.


### Rejected Prior
I also toyed with the idea of describing the survival as a mix of two 
populations, first year and second year crabs, by using a mix of two 
Exponential distributions. I decided it was 
just more 
complicated without providing any apparent benefits. The curves it was 
producing looked pretty similar to an Exponential distribution. [R Markdown 
Notebook](https://github.com/swpease/sand-crabs/blob/master/simulated_exp_data_spectrum.Rmd)

### Sensitivity to the Prior
There's not a ton of data, so how much does the prior matter? Not too much. 
It pushes the averages around, but the relationships are pretty consistent. 

log(mu)-prior|mu-prior|sigma-prior|mu-post-ctrl|mu-post-trt|mu-post-contrast|P(contrast > 0)
:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:
4|55|1|180|92|87|0.95
5|148|1|194|98|96|0.96
6|400|1|215|104|111|0.96
4|55|0.5|140|85|55|0.94
5|148|0.5|182|104|79|0.95
6|400|0.5|251|131|119|0.95


## Gamma Distributed Survival
[Jupyter Notebook](https://github.com/swpease/sand-crabs/blob/master/sand_crabs_gamma.ipynb)

The gamma distribution gives a sigmoidal survival curve. Maybe that'll look 
a bit better? I think it does, particularly at the start, though it also 
seems to have more posterior 
draws that aren't particularly believable. For instance,
look at the control fits' cutoffs on the right at over 700 days.

![Figure 7]({static}/images/science/sand_crabs/gamma_72d.png)
![Figure 8]({static}/images/science/sand_crabs/gamma_730d.png)

### Expected Survival Times
Overall, it's a similar story with the expected survival times here. The 
posterior 
means of the mean survival time are 195 days for the control 
and 84 days for the treatment, but 
once again 
it's pretty uncertain about the control. Actually, it's even more uncertain: 
the standard deviation in this case is 133, while it was merely 64 with the 
exponential model. This uncertainty propogates to the contrasts, though the 
probability density is still mostly above 0 (97% > 0), with a mean of 112.
![Figure 9]({static}/images/science/sand_crabs/forest_ridgeplot_gamma_90hdi.png)
![Figure 10]({static}/images/science/sand_crabs/contrast_gamma_90hdi.png)

### Picking a Prior
This uses the same logic as above, but now needs two priors, $\alpha$ 
(shape) and 
$\beta$ (rate), where for a gamma distribution $\mu = \alpha / \beta$ and 
$var = \alpha / \beta^2$. I settled on $\alpha \sim Gamma(\alpha = 2, \beta = 
1)$ and $\beta \sim HalfNormal(\sigma = 0.02)$, which gave mostly unabsurd 
survival curves in prior predictive simulation. 

### Rejected Prior
I also tried $\beta \sim LogNormal(\mu = -4, \sigma = 1)$, but this did not 
seem to produce as good of fits to the data.

### Sensitivity to the Prior
Changing the prior to $\beta \sim HalfNormal(\sigma = 0.2)$ yielded similar 
results. That's all I looked at because I'm sick of looking at survival curves.

# Discussion / Conclusions
**Eating plastic is probably bad.** What a revelation. Really though, I am 
surprised at the posterior difference in expected survival time, because the 
experiment was designed to have environmentally relevant exposure levels. 
Do sand crabs have much shorter lifespans nowadays? Were the control crabs 
happy to have clean water (but not clean sediment!) for once? I wonder if it 
might be more accurate to think of the control as the effective "treatment", 
since the experimental treatment *ought* to approximate the sand crabs' actual 
living conditions more closely.

And can sand crabs 
vomit? The 
unanswered 
question. I suppose if they all had at least one fiber in them, they at the 
very least don't always vomit up accidentally ingested non-food. I wish 
they'd collected the poop.

**Stay tuned for part 2: egg stuff!**

[^1]: "Anaesthesia of decapod crustaceans." de Souza Valente C. 2022.
https://doi.org/10.1016/j.vas.2022.100252
[^2]: "Gastric processing and evacuation during emersion in the red rock 
crab, Cancer productus." Mcgaw IJ. 2007. https://doi.org/10.1080/10236240701393461