import numpy as np
import matplotlib.pyplot as plt

bowler = { "name": "Shane Warne" , "country" : "Australia"}

ball_by_ball = [0, 1, 4, 0, 6, 0, 0, 1, "W", 6, 0, 0, 2, 1, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 3, 1, 0, 0,
           2, 1, 3, 0, 6, 0, 2, 0, 0, 6, 0, 0, "W", 3, 1, 2, 4, "W", 0, 0, 2, 0, 0, 0, 4, 1, 6, 1, 2, 1]

sum = float(0)
num_wickets = 0
for r in ball_by_ball:
    if type(r) == int:
        sum += r
    elif r == "W":
        num_wickets += 1

econ_rate = sum/len(ball_by_ball) * 6

print "{}: economy rate (runs per over) = {}".format(bowler["name"], econ_rate)
print "{}: num wickets = {}".format(bowler["name"], num_wickets)

ball_by_ball_cleansed = [r if type(r) == int else 0 for r in ball_by_ball]


h = np.histogram(ball_by_ball_cleansed, bins=6)

plt.hist(ball_by_ball_cleansed, bins=6)
plt.xlabel("Runs conceded")
plt.ylabel("Number of occurrences")
plt.title("Histogram of runs conceded by " + bowler["name"])
plt.show()






