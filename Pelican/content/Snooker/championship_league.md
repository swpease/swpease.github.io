Title: It's A Coin Flip! (Part 2)
Date: 2023-5-16
Category: Snooker
Tags: analysis

# Intro
Continuing my attempts to demonstrate that winning shorter matches in snooker should not be belittled, here I wanted to look at the Championship League. The impetus for this is that John Higgins recently won the tournament for the fourth time, beating Judd Trump (who was also going for his fourth win). That's 7 out of 17 wins between them. Clearly there's a knack for these things.

The format of Championship League is kind of confusing, but here is a general outline:

  - Two stages:
    - Group Stage (7 total, 7 players each group)
    - Winner's Group (1 total, the 7 Group Stage winners)
  - Best of 5's.
  - Each group begins with a round robin format:
    - If you're in the top four after the round robin, you enter a play-off.
    - If you're #5, you're put into the next of the Group Stages.
    - If you're in the bottom two, you're eliminated from the tournament.
  - Play-off has the standard knock-out format.
    - If you win, you go on to the Winner's Group
    - If you don't, you're put into the next of the Group Stages.

So, to win the tournament, you need to win a Group Stage, and then win the Winner's Group. 4 of the 7 players in each group are put into the next Group Stage group. Except for after the last Group Stage group, of course. Group.

This is invitational, so players get to pick which group stage they'd like to enter into the tournament at.

# Set-up
I decided to look at it from the skeptical perspective: **Winning the tournament is random chance**. This means that I'm giving everyone a 1 in 7 chance of winning a given group. 

My thinking was:

  - John Higgins is one of the best players.
  - The odds of his four wins in a "roll of the dice" scenario is presumably quite low.
  - The lower the math works out for the odds to be, the stronger my position that these wins are skill-based.

# The Math
## Winning One Tournament
### Probabilities, Visualized
Pictures are nice. To see what I'm doing, here is an example probability tree, for someone entering in Group 5 (and ignoring the Winner' Group):

![Probability Tree]({static}/images/snooker/championship_league/snooker_CL_p_tree.png)

As an example of how to look at this, imagine:

  - The player is one of the 4 players who don't win Group 5, but aren't eliminated (i.e. not in the bottom 2 of the round robin phase). 
  - Then, they win Group 6.  

The probability of getting to the Winner's Group by that route is (4/7)*(1/7) = 4/49. 

Add up all of the routes-to-the-Winner's-Group probabilities to get the total probability of reaching the Winner's Group.

### Mathematical Formulation
The probability of advancing to the Winner's Group is:
$$  \sum_{r=0}^{n - 1} p_{win}*p_{next}^{r} $$
Where:

  - $n$ is the initial number of rounds remaining.
    - For example, if you entered in round 5 (always of 7), n is 3 (rounds 5, 6, and 7).
  - $p_{win}$ is the probability of winning a group.
    - Here, this means 1/7.
  - $p_{next}$ is the probability of going to the next Group Stage group.
    - Here, this means 4/7.

Since I'm assuming the probability of winning a group is always the same, the probability of winning the tournament is just 1/7 times the probability of reaching the Winner's Group:
$$  p_{win} * \sum_{r=0}^{n - 1} p_{win}*p_{next}^{r} $$

### In Python
Here is the above equation, in Python!

```python
def p_win_group_stage(num_rounds, p_win, p_next):
    """
    num_rounds: # of group stage rounds the player has, i.e # of opportunities to reach the final stage.
    p_win: Probability of winning a round (group or final)
    p_next: Probability of going to next Group Stage group (non-final rounds of group stage)
    """
    return sum([p_win * (p_next ** r) for r in range(num_rounds)])


def p_win_tourn(num_rounds, p_win, p_next):
    """
    num_rounds: # of group stage rounds the player has, i.e # of opportunities to reach the final stage.
    p_win: Probability of winning a round (group or final)
    p_next: Probability of going to next Group Stage group (non-final rounds of group stage)
    """
    return p_win * p_win_group_stage(num_rounds, p_win, p_next)
```

## Winning Multiple Tournaments
We have a binary outcome for each tournament (Win/Loss). Ordinarily, we could model our #-of-Wins with a binomial distribution. However, in our case, that doesn't work, because players can enter in different rounds of the Group Stage. If they do, then they have different probabilities of winning each tournament. This calls for the... **Poisson Binomial distribution**.
### The Poisson Binomial Distribution
The idea is just like the binomial distribution, except that each of the independent Bernoulli trials can have its own probability of success.

