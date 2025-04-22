Title: Sand Crabs Eating Bits of Plastic String (Part 2)
Date: 2024-12-17
Category: Science
Tags: analysis

# Introduction
In the [previous post]({filename}/Science/sand_crabs.md) on sand crabs, I 
looked at the mortality of the treatments (exposed to environmentally 
relevant concentrations of microplastic 
fibers)
vs controls. Now, I want to look at another outcome that they looked at: egg 
development.

Specifically, looking at starting vs ending egg development stages. This 
endpoint is.. much trickier to think about. For starters,
it would 
help 
if I knew much about sand crab reproduction, or developmental biology in 
general; it was always a bit of a snooze for me. I mean, I thought the 
reproductive physiology course I took was interesting, but that's different. 

The authors explain:

> The selected experimental time frame (71 d) allowed for two full embryonic 
> development cycles as E. analoga has an incubation cycle of 29–32 days.

I don't really get how this works. Why is one full cycle insufficient? Are 
they expecting slower development in the treatment crabs? Is this just my 
lack of 
understanding of developmental biology?

Adding onto that, there is another observed variable, "# of days with viable 
eggs", which I don't really understand with respect to the start/end egg 
development stages. Do the eggs become inviable after completed development? 
Are there commonly miscarriages (or the egg equivalent)? I guess I should 
just treat this as an exercise in Bayesian stats. It's not like I'll have 
any idea on how to make a useful prior, anyway. 

# Data Discrepancies (Again)
I am using the GitHub data, because the Zenodo data for egg development 
doesn't make sense. The GitHub data also has several issues, but at least 
mostly makes sense. For the GitHub data, there are 3 control crabs missing 
and 4 treatment crabs 
missing, 
which yields 29 control crabs and 28 treatment crabs.

I made a couple of bar charts as descriptive statistics-type things, which 
let me notice that Treatment Crab #5 has wrong data for its egg development 
columns. I was going to just omit it, but I see that there are two other crabs 
for 
which the "# of egg stages(start to finish)" column — which should presumably 
validate the difference between start and end egg stages — is off by one, so 
I think that Treatment Crab #5's end stage was "Z", not 2, plus its "# of egg 
stages(start to finish)" is off by two. This supports by "bad handwriting" 
hypothesis from the previous post. I know I started putting lines through my 
Z's after doing math where some formula creator (I'm guessing with good 
handwriting) 
decided to use Z's and 2's all over the place. Stupid mxn. Stupid ijk. At 
least I'm [not alone](https://betterexplained.
com/articles/linear-algebra-guide/).

Also, there is a column "Reach Larval Stage(9+) Y/N", which has six 
discrepancies with "Egg Stage end of exp". 

Also, there are seven cases of "# of days with viable eggs" exceeding "# of 
days alive".

I guess these data discrepancies further support my thinking of, "Don't take 
the results of my analysis too seriously.".

# Descriptive Plots
Here's what the distribution of egg development stages looked like at the 
start and end of the experiment:

![Figure 1]({static}/images/science/sand_crabs/eggs/starting_stage_hist.png)

![Figure 2]({static}/images/science/sand_crabs/eggs/ending_stage_hist.png)

And how many stages were progressed, based on starting stage, and split out 
by whether the crab died before the end of experiment or not.

![Figure 3]({static}/images/science/sand_crabs/eggs/stages_progressed.png)

I was on the fence about splitting out the above figure by died/lived. I 
decided to, because with them combined, my first question was, "Did those 
starting stage 10 treatment crabs with no development progression die early?
". I suppose I could've coded died/lived by shape, too.

