import json
import sqlite3
from collections import defaultdict
year = 2019
class BamDb():
    def __init__(self):
        self.conn = sqlite3.connect('data/bam.db')

    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()

    def executeQuery(self, sql, params = tuple()):
        c = self.conn.cursor()
        return c.execute(sql, params).fetchall()

    countDnfsPerRacePerCategoryQuery = """
    SELECT ra.id,ro.id,count(*)
    FROM raceResult raRe
    JOIN route ro ON raRe.routeId = ro.id
    JOIN race ra ON ro.raceId = ra.id
    WHERE ra.year = ?
    AND DNF = ?
    AND DNS = ?
    AND DSQ = ?
    GROUP BY ra.id, ro.category, raRe.DNF, raRe.DNS, raRe.DSQ
    """

    def countRacersByRouteId(self, DNF=False, DNS=False, DSQ=False):
        return {r[1]:r[2]  for r in self.executeQuery(self.countDnfsPerRacePerCategoryQuery, (year, DNF,DNS,DSQ))}

def groupBy(how, what):
    return reduce(lambda grp, val: grp[how(val)].append(val) or grp, what, defaultdict(list))

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

with BamDb() as bamDb:
    listRacesQuery = """
SELECT 
ra.id,ro.id,ra.city,ro.category,ra.date
FROM route ro 
JOIN race ra ON ro.raceId = ra.id 
WHERE ra.year = ?
ORDER BY ra.date, ro.category
"""
    raceBasicData = [{'raceId':r[0], 'routeId':r[1], 'city':r[2], 'category':r[3], 'date':r[4]} for r in bamDb.executeQuery(listRacesQuery,(year,))]

    default = {i:0 for i in range(len(raceBasicData) + 1)}
    finished = merge_two_dicts(default, bamDb.countRacersByRouteId())
    dnfs = merge_two_dicts(default, bamDb.countRacersByRouteId(DNF=True))
    dnss = merge_two_dicts(default, bamDb.countRacersByRouteId(DNS=True))
    dsqs = merge_two_dicts(default, bamDb.countRacersByRouteId(DSQ=True))

    racesGrouped = groupBy(lambda val: val['raceId'], raceBasicData)

    totalFinished = 
    totalDnf = 
    totalDns = 
    totalDsq = 
    for i,(raceId, raceInfo) in enumerate(racesGrouped.items()):
        print(i+1)

        categories = [{'category': ro['category'],
        'racersFinished': finished[ro['routeId']],
        'dnf': dnfs[ro['routeId']],
        'dns': dnss[ro['routeId']],
        'dsq': dsqs[ro['routeId']]}
        for ro in raceInfo]

        a = {'id': ("%s_%s" % (year, i+1)),
            'city': raceInfo[0]['city'],
            'date': raceInfo[0]['date'],
            'categories': categories
            }
        print(a)
        



