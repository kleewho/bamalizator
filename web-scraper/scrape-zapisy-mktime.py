import requests
import getopt, sys
import json
import sqlite3
from bs4 import BeautifulSoup

class BamRepository():
    def __init__(self):
        self.conn = sqlite3.connect('data/bam.db')

    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()

    def saveRace(self, date, city, year):
      print('Saving race')
      c = self.conn.cursor()
      c.execute('insert into race(date,city,year) values(?,?,?) on conflict do nothing', (date,city,year))
      return [r[0] for r in c.execute('select id from race where date = ?', (date,))][0]

    def saveRoute(self, raceId, distance, category):
      print('Saving route')
      c = self.conn.cursor()
      c.execute('insert into route(raceId,distance,category) values(?,?,?) on conflict do nothing', (raceId,distance,category))
      return [r[0] for r in c.execute('select id from route where category like ? and raceId = ?', (category, raceId))][0]

    def saveBibNumber(self, number, year):
      print("Saving bibNumber %s for year %s" % (number, year))
      c = self.conn.cursor()
      c.execute('insert into bibNumber(bibNumber,year) values(?,?) on conflict do nothing', (number,year))
      print('Fetching bibNumberId using select')
      bibNumberId = [r[0] for r in c.execute('select id from bibNumber where bibNumber = ? and year = ?', (number,year))][0]
      print("Current bibNumberId %s" % (bibNumberId))
      return bibNumberId

    def saveRaceResult(self, bibNumberId, routeId, time, checkpoint1, DNS, DNF, DSQ):
      print("Saving raceResult for bibNumberId %s and routeId %s" % (bibNumberId, routeId))
      c = self.conn.cursor()
      c.execute('insert into raceResult(bibNumberId,routeId,time,checkpointTime1,DNS,DNF,DSQ) values(?,?,?,?,?,?,?) on conflict do nothing', (bibNumberId,routeId,time,checkpointTime1,DNS,DNF,DSQ))

      return c.lastrowid

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
distance = int(soup.findAll("div", {"class": "topannouncement"})[0].div.div.div.p.get_text().split(' ')[1])
(city, countryAndDate) = soup.findAll("div", {"class": "subheader-minisite"})[0].div.div.findAll("p")[0].get_text().split(',')
(day,month,year) = countryAndDate[-10:].split('.')

with BamRepository() as bamRepository:
  raceId = bamRepository.saveRace(("%s-%s-%s" % (year,month,day)),city,year)
  print(raceId)
  routeId = bamRepository.saveRoute(raceId, distance, category)
  print(routeId)

  tableRows = soup.findAll('tr')[1:]
  numberToName = {}
  endOn = 0
  for row in tableRows:
      if (verbose):
          print (row.get_text())
      tds = row.findAll("td")
      print(tds)
      number = str(int(tds[1].get_text()))
      bibNumberId = bamRepository.saveBibNumber(number, year)
      textContainingName = filter(lambda el: len(el) > 0, [el.strip() for el in tds[0].get_text().split("\n")])[1]
      time = tds[-1].get_text()
      DNF = False
      DNS = False
      DSQ = False
      if time.upper() == 'DNF':
          time = ""
          DNF = True
      elif time.upper() == 'DNS':
          time = ""
          DNS = True
      elif time.upper() == 'DSQ':
          time = ""
          DSQ = True
    
      checkpointTime1 = tds[4].get_text()
      print(time)
      print(checkpointTime1)
      numberToName[number] = textContainingName
      if (verbose):
          print(("Name: %s" % (textContainingName)))

      bamRepository.saveRaceResult(bibNumberId, routeId, time, checkpointTime1, DNS, DNF, DSQ)


# numberToNameFromFile = {}

# try:
#     with open("%s/%s_%s.json" % (directory, year, category)) as f:
#         numberToNameFromFile = json.load(f)
# except IOError as e:
#     #swallow
#     print("Swallowing IOError", e)

# conn.close()

# numberToName.update(numberToNameFromFile)

# utf8NumberToName = {k : unicode(v).encode('utf8') for k, v in numberToName.items()}


# with open("%s/%s_%s.json" % (directory, year, category), 'w') as f:
#     json.dump(utf8NumberToName, f, ensure_ascii=False)

# print (("Number to name dictionary for %s have already %s records" % (year, len(utf8NumberToName))))

