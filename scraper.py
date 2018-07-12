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
                    y_m_d_h_region = '{}-{}-{}-{}-{}'.format(y, m, d, h, td[0].text),
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


###
def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

start_dt = datetime(2018, 4, 2)
end_dt = datetime(2018, 7, 12)
for dt in daterange(start_dt, end_dt):
    daily = queryDailyRainfall(dt.strftime("%y"), dt.strftime("%m"), dt.strftime("%d"))
    for hour in daily:
        for h in hour:
            scraperwiki.sqlite.save(unique_keys=['y_m_d_h_region'], data=h)
            print(h)

###
# hkt = pytz.timezone('Asia/Hong_Kong')
# ytd = datetime.now().replace(tzinfo=hkt)-timedelta(days=1)
# ytdY = ytd.strftime("%y")
#daily = queryDailyRainfall(ytdY, ytd.strftime("%m"), ytd.strftime("%d"))
# for hour in daily:
#     for h in hour:
#         scraperwiki.sqlite.save(unique_keys=['y_m_d_h_region'], data=h)
#         print(h)
# print(ytd.strftime("%Y-%m-%d"))