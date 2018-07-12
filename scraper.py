import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from datetime import timedelta
import pytz
import scraperwiki

def queryHourlyRainfall(y, m, d, h):
    r = requests.get(
        "http://www.hko.gov.hk/wxinfo/rainfall/rf_record_e.shtml",
        params={
            "form": "rfrecorde",
            "Selday": d,
            "Selmonth": m,
            "Selhour": h,
        })

    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table", title="Table of the rainfall recorded in various regions")
    hour_data = []
    if (table != None):
        for tr in table.find_all("tr"):
            td = tr.find_all("td")
            if (td[0].text not in 'Region'):
                if (re.search("to (\d+)", td[1].text)):
                    max = re.search("to (\d+)", td[1].text).group(1)
                else:
                    max = re.search("(\d+)", td[1].text).group(0)
                region_data = dict(
                    datetime_region = '{}-{}-{}-{}'.format(m, d, h, td[0].text),
                    # month = m,
                    # day = d,
                    # hour = h,
                    # region = td[0].text,
                    minRain = re.search("(\d+)", td[1].text).group(0),
                    maxRain = max
                )
                hour_data.append(region_data)
    return(hour_data)


def queryDailyRainfall(y, m, d):
    daily_data = []
    for h in range(0, 24):
        #print("{} {}".format(h, queryHourlyRainfall(d, m, str(h).zfill(2))))
        daily_data.append(queryHourlyRainfall(y, m, d, str(h).zfill(2)))
    return (daily_data)

hkt = pytz.timezone('Asia/Hong_Kong')
ytd = datetime.now().replace(tzinfo=hkt)-timedelta(days=1)
ytdY = ytd.strftime("%y")

#daily = queryDailyRainfall(ytdY, ytd.strftime("%m"), ytd.strftime("%d"))
daily = queryDailyRainfall("18", "06", "05")

for hour in daily:
    for h in hour:
        h['key'] = '{}-{}'.format(ytdY, h['datetime_region'])
        scraperwiki.sqlite.save(unique_keys=['key'], data=h)
        #print(h)
