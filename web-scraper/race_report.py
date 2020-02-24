import json
import sqlite3
from collections import defaultdict
import io
import getopt
import sys

year = 2019

fullCmdArguments = sys.argv
argumentList = fullCmdArguments[1:]

unixOptions = "hy:d:"
gnuOptions = ["help", "year=", "dir="]
verbose = True

try:
    arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
except getopt.error as err:
    # output error, and return with an error code
    print(str(err))
    sys.exit(2)


for currentArgument, currentValue in arguments:
    if currentArgument in ("-h", "--help"):
        print("displaying help")
    elif currentArgument in ("-y", "--year"):
        year = currentValue
    elif currentArgument in ("-d", "--dir"):
        directory = currentValue


class BamDb():
    def __init__(self):
        self.conn = sqlite3.connect('data/bam.db')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()

    def executeQuery(self, sql, params=tuple()):
        c = self.conn.cursor()
        return c.execute(sql, params).fetchall()

    countByRaceAndCategory = """
    SELECT ra.id,ro.id,count(*)
    FROM raceResult raRe
    JOIN route ro ON raRe.routeId = ro.id
    JOIN race ra ON ro.raceId = ra.id
    WHERE ra.year = ?
    AND DNF = ?
    AND DNS = ?
    AND DSQ = ?
    GROUP BY ra.id, ro.category
    """

    def countRacersByRouteId(self, DNF=False, DNS=False, DSQ=False):
        return {r[1]: r[2] for r in self.executeQuery(self.countByRaceAndCategory, (year, DNF, DNS, DSQ))}

    def executeAndGetSingleValue(self, sql, params=tuple()):
        c = self.conn.cursor()
        return c.execute(sql, params).fetchall()[0][0]


def groupBy(how, what):
    return reduce(lambda grp, val: grp[how(val)].append(val) or grp, what, defaultdict(list))


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


listRacesQuery = """
SELECT 
ra.id,ro.id,ra.city,ro.category,ra.date
FROM route ro 
JOIN race ra ON ro.raceId = ra.id 
WHERE ra.year = ?
ORDER BY ra.date, ro.category
"""


def percent(what, total):
    return float(what)/total


def calculateParticipants(finished, dnf, dns, dsq):
    participants = finished + dnf + dsq
    return {'participants': participants,
            'finished': finished,
            'dnf': dnf,
            'dns': dns,
            'dsq': dsq,
            'percentDnf': percent(dnf, participants),
            'percentDns': percent(dns, participants)}


def createCategory(category, finished, dnf, dns, dsq):
    return merge_two_dicts({'category': ro['category']}, calculateParticipants(finished, dnf, dns, dsq))


def sumInCategories(key, categories):
    return reduce(lambda sum, c: sum + c[key], categories, 0)


with BamDb() as bamDb:
    print("Creating report for year %s" % (year,))
    raceBasicData = [{'raceId': r[0], 'routeId':r[1], 'city':r[2], 'category':r[3],
                      'date':r[4]} for r in bamDb.executeQuery(listRacesQuery, (year,))]

    default = {i: 0 for i in range(len(raceBasicData) + 1)}
    finished = merge_two_dicts(default, bamDb.countRacersByRouteId())
    dnfs = merge_two_dicts(default, bamDb.countRacersByRouteId(DNF=True))
    dnss = merge_two_dicts(default, bamDb.countRacersByRouteId(DNS=True))
    dsqs = merge_two_dicts(default, bamDb.countRacersByRouteId(DSQ=True))

    racesGrouped = groupBy(lambda val: val['raceId'], raceBasicData)

    participants = bamDb.executeAndGetSingleValue(
        "select count(*) from bibNumber where year = ?", (year,))

    races = []
    for i, (raceId, raceInfo) in enumerate(racesGrouped.items()):
        print("Building data for city %s" % (raceInfo[0]['city'],))

        categories = [createCategory(ro['category'],
                                     finished[ro['routeId']],
                                     dnfs[ro['routeId']],
                                     dnss[ro['routeId']],
                                     dsqs[ro['routeId']])
                      for ro in raceInfo]

        raceParticipants = calculateParticipants(sumInCategories('finished', categories),
                                                 sumInCategories(
                                                     'dnf', categories),
                                                 sumInCategories(
                                                     'dns', categories),
                                                 sumInCategories('dsq', categories))

        race = merge_two_dicts({'id': int(year) * 100 + i + 1,
                                'city': raceInfo[0]['city'],
                                'date': raceInfo[0]['date']
                                }, raceParticipants)

        for c in categories:
            category = c.pop('category')
            race[category] = c
        races.append(race)

    yearReport = {
        'year': int(year),
        'participants': participants,
        'races': races}

    fullPath = "%s/%s.json" % (directory, year)
    with io.open(fullPath, 'w', encoding='utf8') as fp:
        print("Dumping report to %s" % (fullPath))
        data = json.dumps(yearReport, fp, ensure_ascii=False)
        fp.write(data)
