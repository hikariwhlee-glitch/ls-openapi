"""Domestic futures current quote example (t2111)."""
import os
from ls_openapi import LSOpenAPI

client = LSOpenAPI()
# Replace with the current futures code shown in LS Securities' product information.
result = client.call("t2111", {"focode": os.environ["LS_FUTURES_CODE"]})
print(result)
