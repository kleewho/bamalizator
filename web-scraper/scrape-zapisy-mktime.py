import requests
import getopt, sys
import json
from bs4 import BeautifulSoup

def is_int(value):
  try:
    int(value)
    return True
  except:
    return False

fullCmdArguments = sys.argv
argumentList = fullCmdArguments[1:]
print (argumentList)

unixOptions = "hu:y:d:"
gnuOptions = ["help", "url=", "year=", "dir="]
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
    elif currentArgument in ("-u", "--url"):
        url = currentValue
        print (("url to scrape (%s)") % (currentValue))
    elif currentArgument in ("-y", "--year"):
        year = currentValue
    elif currentArgument in ("-d", "--dir"):
        directory = currentValue


if not url:
    print ("url is missing. Tell me what do you want to scrape, please")
    sys.exit(2)

if not year:
    print ("year is missing")
    sys.exit(2)

if not directory:
    print ("directory is missing")
    sys.exit(2)

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
tableRows = soup.findAll('tr')[1:]
numberToName = {}
endOn = 0
for row in tableRows:
    if (verbose):
        print (row.get_text())
    tds = row.findAll("td")
    number = str(int(tds[1].get_text()))
    textContainingName = filter(lambda el: len(el) > 0, [el.strip() for el in tds[0].get_text().split("\n")])[1]
    numberToName[number] = textContainingName
    if (verbose):
        print(("Name: %s" % (textContainingName)))

numberToNameFromFile = {}

try:
    with open("%s/%s.json" % (directory, year)) as f:
        numberToNameFromFile = json.load(f)
except IOError as e:
    #swallow
    print("Swallowing IOError", e)

numberToName.update(numberToNameFromFile)

utf8NumberToName = {k : unicode(v).encode('utf8') for k, v in numberToName.items()}


with open("%s/%s.json" % (directory, year), 'w') as f:
    json.dump(utf8NumberToName, f, ensure_ascii=False)

print (("Number to name dictionary for %s have already %s records" % (year, len(utf8NumberToName))))
