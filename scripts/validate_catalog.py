"""Validate the packaged TR catalog against the checked-in official index."""
from __future__ import annotations
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TR_CATALOG = runpy.run_path(str(ROOT / "ls_openapi" / "catalog.py"))["TR_CATALOG"]
with (ROOT / "specs" / "official-sample-index.json").open(encoding="utf-8") as f:
    official = {item["code"]: item for item in json.load(f)["transactions"]}

errors: list[str] = []
if set(TR_CATALOG) != set(official):
    errors.append(f"TR code mismatch: missing={sorted(set(official)-set(TR_CATALOG))}, extra={sorted(set(TR_CATALOG)-set(official))}")
for code, item in TR_CATALOG.items():
    ref = official.get(code)
    if not ref:
        continue
    for field in ("name", "path", "protocol"):
        if item.get(field) != ref.get(field):
            errors.append(f"{code}: {field} differs (catalog={item.get(field)!r}, official={ref.get(field)!r})")
    should_be_order = item["protocol"] == "REST" and item["path"] == "/futureoption/order"
    if item["is_order"] != should_be_order:
        errors.append(f"{code}: order safety flag does not match order endpoint")

rest = [x for x in TR_CATALOG.values() if x["protocol"] == "REST"]
websocket = [x for x in TR_CATALOG.values() if x["protocol"] == "WEBSOCKET"]
orders = [x for x in rest if x["is_order"]]
if len(TR_CATALOG) != 91 or len(rest) != 60 or len(websocket) != 31 or len(orders) != 6:
    errors.append(f"Unexpected counts: all={len(TR_CATALOG)}, REST={len(rest)}, WS={len(websocket)}, order REST={len(orders)}")

if errors:
    raise SystemExit("\n".join(errors))
print(f"Catalog OK: {len(TR_CATALOG)} TRs ({len(rest)} REST, {len(websocket)} WebSocket); {len(orders)} REST order TRs guarded.")
