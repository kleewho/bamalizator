import requests
import getopt, sys
import json
import sqlite3
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
verbose = True

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
category = soup.findAll("div", {"class": "topannouncement"})[0].div.div.div.p.get_text().split(' ')[0].lower()
(city, countryAndDate) = soup.findAll("div", {"class": "subheader-minisite"})[0].div.div.findAll("p")[0].get_text().split(',')
(day,month,year) = countryAndDate[-10:].split('.')


conn = sqlite3.connect('data/bam.db')
c = conn.cursor()
raceId = [r[0] for r in c.execute('select id from race where city = ? and year = ?', (city, year))][0]
routeId = [r[0] for r in c.execute('select id from route where category like ? and raceId = ?', (category, raceId))][0]

tableRows = soup.findAll('tr')[1:]
numberToName = {}
endOn = 0
for row in tableRows:
    if (verbose):
        print (row.get_text())
    tds = row.findAll("td")
    print(tds)
    number = str(int(tds[1].get_text()))
    textContainingName = filter(lambda el: len(el) > 0, [el.strip() for el in tds[0].get_text().split("\n")])[1]
    time = tds[-1].get_text()
    checkpointTime1 = tds[4].get_text()
    print(time)
    print(checkpointTime1)
    numberToName[number] = textContainingName
    if (verbose):
        print(("Name: %s" % (textContainingName)))
    c.execute('insert into bibNumber(number,year) values (?,?)',(number, year))
    c.execute('insert into raceResult(bibNumberId,raceId,routeId,time,checkpointTime1) values (?,?,?,?,?)',(1,1,1,time,checkpointTime1))

numberToNameFromFile = {}

try:
    with open("%s/%s_%s.json" % (directory, year, category)) as f:
        numberToNameFromFile = json.load(f)
except IOError as e:
    #swallow
    print("Swallowing IOError", e)

conn.close()

numberToName.update(numberToNameFromFile)

utf8NumberToName = {k : unicode(v).encode('utf8') for k, v in numberToName.items()}


with open("%s/%s_%s.json" % (directory, year, category), 'w') as f:
    json.dump(utf8NumberToName, f, ensure_ascii=False)

print (("Number to name dictionary for %s have already %s records" % (year, len(utf8NumberToName))))
