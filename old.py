import requests
from bs4 import BeautifulSoup
import re

def queryHourlyRainfall(d, m, h):
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
                    day = d,
                    month = m,
                    hour = h,
                    region = td[0].text,
                    minRain = re.search("(\d+)", td[1].text).group(0),
                    maxRain = max
                )
                hour_data.append(region_data)
    return(hour_data)


def queryDailyRainfall(d, m):
    daily_data = []
    for h in range(0, 24):
        #print("{} {}".format(h, queryHourlyRainfall(d, m, str(h).zfill(2))))
        daily_data.append(queryHourlyRainfall(d, m, str(h).zfill(2)))
    return (daily_data)

print(queryDailyRainfall("06", "06"))