# The Modeling
Firstly, an explanatory note re what follows. I did the modeling months 
ago, but had wanted to extend the model to incorporate censoring. Censored 
discrete distributions were(/are) not implemented in PyMC, as I discovered. 
One of the maintainers (Ricardo) fixed that problem within a couple of days 
of my bringing it up. However, said fix has been [sitting in pull request 
purgatory](https://github.com/pymc-devs/pymc/pull/7662) for months now. Oh well. The point is, I'm revisiting this 
analysis months after having done it, so I am probably forgetting some 
nuances of decisions/explanations.

So just looking at the above plots, I was expecting the model output to show 
minimal differences between treatments and controls, for whichever model I 
decided to use.

I opted to use a proportional odds (ordered logit) model. I don't think it's 
entirely 
appropriate, and looking for an alternative model for ordinal data led me to 
discover the [generalized ordered logit model](https://www3.nd.
edu/~rwilliam/gologit2/UnderStandingGologit2016.pdf), but it seemed like the best 
option of any model options I could find. As it is, I don't really think 
that the appropriateness of a proportional odds model is 
assessable by humans without using the Brant Test. Or maybe I just haven't 
become one with the log-odds yet.

The DAG of this model made me go "Woof!". On paper, its description is 
pretty simple: an ordered categorical outcome with an ordered categorical 
predictor and a categorical predictor. That is: final egg stage outcome with 
starting egg stage and treatment group predictors. Well, everything 
right/down of beta_trt is derived stuff (Stan's "generated quantities" block),
so 
I guess you can ignore that part.

![Figure 4]({static}/images/science/sand_crabs/eggs/DAG.png)

And here is the PyMC model that produced that thing:

```python
N_cutpoints = len(data["Egg Stage end of exp"].cat.categories) - 1
N_deltas = len(data["Egg Stage at Beginning of exp"].cat.categories) - 1
coords = {
    "grp": ["c", "t"],
    "end_stage": data["Egg Stage end of exp"].cat.categories,
    "start_stage": data["Egg Stage at Beginning of exp"].cat.categories,
    "cutpoint": np.arange(N_cutpoints)
}

with pm.Model(coords=coords) as model4:
    # Data
    y_data = pm.Data("y_data", data["Egg Stage end of exp"].cat.codes, dims="obs_id")
    start_stage_data = pm.Data("start_stage_data", data["Egg Stage at Beginning of exp"].cat.codes, dims="obs_id")
    grp_data = pm.Data("grp_data", data["c_or_t_grp"], dims="obs_id")

    # Priors
    cutpoints = pm.Normal("cutpoints", 
                        mu=(np.arange(N_cutpoints) / 2) - 2.5, 
                        sigma=2, 
                    #   initval=(np.arange(N_cutpoints) / 2) - 2.5,
                        transform=pm.distributions.transforms.ordered,
                        shape=N_cutpoints)
    beta_trt = pm.Normal("beta_trt", mu=0, sigma=2)
    beta_start = pm.Normal("beta_start", mu=0, sigma=2)
    delta = pm.Dirichlet("delta", a=np.repeat(2.0, N_deltas), shape=N_deltas)
    delta_j = pm.Deterministic("delta_j", pm.math.concatenate([pm.math.zeros(1), delta]))
    delta_j_cumulative = pm.Deterministic("delta_j_cumulative", pm.math.cumsum(delta_j))

    # params
    phi = pm.Deterministic("phi", 
                           (beta_start * delta_j_cumulative[start_stage_data] 
                            + beta_trt * grp_data),
                            dims="obs_id")

    # lik
    y_obs = pm.OrderedLogistic("y_obs", 
                               eta=phi, 
                               cutpoints=cutpoints, 
                               observed=y_data,
                               shape=grp_data.shape[0])
    
    # derived params
    cutpoints_col = pm.Deterministic("cutpoints_col", cutpoints.reshape((10,1)))
    bc_delta_j_cumulative = pm.Deterministic("bc_delta_j_cumulative",
                                        pm.math.broadcast_to(delta_j_cumulative, (N_cutpoints, N_deltas + 1)))
    cutpoints_by_grp = pm.Deterministic("cutpoints_by_grp",
                                        pm.math.stack([
                                            cutpoints_col - (bc_delta_j_cumulative * beta_start),  # phi = 0
                                            cutpoints_col - ((bc_delta_j_cumulative * beta_start) + beta_trt),  # phi = beta_trt
                                        ],
                                        axis=2),
                                        dims=("cutpoint", "start_stage", "grp"))

    # derived vars
    cum_probs = pm.Deterministic("cum_probs", pm.invlogit(cutpoints_by_grp), dims=("cutpoint", "start_stage", "grp"))
    probs = pm.Deterministic("probs", 
                             (pm.math.concatenate([cum_probs, pm.math.ones((1, 10, 2))]) -
                             pm.math.concatenate([pm.math.zeros((1, 10, 2)), cum_probs])),
                             dims=("end_stage", "start_stage", "grp"))
```

I had quite a time making myself confident that the indexing tetris required 
for `probs` wound up correct.

## Output
Assessing the output of this model was a bit of a chore. I looked at it from 
a couple of different perspectives:

  1. Posterior predictions
  2. The distributions of the `probs` in a forest plot.

The first view looks neater, while the second provides HDI's.

First, the posterior predictions. This graph could be cleaner, but the lack 
of any apparent difference between treatments and controls kind of took the 
wind out of my sails, at least to the extent of fixing the 
indexing and re-looking-up how to 
customize legends in seaborn/matplotlib. The bins are split by control = 0 
and treatment = 1 (as if it matters), and ordered by ending stage (0 = stage 
1, ..., 9 = stage 10, 10 = stage Z). I suppose the main wrong thing with 
this model is how the probability of final stages earlier than starting 
stages is non-zero.

![Figure 5]({static}/images/science/sand_crabs/eggs/posterior_preds.png)

Second, the posterior probabilities arranged as ["end_stage", "start_stage", 
"grp"]. I think it's a bit interesting how the `end_stage` of zygote 
monotonically increases with `start_stage`, and non-zygote end stages kind 
of do a wave pattern indicating the most highly expected development of maybe 
5-ish stages (e.g. the [9, x, x] portion of the graph):

![Figure 5]({static}/images/science/sand_crabs/eggs/posterior_probs.png)

When it comes down to it, there's not a lot of data to go off of, though, 
and I don't think all this modeling work does a whole lot more than what 
could be eyeballed based on the descriptive stats/plots. 

# Conclusions
Keeping in mind the caveats of "not my experiment" and "I'm not an invert 
zoologist", I think that this experiment doesn't show any meaningful 
difference between treatments and controls in terms of egg development.

Probably the most valuable thing to come out of this exercise was the 
(pending) enhancement to PyMC's capabilities. I figure that even if I'd 
gotten to incorporate censoring into the model, all it would've done 
would've been to make the HDI's wider and maybe push some point estimates 
around.

# Discussion (but not what you're expecting)
I was thinking about the survival analysis from part 1, and it occurred to 
me that these "environmentally relevant concentrations" are if anything 
*low*, because in the wild, there is a continuously replenishing supply of 
microplastics for the crabs to eat, while this experiment capped their 
exposure: if one of the three plastics was eaten, then the ambient 
concentration was now two per jar, until the new batch was introduced. So 
the crabs in the wild should be hurting even more than this experiment 
suggests. Have people noticed sand crab population shifts? I feel like as a 
kid there were tons around at the beach, but even just a decade later they 
were much rarer, though that's a pretty flimsy bit of anecdotal evidence 
(for instance, I 
certainly went to the shore much less often as I got older).