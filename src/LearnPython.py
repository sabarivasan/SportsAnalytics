import matplotlib.pyplot as plt

ball_by_ball = [2, 1, 3, "WIDE", 6, 0, 2, 0, 0, 6, 0, 0, 3, 3, "NB", 2, 4, 2, 0, 0, 2, 0, "W", 0, 4, 1, 6, 1, 2, 1,
4, 1, 2, 0, 4, "W", 2, 0, "W", 6, 1, 2, 3, 4, 5, 2, 4, 2, 0, 0, 2, 2, 0, 3, 4, 1, 6, 1, 2, 3]

ball_by_ball_cleansed = [r if type(r) == int else (1 if r in ["WIDE, NB"] else 7) for r in ball_by_ball]
print ball_by_ball_cleansed

def sum(l):
    sum = 0.0
    for v in l:
        if type(v) == int:
            sum += v
        elif is_no_ball(v) or is_wide(v):
            sum += 1
    return sum

def is_wicket(v):
    return "W" == v

def is_wide(v):
    return "WIDE" == v

def is_no_ball(v):
    return "NB" == v

num_wickets = 0
for r in ball_by_ball:
    if is_wicket(r):
        num_wickets += 1

run_rate = 6 * (sum(ball_by_ball)/len(ball_by_ball))

print "Runs conceded = {}, num of wickets = {}, # balls bowled = {}, Run rate = {}".\
    format(sum(ball_by_ball), num_wickets, len(ball_by_ball), run_rate)



plt.hist(ball_by_ball_cleansed, bins=7)
plt.show()

