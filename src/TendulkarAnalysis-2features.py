"""
This program does a linear regression of Tendulkar's scores based on 2 features:
1) Recent batting form as represented by the last N scores
2) Opponent team ranking as represented by the Team Rankings obtained in Sep 2017.
"""
import csv
import numpy as np
from AnalyticsUtil import run_model
# How many last scores to take average of?
last_N = 5
# What percentage of the data is training (remaining is test)
train_percent = 50
# Team ranking to use when we don't know the team ranking
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
    run_col_index = 5
    team_col_index= 2

    with open("/Users/sabarivasan/work/SportsAnalytics/data/cricket/Tendulkar-subset.csv", "row") as file:
        for row in csv.reader(file):
            if row[run_col_index].endswith("*"):
                r = int(row[run_col_index][:-1])
            elif "-" == row[run_col_index]:
                continue
            else:
                r = int(row[run_col_index])

            rankings.append(get_team_ranking(row[team_col_index], team_rankings))
            runs.append(r)
    print "Found {} scores".format(len(runs))
    return (runs, rankings)


def running_mean(x, N):
    y = np.zeros(len(x) - N + 1)
    for ctr in range(len(x) - N + 1):
        y[ctr] = np.average(x[ctr:ctr + N])
    return y


def analyze_batting_data():
    global mov_avg, x, y
    team_rankings = load_team_rankings()
    (runs, rankings) = load_batting_data(team_rankings)
    mov_avg = running_mean(runs[:-1], last_N).tolist()
    print "Running mean has size {}. {}".format(len(mov_avg), mov_avg)
    x = [[mov_avg[n], rankings[n + last_N]] for n in range(len(mov_avg))]
    x = np.array(x)
    # print "x = {}".format(x)
    y = np.array(runs[last_N:])
    # print "y has size {}. {}".format(len(y), y)
    assert len(x) == len(y)

    run_model(x, y, train_percent, "/Users/sabarivasan/work/SportsAnalytics/data/cricket/Tendulkar-model-results.csv")


analyze_batting_data()


