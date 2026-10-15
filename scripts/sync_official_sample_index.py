from __future__ import annotations

import html
import json
import re
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
GUIDE_URL = "https://openapi.ls-sec.co.kr/api/apis/public/tr-guides.json?download=true"
MENU_URL = "https://openapi.ls-sec.co.kr/apiservice"
DOC_PATH = ROOT / "docs" / "official-samples.md"
INDEX_PATH = ROOT / "specs" / "official-sample-index.json"


class MenuParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.items: list[dict[str, str]] = []
        self.current: dict[str, str] | None = None
        self.span_class = ""

    def handle_starttag(self, tag, attrs) -> None:
        a = dict(attrs)
        if tag == "button" and "tr-item" in a.get("class", "").split():
            self.current = {k: v or "" for k, v in a.items()}
            self.current.update(code="", name="")
        elif tag == "span" and self.current is not None:
            self.span_class = a.get("class", "") or ""

    def handle_data(self, data: str) -> None:
        if self.current is None:
            return
        if "tr-item__code" in self.span_class:
            self.current["code"] += data.strip()
        elif "tr-item__name" in self.span_class:
            self.current["name"] += data.strip()

    def handle_endtag(self, tag: str) -> None:
        if tag == "span":
            self.span_class = ""
        elif tag == "button" and self.current is not None:
            self.items.append(self.current)
            self.current = None


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "ls-openapi-sample-index/0.1", "Referer": MENU_URL})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read()


def main() -> None:
    guide = json.loads(fetch(GUIDE_URL).decode("utf-8"))
    apis = [a for a in guide["apis"] if any("선물/옵션" in str(c) for c in a.get("categories", []))]
    transaction_map = {tx["code"]: {"name": tx.get("name", ""), "group": api.get("name", ""), "path": api.get("path", ""), "protocol": api.get("protocol", "REST"), "rate_limit_per_second": tx.get("transactionPerSec", "")} for api in apis for tx in api.get("transactions", [])}
    menu = fetch(MENU_URL).decode("utf-8")
    category = re.search(r'<div class="cat"[^>]*data-cat="선물/옵션"[^>]*data-cat-id="([^"]+)"', menu)
    if not category:
        raise RuntimeError("Domestic futures/options category is missing from the official menu")
    parser = MenuParser()
    parser.feed(menu)
    items = [i for i in parser.items if i.get("data-cat") == category.group(1)]
    records = []
    for item in items:
        code = item["code"].strip()
        if code not in transaction_map or not item.get("data-tr") or not item.get("data-api"):
            raise RuntimeError(f"Could not match official guide record: {item}")
        meta = transaction_map[code]
        official_url = MENU_URL + "?" + urlencode({"api_id": item["data-api"], "group_id": category.group(1)})
        sample_url = "https://openapi.ls-sec.co.kr/guide/api/" + item["data-tr"] + "?" + urlencode({"type": "rest", "api": item["data-api"]})
        records.append({"code": code, "name": meta["name"], "group": meta["group"], "protocol": meta["protocol"], "path": meta["path"], "rate_limit_per_second": meta["rate_limit_per_second"], "official_page": official_url, "sample_data": sample_url})
    if len(records) != len(transaction_map):
        raise RuntimeError(f"Official menu/guide mismatch: {len(records)} vs {len(transaction_map)} TRs")
    records.sort(key=lambda r: (r["group"], r["code"]))
    snapshot = {"source": MENU_URL, "guide_version": guide.get("version"), "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(), "transaction_count": len(records), "languages_on_portal": ["Python", "Java", "JavaScript"], "transactions": records}
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# 국내 선물·옵션 공식 샘플 인덱스", "", f"- 공식 API 서비스: [{MENU_URL}]({MENU_URL})", f"- 가이드 버전: `{guide.get('version')}`", f"- TR: {len(records)}개", "- 샘플 JSON 링크는 해당 TR의 Python·Java·JavaScript 코드 예제를 포함한 공식 상세 데이터를 엽니다.", "- 이 저장소는 공식 샘플 코드를 복사해 재배포하지 않고, TR별 공식 페이지 링크와 검색용 메타데이터를 제공합니다.", ""]
    for group in sorted({r["group"] for r in records}):
        lines.extend([f"## {group}", "", "| TR | 이름 | 프로토콜 | 경로 | 초당 제한 | 공식 가이드(그룹) | 샘플 JSON(TR별) |", "|---|---|---|---|---:|---|---|"])
        for r in records:
            if r["group"] == group:
                lines.append(f"| `{r['code']}` | {r['name']} | {r['protocol']} | `{r['path']}` | {r['rate_limit_per_second']} | [가이드]({r['official_page']}) | [샘플 데이터]({r['sample_data']}) |")
        lines.append("")
    lines += ["## 이용 방법", "", "샘플 JSON 링크에서 해당 TR의 `codeSamples` 안에 있는 Python, Java, JavaScript 코드를 확인하세요. 공식 가이드 링크는 해당 TR이 속한 API 그룹 페이지를 엽니다. 예제의 인증 값과 요청값을 본인 환경에 맞게 설정한 뒤, 특히 주문 API는 실계좌 주문이 발생하지 않도록 토큰과 계좌 환경을 확인해야 합니다.", "", f"> 출처: [LS증권 API 서비스]({MENU_URL}). 명세 필드 표는 [공식 명세 스냅샷](../specs/domestic-futures-options.json)을 참고하세요.", ""]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"guide_version": guide.get("version"), "transactions": len(records), "groups": len(apis), "markdown_bytes": DOC_PATH.stat().st_size, "index_bytes": INDEX_PATH.stat().st_size}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

