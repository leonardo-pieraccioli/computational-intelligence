For the whole results and a more accurate reading of data I suggest to read the HalloweenChallenge.ipynb file. This file is just a summary of the results.

# Best solution

| Num Points & Sets | Density | Solution Size | Number of Cycles |
| ----------------- | ------- | ------------- | ---------------- |
| 100               | .3      | 11            | 38               |
| 1000              | .3      | 17            | 22               |
| 5000              | .3      | 18            | 33               |
| 100               | .7      | 3             | 10               |
| 1000              | .7      | 6             | 13               |
| 5000              | .7      | 7             | 14               |

Reached with a maximum of total failed improvements of 5. 

# Conclusions

After a reading of the output we can see that having a maximum of consecutive improvements rather than total, does not give any advantage in terms of quality of the solution. Of course if we run the program with a maximum of improvements we will use less cycles, therefore the solution could be worse, but found with less cycles.