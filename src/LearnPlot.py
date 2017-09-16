from matplotlib import pyplot as plt
import numpy as np



def plot():
    years = [1950, 1960]

    gdp = [[300, 150], [543.2, 172]]

    plt.plot(years, gdp)

    plt.show()



def simple_bar():
    objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
    y_pos = np.arange(len(objects))
    performance = [10,8,6,4,2,1]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Usage')
    plt.title('Programming language usage')

    plt.show()

def horiz_bar():
    plt.rcdefaults()
    objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
    y_pos = np.arange(len(objects))
    performance = [10,8,6,4,2,1]

    plt.barh(y_pos, performance, align='center', alpha=0.5)
    plt.yticks(y_pos, objects)
    plt.xlabel('Usage')
    plt.title('Programming language usage')

    plt.show()

def multiple_bars():

    # data to plot
    n_groups = 4
    means_frank = [90, 55, 40, 65]
    means_guido = [85, 62, 54, 20]

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, means_frank, bar_width,
                     alpha=opacity,
                     color='b',
                     label='Frank')

    rects2 = plt.bar(index + bar_width, means_guido, bar_width,
                     alpha=opacity,
                     color='g',
                     label='Guido')

    plt.xlabel('Person')
    plt.ylabel('Scores')
    plt.title('Scores by person')
    plt.xticks(index + bar_width, ('A', 'B', 'C', 'D'))
    plt.legend()

    plt.tight_layout()
    plt.show()


def stacked_bars():
    # a stacked bar plot with errorbars

    N = 5
    menMeans = (20, 35, 30, 35, 27)
    womenMeans = (25, 32, 34, 20, 25)
    menStd = (2, 3, 4, 1, 2)
    womenStd = (3, 5, 2, 3, 3)
    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, menMeans, width, color='#d62728', yerr=menStd)
    p2 = plt.bar(ind, womenMeans, width,
                 bottom=menMeans, yerr=womenStd)

    plt.ylabel('Scores')
    plt.title('Scores by group and gender')
    plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
    plt.yticks(np.arange(0, 81, 10))
    plt.legend((p1[0], p2[0]), ('Men', 'Women'))

    plt.show()

if __name__ == "__main__":

    # simple_bar()
    # horiz_bar()
    # multiple_bars()
    stacked_bars()