Both the Poisson Binomial and binomial distributions are the sums of their Bernoulli trials. As such, both can be found by taking the [convolution](https://en.wikipedia.org/wiki/Convolution_of_probability_distributions) of the Bernoulli trials.

This is all well and good, but it's not like you're going to calculate it by hand or write the function to calculate it. Well, I did out of curiosity, but then I just found a Python package that does it for me.

# The Odds of Higgins's Performance
**1 in 900** (ish, in a roll-of-the-dice scenario)

John Higgins played in 14 of the 17 Invitational Championship Leagues, entering in the following rounds (most recent first):

```python
# W  W           W  W
 [4, 7, 1, 6, 7, 7, 7, 1, 7, 5, 1, 1, 1, 3]
```

So he won 3 events where he entered in the final Group Stage group!

## The Poisson Binomial Code

```python
from poibin import PoiBin # An un-published package I found on GitHub. There are other options.


if __name__ == '__main__':
    p_win = 1 / 7
    p_next = 4 / 7
    max_rounds = 7
                      # W  W           W  W
    entered_in_round = [4, 7, 1, 6, 7, 7, 7, 1, 7, 5, 1, 1, 1, 3]
    num_rounds = [(max_rounds +  1) - rd for rd in entered_in_round]
    tourn_win_probs = [p_win_tourn(num_rds, p_win, p_next) for num_rds in num_rounds]
    pb = PoiBin(tourn_win_probs)
    p_over_3_wins = 1 - pb.cdf([3])
    print(1 / p_over_3_wins)
```

## Alternate Odds
I also checked the odds if we assume that Higgins will definitely get to the group playoffs (i.e. past the round robin phase), but the playoffs are still a dice roll. In code:

```python
    p_win = 1 / 4
    p_next = 3 / 4
```

In this scenario, the odds of Higgins's performance are way way better: **1 in 7**!

Just adding in a little bit of an edge in favor of Higgins quickly improves the odds of his performance, down to believable levels. Here's a full table of odds against Higgins's performance at various probabilities of winning (p_win) and getting to the next Group Stage group (p_next), with blue highlights on the (rounded) two scenarios I've considered above:

![Odds Table]({static}/images/snooker/championship_league/higgins_odds_table.png)

## Conclusion
**Even just rounding 1/7 and 4/7 to two digits (0.14 and 0.57) yields pretty different odds. It doesn't take much of a shift away from roll-of-the-dice to wind up in believeable odds territory, so my argument isn't air-tight, but it's something!**

### Code for the Above Table

```python
round_win_ps = np.linspace(0.14, 0.25, 12)
round_x_ps = np.linspace(0.28, 0.75, 48)
max_rounds = 7
                  # W  W           W  W
entered_in_round = [4, 7, 1, 6, 7, 7, 7, 1, 7, 5, 1, 1, 1, 3]
num_rounds = [(max_rounds +  1) - rd for rd in entered_in_round]

odds_over_3_wins_all = []
for win_p in round_win_ps:
    odds_over_3_wins = []
    for x_p in round_x_ps:
        p_wins = [p_win_tourn(num_rds, win_p, x_p) for num_rds in num_rounds]
        pb = PoiBin(p_wins)
        p = 1 - pb.cdf([3])
        p = p[0]
        odds = (1 - p) / p
        odds_over_3_wins.append(odds)
    odds_over_3_wins_all.append(odds_over_3_wins)
```


# Bonus: Brute Force!
I'm always a bit worried about my math when dealing with probabilities — it's so easy to make a mistake! So, I decided to make a brute force alternate formulation to check my math, and I guess kind of check my code. Voila:

```python
import numpy as np


def brute_force_single_tourn_outcome(num_rounds):
    rn = np.random.random()
    if rn < (1 / 7):  # Won
        return 1
    elif rn > (5 / 7):  # Eliminated
        return 0
    else:
        if num_rounds == 1:  # Eliminated b/c no more rounds.
            return 0
        else:  # Through to next round of group stage.
            return brute_force_single_tourn_outcome(num_rounds - 1)


def brute_force_p_win_tourn(n=100_000):
    for i in [1,2,3,4,5,6,7]:
        results = []
        for _ in range(n):
            results.append(brute_force_single_tourn_outcome(i))
        print(sum(results) / n)
```