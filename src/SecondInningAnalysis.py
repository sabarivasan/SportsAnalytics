"""
This program runs a model for predicting the 2nd innings score as a function of 2 features:
 - run_rate required to win the match
 - # of wickets in hand
"""
import yaml
import csv

num_overs_per_innings = 50
bowling_figures = {}


with open("/Users/sabarivasan/work/SportsAnalytics/data/cricket/cricsheet-odi-ball_by_ball/225171.yaml", "r") as match_file:
    obj = yaml.load(match_file)
    teams = obj["info"]["teams"]
    print "Match was played between {} and {}".format(teams[0], teams[1])

    print "Ist innings - %s" % obj["innings"][0]["1st innings"]["team"]
    first_inn_balls = obj["innings"][0]["1st innings"]["deliveries"]
    second_inn_balls = obj["innings"][1]["2nd innings"]["deliveries"]
    wickets_fallen = 0
    running_score = 0
    with open("/Users/sabarivasan/work/SportsAnalytics/data/cricket/running_score.csv", "w") as csv_file:
        csv_obj = csv.writer(csv_file)
        csv_obj.writerow([obj["innings"][0]["1st innings"]["team"]])
        csv_obj.writerow(["Ball", "Runs", "Running Score", "Wickets Fallen"])
        for b in first_inn_balls:
            for k in b:
                runs = int(b[k]["runs"]["total"])
                running_score += runs
                if "wicket" in b[k]:
                    wickets_fallen += 1

                csv_obj.writerow([k, runs, running_score, wickets_fallen])
        print "2nd innings - %s chasing %d runs" % (obj["innings"][1]["2nd innings"]["team"], running_score)

        csv_obj.writerow([obj["innings"][1]["2nd innings"]["team"]])
        csv_obj.writerow(["Ball", "Runs", "Running Score", "Wickets Fallen", "Runs remaining", "Required Run Rate", "Wickets in hand"])

        runs_remaining = float(running_score + 1)

        balls_remaining = 6 * num_overs_per_innings
        required_run_rate = runs_remaining / balls_remaining

        running_score = 0
        wickets_fallen = 0
        for b in second_inn_balls:
            for k in b:
                runs = int(b[k]["runs"]["total"])
                if "wicket" in b[k]:
                    wickets_fallen += 1
                csv_obj.writerow([k, runs, running_score, wickets_fallen, runs_remaining, required_run_rate, 10 - wickets_fallen])
                if not "extras" in b[k]:
                    balls_remaining -= 1
                runs_remaining -= runs
                required_run_rate = runs_remaining / balls_remaining
