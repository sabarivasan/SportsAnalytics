import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

# How many last scores to take average of?
last_N = 10
# What percentage of the data is training (remaining is test)
train_percent = 50

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
    y = np.zeros(len(x) - N + 1)
    for ctr in range(len(x) - N + 1):
        y[ctr] = np.average(x[ctr:ctr+N])
    return y



mov_avg = runningMean(scores[:-1], last_N).tolist()
print "Running mean has size {}. {}".format(len(mov_avg), mov_avg)


x = [[a] for a in mov_avg]
print "x = {}".format(x)

y = scores[last_N:]
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
plt.scatter(x_test, y_test,  color='black')
plt.plot(x_test, y_pred, color='blue', linewidth=3)

plt.show()
