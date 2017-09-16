
bowler = "Shane Warne"

ball_by_ball = [0, 1, 4, 0, 6, 0, 0, 1, 2, 6, 0, 0, 2, 1, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 3, 1, 0, 0,
           2, 1, 3, 0, 6, 0, 2, 0, 0, 6, 0, 0, 1, 3, 1, 2, 4, 6, 0, 0, 2, 0, 0, 0, 4, 1, 6, 1, 2, 1]

sum = float(0)
for r in ball_by_ball:
    sum += r

econ_rate = sum/len(ball_by_ball) * 6

print "{}: economy rate (runs per over) = {}".format(bowler, econ_rate)






