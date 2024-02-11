# ES Agent to optimize a strategy for the game of Nim

This was a (failed) attempt to use an Evolutionary Strategy (ES) agent to choose a good strategy for the game of Nim. 

## Initial Goal

1. Try to implement an ES agent in a game environment
2. Refresh the concept of ES and its implementation
3. Properly implement gaussian mutation and uniform crossover
4. Learn how to use multifile and classes in python

## Idea

I built a function that used 3 different strategies to pick a row and three different strategies to pick how many matches to remove. Each strategy had a probability of beeing selected and the ES agent would optimize these probabilities. 

## Problems

### "Agent"

I don't thing the term "Agent" is correct here. The agent here uses the parameters from the ES algorithm to choose a strategy, not to play. 

### Bad strategy function

The second error was to set the selection of a strategy to each move and not for a whole game. In this way the agent was not trying to search for the best combination of strategies, but to optimize the probability of selecting a strategy for each move. This resulted in an almost random strategy, in fact it performed really similarly. 

### Lack of exploration 

By using a gaussian mutation and a uniform crossover, the agent was not able to really explore the space of strategies. In fact, even after many generations, the best individual was very similar to the initial one. This is because instead of generating the first individuals with a random probability of selecting a strategy, I used a fixed uniform one. Moreover the mutation was not able to change the probability of selecting a strategy by a lot, given that it just shuffled the probabilities a little bit.

### Parameters of generations and individuals

Here I blame my partial understanding of ES at the time I wrote this code. I used a population size of 10, but worse I only selected one single parent to generate the next generation. This is not a good approach, again, because it totally destroys the exploration of the space of strategies and it does not really count as implementation of the ES.

## The half full glass

Apart from the mess, I learned a lot from this attempt, especially by making all this errors. By reviewing the concepts I could see where I went wrong and how to fix it. I also learned a lot about how to use classes and multifile in python and I'm quite happy with the result, even if I think it could be better and at the end I introduced a lot of clutter and confusion in the code.

Also I now understand the mechanism of game environments and how to implement an agent in it. This is a good start for the next attempts

Now I have many ideas on how to really exploit an ES and where is useless to use it. I'm looking forward to try again and see if I can do better.

# Bye!

If someone is interested in this, I hope this can be a good way to learn what NOT to do :). 