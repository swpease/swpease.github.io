Title: Causal Inference: What If, Part 1
Date: 2026-06-01
Category: Statistics
Tags: statistics

# Introduction
I was exposed to the concept of causal inference in the excellent 
Statistical Rethinking series/book, by Richard McElreath. I suppose I had 
been exposed to it indirectly via my scientific education, but not in the 
formal sense of back-door criterion, etc. Anyway, I decided to try and 
expand/harden my understanding of the concepts, and found the book [Causal 
Inference: What If](https://miguelhernan.org/whatifbook) via this helpful 
[blog post](https://www.bradyneal.com/which-causal-inference-book).

# Preliminary Review
In evaluating a textbook, I think one of the most effective things to do is 
to find a section of the text that you already have an understanding of, and 
see how well you can follow the author's attempt at explaining it. 

Doing that with this textbook, I'm kind of on the fence. I read through 
four or five chapters about half a year ago, and called it quits for the 
time. I remember thinking that I kind of lost apart in terms of the purpose. 
It didn't help that I was more or less familiar with the concepts being 
introduced, which can flag your interest. I feel like this text 
leans a 
bit too far into the 
mathematics 
at the expense of pedagogy. I also feel like the presentation of the math in 
narrative form, by which I mean, written in paragraphs, kind of obfuscates 
what's being said. I'm not sure what the solution there is, although I am a 
big fan of colorized math. I think that can probably help here. I was left 
wondering how to translate what I was reading into actual real life problems,
i.e. "So what?", that most important of questions, though that might come later in the book.

Supporting my opinion, I found a set of [blog posts](https://www.manifoldmadness.com/blog/whatif/notes/chapter1) going over this text. These 
posts stopped at Chapter 4. Coincidence? Or is this a... causal association?

I think it is quite useful to have an accompanying intro epidemiology book on 
hand to reference/read along with. I have the book by Gordis, from my own 
days as a public health student. 

I'm planning on providing some commentary on things that I think could be 
done better, in a series of posts.

# Chapter 1
This introduces causal inference. 

My main gripe with it is how the 
terminology, specifically the mathematical symbols, is given a quick 
run-down. I wish that authors would reiterate what objects these symbols 
represent when they are used, at least for a chapter or two, and maybe an 
occasional, "remember, this means \[stuff\]" in later chapters; students 
aren't practicing professionals. 

This issue came up in Chapter 2 (I guess I'll say it now), where the author 
introduces the mathematical representation of exchangeability. I found 
myself using my understanding of exchangeability in order to figure out what 
the math was saying. That's always a sore spot for me.

Also, the authors introduce a couple of different "consistency"ies. This 
word appears to mean roughly "trustworthy": consistent observations match 
the "true" counterfactual outcomes, and consistent estimators provide 
estiimates of "true" parameter values that tend to improve as you 
collect 
more 
data. 

# Chapter 2
Beyond my math notation gripe listed above, which came to a head here, my 
main issue was in converting the conditional randomized study design into 
English, dammit!

## Conditional Randomization
I feel the authors could have gone more deeply into the merits and rationale 
for such a study design. Or maybe just separated it out into its own section.
For instance, the concept of effect modification is buried, in my opinion. As a 
contrast, Gordis expresses that you might use 
this (at least, if "conditional randomization" == "stratified randomization")
if 
you wanted to be sure that 
something that might impact 
the outcome 
(e.g. sex) is equally distributed between treatments, because random chance 
could lead to (e.g.) uneven M/F ratios in groups.

### Calculating Population-level Estimates in C.R. Experiments
The authors take up a lot of space here. The overall principle to calculate 
population-level estimates in these studies is:

1. Use the principle of exchangeability to say "the observed 
   distribution of outcomes for this 
   treatment within this stratum holds for the entire stratum".
2. Calculate the weighted mean across strata.

You have a few options of how to get there (written for binary outcome):

1. take the (proportion with outcome)
2. multiply that by either:
    1. (stratum size, as a proportion of total pop)
    2. (stratum size, as a number)
3. add these up across all strata

Route 2.1 gets you a population-level proportion, while 2.2 provides the 
answer as a count. You can interchange between them by * or / by the 
population size, respectively.

Going with method 2.1 is "standardization". "Inverse probability weighting" 
is technically a third route, wherein you use (# with outcome) / ( treatment 
group
size, as a proportion of stratum size), which nets you the same as route 2.2. 
Really, whichever method you use 
will probably just depend on what information is on hand, to minimize the 
cognitive overhead. I think that these two names and their associated 
mathematese just obfuscate a fairly straightforward concept.

# I forgot about this.
I dropped this again at the start of chapter 4. Chapter 3 was a slog. 
Chapter 4 didn't seem to be providing me with anything revolutionary to make 
it worth the effort, and I couldn't see any purpose in continuing to read.