"""Quickstart using the domain-oriented SDK facade."""
import os

from ls_openapi import LSClient

client = LSClient()
code = os.environ["LS_FUTURES_CODE"]

quote = client.market.quote(code)
print(quote.get("t2111OutBlock", quote))
