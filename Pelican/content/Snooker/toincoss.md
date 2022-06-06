Title: It's A Coin Flip!
Date: 2022-5-25
Category: Snooker
Tags: analysis

# The Problem
While I have only been watching snooker since the 2019 World Championship, I gather than matches have become shorter over time. People tend to complain that the shorter formats add a larger element of luck to the outcomes. I decided to try and put some numbers to this perception.

# The Data
I got the data from [snooker.org](snooker.org)'s API. I took data from the 2015/16 season through to the end of the past season (2021/22). I picked this timespan because it looks like the current rankings system [started then](http://api.snooker.org/help.html#RankingTypes). I looked at ranking events only, and only those first rounds of 128 players. I restricted to the round of 128 to try and keep things as even as possible (full draw, no "hot" players, etc.). I omitted walkovers, of which there are often one or two, and sometimes a lot (Gibralter Open 2022). To summarize:

  1. Seasons 2015/16 – 2021/22
  2. Ranking events
  3. First round only, of 128 players
  4. Walkovers excluded

# Basic Comparison
## Upsets by Tournament
Let's start by looking at things on a tournament-by-tournament basis over time, because that's how the data comes at us. What percentage of matches per tournament were upsets?

![Table 1]({static}/images/snooker/snooker_pct_upsets_by_season.png)

Hm. This isn't *super* informative... Let's ignore the seasons, group the tournaments by match length, and split out Top 16 seeds from the others:

![Table 2]({static}/images/snooker/snooker_num_upsets_by_tourn.png)

I guess longer matches make upsets a bit rarer, but it's hardly night and day. A handy thing about this plot is the two y-axes (# Upsets) go to 100%, so we can use the heights of the dots between the Top 16 seeds and the non-Top 16 seeds for percent-wise comparison. 

What are the actual numbers? 

