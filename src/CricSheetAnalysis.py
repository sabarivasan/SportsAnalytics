import yaml
import csv

# {
#    "Johnston" : {
#                    "overs" : 10
#                    "runs" : 172
#                    "extras": 10
#                  }
#    "Bowler B" : {
#                    "overs" : 10
#                    "runs" : 172
#                    "extras": 10
#                  }
#  }
bowling_figures = {}

def create_bowling_figures(deliveries):
    for d in deliveries:
        for k in d:
            bowler = d[k]["bowler"]
            print "Ball = {} Bowler={}".format(k, bowler)
            if bowler not in bowling_figures:
                bowling_figures[bowler] = { "overs": 0, "runs": 0, "extras": 0}
            bowling_figures[bowler]["runs"] += d[k]["runs"]["total"]
            bowling_figures[bowler]["extras"] += d[k]["runs"]["extras"]

def write_bowling_figures():
    with open("/Users/sabarivasan/work/SportsAnalytics/data/cricket/bowling_figures.csv", "w") as csv_file:
        csv_obj = csv.writer(csv_file)
        for b in bowling_figures:
            bf = bowling_figures[b]
            csv_obj.writerow([b, bf["runs"], bf["extras"]])


with open("/Users/sabarivasan/work/SportsAnalytics/data/cricket/odis.zip Folder/225171.yaml", "r") as match_file:
    obj = yaml.load(match_file)
    teams = obj["info"]["teams"]
    print "Match was played between {} and {}".format(teams[0], teams[1])

    create_bowling_figures(obj["innings"][0]["1st innings"]["deliveries"])


    write_bowling_figures()

