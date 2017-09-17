import yaml


with open("/Users/sabarivasan/work/SportsAnalytics/data/cricket/odis.zip Folder/225171.yaml", "r") as match_file:
    obj = yaml.load(match_file)
    teams = obj["info"]["teams"]
    print "Match was played between {} and {}".format(teams[0], teams[1])
    print len(obj["innings"][0]["1st innings"]["deliveries"])


