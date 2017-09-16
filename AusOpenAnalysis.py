import csv
import sys
import math
from matplotlib import pyplot as plt
import numpy as np

MATCHES_CSV = "/Users/sabarivasan/work/SportsAnalytics/tennis_slam_pointbypoint/2017-ausopen-matches.csv"
POINTS_CSV = "/Users/sabarivasan/work/SportsAnalytics/tennis_slam_pointbypoint/2017-ausopen-points.csv"

def avg(arr):
    return sum(arr)/len(arr)

def get_match_id(player1, player2):
    with open(MATCHES_CSV, "r") as matches_file:
        for row in csv.DictReader(matches_file):
            if ( (row["player1"] == player1 or row["player2"] == player1)
                and (row["player1"] == player2 or row["player2"] == player2)):
                p1 = player1 if row["player1"] == player1 else player2
                p2 = player2 if row["player2"] == player2 else player1
                return (p1, p2, row["match_id"])

    return None

def analyze_by_rally_length(match_id):
    max_rally_length = 0
    rally_winners_by_length = [[0, 0] for i in range(50)]
    # for i in range(50):
    #     rally_winners_by_length[i] = [0, 0]
    with open(POINTS_CSV, "r") as matches_file:
        for row in csv.DictReader(matches_file):
            if row["match_id"] == match_id and "RallyCount" in row and int(row["RallyCount"]) > 0:
                rally_count = int(row["RallyCount"])
                if rally_count > max_rally_length:
                    max_rally_length = rally_count
                rally_winners_by_length[rally_count - 1][int(row["PointWinner"]) - 1] += 1
    del rally_winners_by_length[max_rally_length:]
    rally_lengths = [i + 1 for i in range(max_rally_length)]
    plt.plot(rally_lengths, rally_winners_by_length)
    plt.xlabel([player1, player2])
    plt.show()



def enumerate(match_id, analysis_cls):
    max_rally_length = 0
    rally_winners_by_length = [[0, 0] for i in range(50)]
    # for i in range(50):
    #     rally_winners_by_length[i] = [0, 0]
    with open(POINTS_CSV, "r") as matches_file:
        for row in csv.DictReader(matches_file):
            if row["match_id"] == match_id:
                analysis_cls.offer(row)

    analysis_cls.done()

class AnalyzeServeByGameScore:

    def __init__(self, player1, player2):
        self.point_numbers = ["0", "15", "30", "40"]
        self.keys = [self.key(n1, n2) for n1 in self.point_numbers
                                      for n2 in self.point_numbers]
        self.keys.append("40/AD")
        self.keys.append("AD/40")
        self.point_numbers.append("AD")
        self.serve_speeds = [{}, {}]

        self.prev_key = None
        self.player1 = player1
        self.player2 = player2

    def key(self, p1Score, p2Score):
        return p1Score + "/" + p2Score

    def offer(self, row):
        p1_score = row["P1Score"]
        p2_score = row["P2Score"]
        point_winner = row["PointWinner"]
        point_server = row["PointServer"]
        key = None
        serve_speed = int(row["Speed_KMH"])
        set_num = int(row["SetNo"])
        if serve_speed <= 0:
            return

        if self.prev_key:
            key = self.prev_key

        if point_server == "1":
            # if point_winner == "1":
            #    key = self.key(self.point_numbers[self.point_numbers.index(p1_score) - 1], p2_score)
            # else:
            #    key = self.key(p1_score, self.point_numbers[self.point_numbers.index(p2_score) - 1])
            stat_obj = self.serve_speeds[0]
            self.prev_key = self.key(p1_score, p2_score)
        elif point_server == "2":
           # if point_winner == "2":
           #     key = self.key(self.point_numbers[self.point_numbers.index(p2_score) - 1], p1_score)
           # else:
           #     key = self.key(p2_score, self.point_numbers[self.point_numbers.index(p1_score) - 1])
           stat_obj = self.serve_speeds[1]
           self.prev_key = self.key(p2_score, p1_score)

        if key:
            if not key in stat_obj:
                stat_obj[key] = []

            stat_obj[key].append(serve_speed)


    def done(self):
        avg_serve_speeds = [[], []]
        for k in self.keys:
            for n in range(2):
                stat_obj = self.serve_speeds[n]
                avg_serve_speeds[n].append(avg(stat_obj[k]) if k in stat_obj else 0)


        # data to plot
        n_groups = len(self.keys)

        # create plot
        plt.subplots()
        index = np.arange(n_groups)
        bar_width = 0.35
        opacity = 0.8

        plt.bar(index, avg_serve_speeds[0], bar_width,
                alpha=opacity,
                color='blue',
                label=self.player1)

        plt.bar(index + bar_width, avg_serve_speeds[1], bar_width,
                alpha=opacity,
                color='green',
                label=self.player2)

        plt.xlabel('Point Score')
        plt.ylabel('Serve Speed (km/h')
        plt.title('Serve speed analysis by point score')
        plt.xticks(index + bar_width, self.keys)
        plt.legend()

        plt.tight_layout()
        plt.show()


        # sp = plt.subplot(111)
        # sp.bar(1, self.num_brk_pts[0], color='b',width=0.2)
        # sp.bar(1.2, self.saved_brk_pts[0], color='b', width=0.2)
        #
        # sp.bar(2, self.num_brk_pts[1], color='g', width=0.2)
        # sp.bar(2.2, self.saved_brk_pts[1], color='g', width=0.2)
        # plt.legend("Break points faced by " + player1, "Break points faced by " + player2)
        plt.show()

