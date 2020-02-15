import requests
import getopt, sys
import json
import glob
import os

fullCmdArguments = sys.argv
argumentList = fullCmdArguments[1:]
print (argumentList)

unixOptions = "hd:a:"
gnuOptions = ["help", "dir=", "assets-dir="]
verbose = False

try:
    arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))
    sys.exit(2)


for currentArgument, currentValue in arguments:
    if currentArgument in ("-h", "--help"):
        print ("displaying help")
    elif currentArgument in ("-d", "--dir"):
        directory = currentValue
    elif currentArgument in ("-a", "--assets-dir"):
        assets = currentValue

if not directory:
    print ("directory is missing")
    sys.exit(2)

if not assets:
    print ("assets directory is missing")
    sys.exit(2)

files = [f for f in glob.glob(directory + "/*.json")]

for f in files:
    basename = os.path.basename(f)
    (idString, category) = basename.replace(".json", "").split("_")
    id = int(idString)
    year = idString[0:4]
    with open(f) as openedFile:
        participantsJson = json.load(openedFile)
    print(len(participantsJson))
    with open("%s/%s.json" % (assets, year)) as openedFile:
        seasonJson = json.load(openedFile)

    for r in seasonJson["races"]:
        print(r['id'])
        if (r[u'id'] == id):
            print("found")
            print(r)
            r[unicode(category, 'utf-8')] = len(participantsJson)
            print(r)
    print(seasonJson)











