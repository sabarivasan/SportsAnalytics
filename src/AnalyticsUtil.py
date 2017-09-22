import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

def run_model(x, y, train_percent, out_file_name):
    train_size = len(x) * train_percent / 100
    test_size = len(x) - train_size
    print "Size of data = {}, Size of training set = {}, Size of test set = {}".format(len(x), train_size, test_size)
    x_train = x[:train_size]
    y_train = y[:train_size]
    x_test = x[train_size:]
    y_test = y[train_size:]
    regr = linear_model.LinearRegression()
    regr.fit(x_train, y_train)
    print('Intercept:{}, Coefficients: {}\n'.format(regr.intercept_, regr.coef_))
    # Make predictions using the testing set
    y_pred = regr.predict(x_test)
    print "Predicted values = {}\n".format(y_pred)
    # The mean squared error
    print("Mean squared error: %.2f"
          % mean_squared_error(y_test, y_pred))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % r2_score(y_test, y_pred))

    with open(out_file_name, "w") as out_csv:
        # Header row
        # x1, x2, y_actual, y_pred, theta0, theta1, theta2, y_pred_check
        for n in range(x.shape[1]):
            out_csv.write("x%d," % (n + 1))
        out_csv.write("y_actual,y_pred,")
        for n in range(x.shape[1] + 1):
            out_csv.write("theta%d," % n)
        out_csv.write("y_pred_check")
        out_csv.write("\n")

        out_csv.write("Training Data\n")
        for row_num in range(x.shape[0]):
            if row_num == train_size:
                out_csv.write("Test Data\n")

            for n in range(x.shape[1]):
                out_csv.write("%f," % x[row_num][n])
            out_csv.write("%f," % y[row_num])  #y_actual

            if row_num < train_size:
                out_csv.write(",")
            else:
                out_csv.write("%f," % y_pred[row_num - train_size])
                out_csv.write("%f," % regr.intercept_)  # theta0
                for n in range(x.shape[1]):  # theta values
                    out_csv.write("%f," % regr.coef_[n])
            out_csv.write("\n")



    # Plot outputs

    # Plot predicted value of y vs actual
    innings_num = [n + 1 for n in range(test_size)]
    plt.plot(innings_num, y_test, "go")
    plt.plot(innings_num, y_pred, "b")
    plt.yticks()
    plt.show()

    # 3-D plot of features vs y
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax = fig.gca(projection='3d')
    # ax.scatter(x_test[:, 0], x_test[:, 1], y_pred, color='blue', linewidth=1)
    # ax.scatter(x_test[:, 0], x_test[:, 1], y_test, color='green', linewidth=1)
    # plt.show()