class AnalyzeByBreakPoint:

    def __init__(self, player1, player2):
        self.p1_brk_pts_lost = [0] * 5
        self.p1_brk_pts_saved = [0] * 5
        self.p2_brk_pts_lost = [0] * 5
        self.p2_brk_pts_saved = [0] * 5
        self.player1 = player1
        self.player2 = player2
        self.curr_set = None

    def offer(self, row):
        p1_score = str(row["P1Score"])
        p2_score = str(row["P2Score"])
        set_num = int(row["SetNo"])
        # if self.is_p1_brk_point(p1_score, p2_score):
        if row["P1BreakPoint"] == "1":
           if row["PointWinner"] == "1":
               self.p2_brk_pts_lost[set_num - 1] += 1
           else:
               self.p2_brk_pts_saved[set_num - 1] += 1
        # elif self.is_p1_brk_point(p2_score, p1_score):
        elif row["P2BreakPoint"] == "1":
           if row["PointWinner"] == "2":
               self.p1_brk_pts_lost[set_num - 1] += 1
           else:
               self.p1_brk_pts_saved[set_num - 1] += 1


    def is_p1_brk_point(self, p1_score, p2_score):
        return ("40" == p2_score and p1_score in ["0", "15", "30"]) or ("AD" == p2_score and p1_score == "40")

    def done(self):
        # data to plot
        n_groups = 5

        # create plot
        plt.subplots()
        index = np.arange(n_groups)
        bar_width = 0.35
        opacity = 0.8

        plt.bar(index, self.p1_brk_pts_lost, bar_width,
                alpha=opacity,
                color='blue',
                label=self.player1 + " - break points lost")
        plt.bar(index, self.p1_brk_pts_saved, bar_width,
                alpha=opacity,
                color='lightblue',
                bottom=self.p1_brk_pts_lost,
                label=self.player1 + " - break points saved")

        plt.bar(index + bar_width, self.p2_brk_pts_lost, bar_width,
                alpha=opacity,
                color='green',
                label=self.player2 + " - break points lost")
        plt.bar(index + bar_width, self.p2_brk_pts_saved, bar_width,
                alpha=opacity,
                color='lightgreen',
                bottom=self.p2_brk_pts_lost,
                label=self.player2 + " - break points saved")

        plt.xlabel('Set')
        plt.ylabel('Break points')
        plt.title('Break point analysis')
        plt.xticks(index + bar_width, [("Set " + str(n + 1)) for n in range(5)])
        plt.legend()

        plt.tight_layout()
        plt.show()


        # sp = plt.subplot(111)
        # sp.bar(1, self.num_brk_pts[0], color='b',width=0.2)
        # sp.bar(1.2, self.saved_brk_pts[0], color='b', width=0.2)
        #
        # sp.bar(2, self.num_brk_pts[1], color='g', width=0.2)
        # sp.bar(2.2, self.saved_brk_pts[1], color='g', width=0.2)
        # plt.legend("Break points faced by " + player1, "Break points faced by " + player2)
        plt.show()



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: python AusOpenAnalysis.py player1 player2"
        exit(1)

    player1, player2, m_id = get_match_id(sys.argv[1], sys.argv[2])
    if (not m_id):
        raise "Could not find match between {} and {}" % (player1, player2)
    else:
        print "Match between %s and %s has match id %s" % (player1, player2, m_id)


    # 6-4, 3-6, 6-1, 3-6, 6-3.
    #analyze_by_rally_length(m_id)

    # enumerate(m_id, AnalyzeByBreakPoint(player1, player2))

    enumerate(m_id, AnalyzeServeByGameScore(player1, player2))








