"""Realtime KOSPI 200 futures/options quote subscription example."""
import os
from ls_openapi import LSOpenAPI
from ls_openapi.websocket import LSWebSocket

rest = LSOpenAPI()
with LSWebSocket(rest) as feed:
    feed.subscribe("FC9", os.environ["LS_FUTURES_CODE"])
    while True:
        print(feed.recv())
