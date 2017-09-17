import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

scores = []
with open("/Users/sabarivasan/work/SportsAnalytics/data/cricket/Tendulkar-HowStat.csv", "r") as file:
    for r in csv.reader(file):
        if r[6].endswith("*"):
            score = int(r[6][:-1])
        elif "-" == r[6]:
            continue
        else:
            score = int(r[6])
        scores.append(score)

print "Found {} scores, {}".format(len(scores), scores)

def runningMean(x, N):
    y = np.zeros((len(x),))
    for ctr in range(len(x)):
         y[ctr] = np.sum(x[ctr:(ctr+N)])
    return y/N

def moving_avg(arr, N):
    cumsum, moving_aves = [0.], []
    for i, x in enumerate(arr, 1):
        cumsum.append(cumsum[i - 1] + x)
        if i >= N:
            moving_ave = (cumsum[i] - cumsum[i - N]) / N
            # can do stuff with moving_ave here
            moving_aves.append(moving_ave)
    return moving_aves

last_N = 3

mov_avg = moving_avg(scores[:-1], last_N)
print "Running mean has size {}. {}".format(len(mov_avg), mov_avg)


x = [[a] for a in mov_avg]
print "x = {}".format(x)

y = scores[last_N:]
print "y has size {}. {}".format(len(y), y)
assert len(mov_avg) == len(y)
train_percent = 80
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
plt.scatter(x_test, y_test,  color='black')
plt.plot(x_test, y_pred, color='blue', linewidth=3)

plt.show()