## Upset Percentages
Now let's look at the upset percentages of all tournaments combined, split out by match length. I'll also split out the Top 16 seeds[^1] from the sub-Top 16 higher seeds. (See below[^2] for counts of the matches in each sub-group, so we know how many we're talking about. Important, but busy.) I'll include the Shoot-Out and British Open here and in any subsequent tables, even though I don't pay them much attention, because an extra line on a table is easier to ignore than extra lines/dots on a chart. Let's see:

![Table 4]({static}/images/snooker/snooker_total_upset_pct.png)

So, looking at Best of 9's – 11's, upsets are less likely in longer matches. **We can expect one more Top 16 Seed to be upset in Best of 7's compared to Best of 11's (2 -> 3, of 16), and three more non-Top 16 Seeds (13 -> 16, of 48)**. For reference: 

  - 20% = 1 in 5 
  - 17% = 1 in 6 
  - 14% = 1 in 7 
  - 12% = 1 in 8 

Case closed! Right? Well... these matches aren't all between the same seedings each time. How much does that change things?

# Factoring in Match Difficulty
## Upset Potentials Defined
Seed 2 losing to seed 42 is a bigger upset than seed 42 losing to seed 82. To account for this aspect of the rankings, I converted the seeds using the base-2 logarithm, which I'll write as `log2(seed)`. If you're unfamiliar with logarithms, here are some reference values to get the gist:

![Table 6]({static}/images/snooker/snooker_lg_ref.png)

I created a metric from these logarithmed seedings that I called **upset potential**, which is just the size of the difference in the match's two players' logarithmed seedings, i.e.:

  - **upset potential** = `log2(higher seed) - log2(lower seed)`

I set any amateurs' seeding as 128. I also think of the upset potential as equating to **skill gap**. For instance, Yan (16) losing to Ding (32) has an upset potential of 1.00, and Ding losing to Ursenbacher (62) has an upset potential of 0.95. Does that sound about right to you?[^3]

## Splitting Out the Upset Potentials
Here are the average upset potentials, split out by match length:

![Table 7]({static}/images/snooker/snooker_upset_potential.png)

A smaller upset potential means the match had players closer in seeding. So we see that, moving from Best of 7 to Best of 11, the average upset potential increased, which means that **the higher seeded players had easier matches on average with increasing match length**. How much easier? Well, the Top 16 Seeds had on average an upset potential in their matches 0.4 greater in Best of 11 compared to Best of 9. That's like playing Seed 28 instead of Seed 21, Seed 42 instead of Seed 32, or Seed 84 instead of Seed 64!


And the same info, further split by whether an upset occurred:

![Table 8]({static}/images/snooker/snooker_upset_potential_split.png)

So, for a given match length, the upsets have a smaller average upset potential compared to the non-upsets, i.e. upsets happen when the players are closer in skill level. Obviously. This happens across the board. Wait... what about the Top 16 seeds in the Best of 11? Top 16 seeds have been more likely to lose against *worse* players in Best of 11s these past several years! Oh dear.


## Splitting Out the Upset Potentials Even More
### Upset Percents, Grouped by Upset Potential
Well, so how does a higher seed do for a given upset potential, i.e. against players of the same skill gap, across the match lengths? Here is the data, rounding down the upset potentials to the nearest whole number:

![Table 9]({static}/images/snooker/snooker_u_p_barplt_log2.png)

50% upsets is the proverbial coin flip. The blue / orange / green bars show what has *actually happened*, while the black lines at the top of each bar are the 95% confidence intervals. Essentially, the longer the black line, the less trust you should put in the corresponding colored bar staying where it is as more data is collected. Some of these are pretty huge (Top 16 upset potential of 0, 1, 6, 7). I'm guessing there aren't many data points... Nope. See here[^4].

Well, in that case, let's use that other upset potential metric from Footnote [^3] and see what happens. The counts look better[^5], so how does the plot look?:

![Table 10]({static}/images/snooker/snooker_u_p_barplt_ceillog2div4.png)

So it looks pretty similar, except at higher upset potentials for Top 16 matches, which was exactly the point.

#### Conclusions
What can we get out of these plots? 

  - **At a given upset potential (skill gap), there are more instances of the expected pattern of increasing match length yielding decreasing upset % *not* happening than happening.** 
  - **At a given skill gap, the differences in upset % usually and at most equate to differences of a few more/fewer upsets.** Maximums: 
    - For Top-16 Seeds: 3 fewer in Best of 11 vs Best of 7 at upset potential of 2.
    - For non-Top-16 Seeds: 4 fewer in Best of 11 vs Best of 9 (note: not 7!) at upset potential of 0.
  - **At a given match length, increasing skill gap makes upsets less and less likely, with the notable exception of Top 16 seeds in Best of 11's, for which the opposite trend is true.**

## Yet Another View
### Percent Realized Upset Potential
One last way I wanted to look at the data is comparing the total upset potential for a tournament against the amount of that upset potential that actually occurred.

"Percent realized upset potential" a lot of words; let's unpack it. We've established what "upset potential" means. "Realized" refers to the upsets that actually happened. "Percent" refers to totaling the realized upset potentials, and dividing by the total upset potentials over all the matches in the tournament round.

A simple example: only two matches in the round, Match 1 has an upset potential of 3, while Match 2 has an upset potential of 1. If neither is an upset, the percent realized upset potential is 0%. If both are upsets, it is 100%. If Match 1 is an upset while Match 2 isn't, it is 3/4 = 75%. If Match 2 is an upset while Match 1 isn't, it is 1/4 = 25%.

Here's what it looks like:

![Table 11]({static}/images/snooker/snooker_pct_realized_u_p.png)

There seem to be a few aspects in favor of either side of the argument.

**Points in favor of match length mattering:**

  - The Shoot-Out and British Open are at the upper end of percent realized upset potential.
  - The Best of 7's at similar total upset potential to longer matches are also at the upper end of percent realized upset potential in that subset.

However, in both cases there are not very many data points. Even so, I suspect neither the Shoot-Out nor the British Open data will budge much in coming years, given their unique formats.

**Points in favor of match length not mattering:**

  - The Best of 9's seem to have a similar distribution to the Best of 7's at the lower total upset potentials, along with a similar distribution to the Best of 11's at the higher total upset potentials. 

Finally, a general point about the graph:

  - The percent realized upset potential seems to get both less variable and on average smaller as the total upset potential increases. However, the match lengths tend to increase as total upset potential increases, confounding the relationship. 

# Conclusions
I think the major takeaways from this analysis are:

  - **Upsets are more likely in shorter matches.**
  - **Shorter matches tend to be against harder opponents for higher seeds.**
  - **At a given skill gap, there isn't a consistent relationship between match length and the chances of an upset.**

That's all for now! I hope you at least gave the graphs a good look.


[^1]: Note I said "Seeds", not "Ranking". So the defending champion is Seed 1. Yes, it's a smidge imprecise, but using rankings would have been a lot more effort for minimal gain.

[^2]: ![Table 5]({static}/images/snooker/snooker_split_upset_pct.png)

[^3]: I know it's not perfect, but I tried a more complicated transformation, namely `1 + log2(ceil(seeding / 4))`, which seemed closer to correct to me, but the graphs wound up looking basically the same, so I decided to keep the simpler transformation.

[^4]: ![Table 6 supp_1]({static}/images/snooker/snooker_u_p_bin_counts_log2.png)
 ![Table 6 supp_2]({static}/images/snooker/snooker_u_p_bin_counts_log2_non-top16_plt.png)
![Table 6 supp_3]({static}/images/snooker/snooker_u_p_bin_counts_log2_top16_plt.png)

[^5]: ![Table 7 supp]({static}/images/snooker/snooker_u_p_bin_counts_stuffdiv4.png)
![Table 7 supp_2]({static}/images/snooker/snooker_u_p_bin_counts_stuffdiv4_non-top16_plt.png)
![Table 7 supp_3]({static}/images/snooker/snooker_u_p_bin_counts_stuffdiv4_top16_plt.png)
