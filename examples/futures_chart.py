"""Domestic futures tick-chart request example (t8464)."""
import os
from datetime import date
from ls_openapi import LSOpenAPI

client = LSOpenAPI()
today = date.today().strftime("%Y%m%d")
result = client.call("t8464", {
    "shcode": os.environ["LS_FUTURES_CODE"], "ncnt": 1, "qrycnt": 200,
    "nday": 0, "sdate": today, "stime": "", "edate": today,
    "etime": "", "cts_date": "", "cts_time": "", "comp_yn": "N",
})
print(result)
