import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

# How many last scores to take average of?
last_N = 5
# What percentage of the data is training (remaining is test)
train_percent = 50

unknown_team_ranking = 11


def load_team_rankings():
    team_rankings = {}
    with open("/Users/sabarivasan/work/SportsAnalytics/data/cricket/ODI-Team-Rankings.csv", "r") as file:
        for r in csv.DictReader(file):
            team_rankings[r["Team"].upper()] = int(r["Ranking"])
    return team_rankings


def get_team_ranking(team, team_rankings):
    return team_rankings[team.upper()] if team.upper() in team_rankings else unknown_team_ranking

def load_batting_data(team_rankings):
    runs = []
    rankings = []
    with open("/Users/sabarivasan/work/SportsAnalytics/data/cricket/Tendulkar-Batting-ODIs.csv", "row") as file:
        for row in csv.reader(file):
            if row[6].endswith("*"):
                r = int(row[6][:-1])
            elif "-" == row[6]:
                continue
            else:
                r = int(row[6])

            rankings.append(get_team_ranking(row[2], team_rankings))
            runs.append(r)
    print "Found {} scores".format(len(runs))
    return (runs, rankings)


def running_mean(x, N):
    y = np.zeros(len(x) - N + 1)
    for ctr in range(len(x) - N + 1):
        y[ctr] = np.average(x[ctr:ctr + N])
    return y


team_rankings = load_team_rankings()
(runs, rankings) = load_batting_data(team_rankings)
mov_avg = running_mean(runs[:-1], last_N).tolist()
print "Running mean has size {}. {}".format(len(mov_avg), mov_avg)

x = [[mov_avg[n], rankings[n + last_N]] for n in range(len(mov_avg))]
print "x = {}".format(x)

y = runs[last_N:]
print "y has size {}. {}".format(len(y), y)
assert len(mov_avg) == len(y)

train_size = len(mov_avg) * train_percent / 100
print "Size of X = {}, Size of training set = {}".format(len(mov_avg), train_size)

x_train = x[:-train_size]
y_train = y[:-train_size]
x_test = x[-train_size:]
y_test = y[-train_size:]

regr = linear_model.LinearRegression()
regr.fit(x_train, y_train)
print('Intercept:{}, Coefficients: {}\n'.format(regr.intercept_, regr.coef_))

# Make predictions using the testing set
y_pred = regr.predict(x_test)

# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(y_test, y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(y_test, y_pred))

# Plot outputs

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax = fig.gca(projection='3d')
#ax.scatter(x_test, y_test, color='black')
ax.plot(x_test, y_pred, color='blue', linewidth=3)

plt.show()
