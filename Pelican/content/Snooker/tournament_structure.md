Title: What Does Tournament Structure Matter?
Date: 2023-5-31
Category: Snooker
Tags: analysis

# The Situation
"Oh boy, Jersey Shore!" you might be thinking. Sorry, not today.

There are a few different tournament structures that they use in snooker. The three that I'm considering today are:

  1. Random draws:
    - Tournaments: ShootOut, British Open
    - Structure: What it says on the tin.
  2. Flat draws:
    - Tournaments: UK Championship prior to 2022
    - Structure: Seed 1 v 128, 2 v 127, ..., 64 v 65
  3. Tiered draws:
    - Tournaments: World Championship, UK 2022
    - Structure: Hard to describe. See [Wikipedia](https://en.wikipedia.org/wiki/2023_World_Snooker_Championship) for an example.

In general, the tournaments try to strike a balance of maximizing the spotlight for the stars without being too harsh on the non-stars. People want to see Neil Robertson (for instance), so his qualifying matches are against a low-ranked player and are held over to the main event just in case (Astley 😠), or he gets a bye to the last 32.

The common complaint with the flat draw structure is that it's unfair for the lower ranked players — particularly the new ones: "Congratulations on becoming a professional snooker player! Have fun playing Ronnie, Kyren, and Judd!" Poor Amine Amiri.

The tiered draw structure prevents that scenario. However, it means that the lower ranked you are, the more matches you have to play. That aspect was what I was particularly interested in: who benefits, who doesn't? It can't magically be better for everyone. 

The top players come in at the Last 32. The common asterisks brought up seem to be "match sharpness" and the added risk of no ranking points for a first-match loss. But surely only a madman would say, "No thanks, I'll pass on the bye to the Last 32 so that I can be match sharp." or "Good thing I'm ranked #17 in time for the Worlds!".

The bottom players have to play a whopping nine (9) rounds. On the one hand, they're playing lower ranked players compared to other structures, but on the other hand, nine rounds. Similarly, the two middle tiers of player have 8 and 7 rounds.

## Before We Begin
There'a a lot of words coming up. You might want to just skip to the bottom four graphs. The results probably won't surprise you (at least, they didn't surprise me).

# The Tournaments
I'm looking at:

  - UK Championship 2015-2022
    - Flat 2015-2021
    - Tiered 2022
  - British Open 2021-2022
    - Random
  - ShootOut 2016-2022
    - Random
  - World Championship 2019-2022
    - Tiered
      - Best of 11 pre-"Judgement Day" for 2019-2021
## Lumping Tournaments Together
I'd prefer to lump together all tournamentes with a given structure together and take their averages. There's not many tournaments in each group, so just being able to go from 4 to 5 would be nice.

### Flat Draws
The flat draw is easy: it's always the UK. 

![Figure 1]({static}/images/snooker/tournament_structure/flat_tournaments.png)

Overlapping dots are points that *were* on the same spot, so I nudged them to make sure all were visible. If there were no players left at a given round, they're at zero (i.e. not on the chart).

### Tiered Draws
The tiered draw tournaments' lump-ability largely depends on your belief in how much match length and tournament name matter. I'm convinced that match length is way overblown in terms of match outcomes, but am concerned about lumping the UK in with the Worlds. I'll plot the number of players who reached a given round, split out by their tier and the tournaments:

![Figure 2]({static}/images/snooker/tournament_structure/tiered_tournaments.png)

The WC 2022 is indistinguishable from 2019-2021. I'm less confident with the UK, which looks a bit different, but that looks mostly due to the good performance of the 17-48 ranked players (which included Ding!).

### Random Draws
The random draws are in the British Open and ShootOut, two very different tournaments. Here is the same graph as above, but for these tournaments:

![Figure 3]({static}/images/snooker/tournament_structure/random_tournaments.png)

Sorry that it's getting a bit pointillist. In the British Opens, the 17-48 tier looks to have done a bit better at the expense of the 81+ tier, but... well it's not a huge difference. I'm not particularly interested in the random draw right now. Maybe I should just leave the British Open out. We'll cross that bridge when we come to it.

### The Lumps
Actually, I'll just leave out the British Open and 2022 UK. I think including them would raise more doubts than the extra power is worth. I've looked at the subsequent charts in both scenarios, and they look close, so in the end it doesn't much matter.

# Average Outcomes
## Preliminary
### Using Averages
Are the averages useful metrics here? i.e. are any of the player counts wildly different between tournaments? Looking at the above three graphs, there are a few cases where things are pretty variable, but in general the averages look useful.
### How to Look at the Following Graphs
Because of the variable number of rounds that players play in the different tournament structures, there's not exactly an obvious way to compare them. You could...
  
  - Read things left to right.
    - This looks at the number of rounds that players have made it through.
  - Read things right to left.
    - This looks at how deep into a tournament players are getting.
  - Look at a middle point (Last 32)
    - This is where all the tournament types sync up.

## The Graphs, Split up by Player Tiers

![Figure 4]({static}/images/snooker/tournament_structure/avg_1-16.png)
![Figure 5]({static}/images/snooker/tournament_structure/avg_17-48.png)
![Figure 6]({static}/images/snooker/tournament_structure/avg_49-80.png)
![Figure 7]({static}/images/snooker/tournament_structure/avg_81plus.png)

I've rounded the average counts to the nearest whole numbers, because the graphs look way better this way. One issue that can't really go away is the differing number of rounds and entry points across tournament structure and player seeding. The result of this is that the lines you naturally try to make by connecting the dots aren't going to be quite right in most cases (e.g. L128 and L64 has L80 and L48 shoved in between).

## Assessing the Graphs
### Tier 1-16
Coming as no surprise, tiered tournaments are beneficial to these players. Unless they lose first round, which is now more likely.

### Tier 17-48
This group looks like it's most heavily footing the bill in the tiered tournaments. I mean, just look at that graph — they do worse than in the flat draws.

### Tier 49-80
Tiered tournaments seem to be beneficial to these players.
  
  - They tend to get about as deep into the tiered or flat draw tournaments.
  - They are a bit more likely to get to the Last 32 in tiered tournaments.
  - They are more likely to win at least one match (and two and three matches) in tiered tournaments.

### Tier 81+
It's more mixed for these players.

  - They tend to get farther into flat draw tournaments.
  - They are less likely to get to the Last 32 in tiered tournaments.
  - As with the tier 49-80, they are more likely to win at least one match (and two and three matches) in tiered tournaments.

# My Conclusions
My assessment of the above graphs is about what I thought the case would be beforehand.

  - Tiered tournaments are good for the top players, with extra risk of a first-match exit due to harder opponents.
  - Tiered tournaments are bad for players just outside the top 16. Like the top players, they have harder matches from the start, but they have more rounds to get through.
  - Tiered tournaments are arguably beneficial for low-to-mid-ranked players. They have easier early-rounds matches, but have to get through more rounds.
<!-- So how do these three tournament structures' average outcomes look?

![Figure 3]({static}/images/snooker/tournament_structure/avg_outcomes.png)

Firstly, this image appears too small (at least on my screen). You can get the full-sized image by right clicking on it and clicking on "Open Image in New Tab". -->