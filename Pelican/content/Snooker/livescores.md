Title: Livescore Graphics Wishes
Date: 2023-7-25
Category: Snooker
Tags: analysis

# Introduction
WST has in the past provided livescores and recent results for matches. The livescores showed:

  - Who was at the table and their current break.
  - The current frame's score and points remaining.
  - The match score.
  - Average shot times for the match.

Strangely, they also offered the scores for each frame of the match, but only made it available after the match was finished, unless you went to [snooker.org](snooker.org), which somehow had these links mid-match.

They are rolling out a new scoring site. A temporary one is currently up, which has had issues (e.g. wrong scores). I **hope** that this new site takes more advantage of the shot-by-shot data, because I think that there is a lot of potential to make things more interesting.

# My Wish List
The WST does not to my knowledge publish information about the frames of matches it oversees. Luckily, the [WPBSA site](https://snookerscores.net/) has tournament histories with matches and frame information. This **does not** include WST matches, but does include other snooker organizations, such as the Women's and Seniors' tours. In most cases, the frame data was manually recorded, so it is not there, but in some cases, such as the [British Women's Open](https://snookerscores.net/tournament-manager/2023-british-womens-open/results), some of the matches **do** have what are called a **"frame sheet"**. These frame sheets list the shot time and outcomes of the shots for each shot of the frame ([example](https://snookerscores.net/scoreboard/frame/9iwyicyxumm5vmp7iocqod7mwhnimjcg/sheet)).

Below are a couple of prototype graphics I've created from a WPBSA frame sheet from the 2023 British Women's Open final between Bai Yulu and Reanne Evans. Assuming that the WST has the data required to generate such a frame sheet for its own matches, I think things along these lines would be great additions to the livescoring site.

Also, I'm aware that it should be "Bai" rather than "Yulu" in the legends. I just copied over the data.

## 1. Scores over Time
![Figure 1]({static}/images/snooker/livescores/frame_scores.png)

This figure shows the scores of each player over the course of the frame. 

  - The colored circles indicate which colored ball was potted at that time (hopefully obvious). 
  - The red "X"s indicate where a player fouled. In this match, Reanne fouled five times. 
  - The yellow band(s) indicate where in the match there were snookers required.


## 2. Shot Outcomes over Time
![Figure 2]({static}/images/snooker/livescores/frame_actions.png)

This figure shows the outcome of each player's shots over the course of the frame.

I like how this graph provides a snapshot of the match that is complementary to the first graph. You can see things such as: 

  - Where a break went awry.
  - Who played a good (dare I say, telling) safety resulting in fouls.
  - Where a safety battle occurred.

## Ending Remarks
These are just prototype graphs. I like them, but there are presumably other directions you can go with the data. I considered lumping the two together, but it looked so busy in my mental image that I didn't even actually try it.

I do hope that the new WST livescore site takes better advantage of the frame data; you can really paint a picture with it.