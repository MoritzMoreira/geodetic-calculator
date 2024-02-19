import json

datei = {"P0": {"y": 0.0,"x":500.0},
"P1": {"y": 179.20, "x": 352.69},
"PN": {"y": 466.17, "x": 793.75},
"PN+1": {"y": 223.81, "x": 916.95}}

dateirunds = {"r1": 71.1530, "s1": 148.11, "r2": 218.0123, "s2": 135.25, "r3": 211.5327, "s3": 121.17, "r4": 212.3319, "s4": 138.28, "r5": 73.1133}

with open('punkte_polygon.json','w') as json_datei:
    json.dump(datei,json_datei, sort_keys=True, indent=4)

with open('runds_polygon.json','w') as json_datei:
    json.dump(dateirunds,json_datei, sort_keys=True, indent=4)



