"""Download LS Securities' official TR guide and generate the domestic derivatives catalog."""
from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SOURCE_URL = "https://openapi.ls-sec.co.kr/api/apis/public/tr-guides.json?download=true"
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "specs" / "domestic-futures-options.json"
DEFAULT_MARKDOWN = ROOT / "docs" / "domestic-futures-options.md"


def download_guide(url: str = SOURCE_URL) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "ls-openapi-spec-sync/0.1"})
    with urllib.request.urlopen(request, timeout=60) as response:
        guide = json.loads(response.read().decode("utf-8"))
    if not isinstance(guide, dict) or not isinstance(guide.get("apis"), list):
        raise ValueError("Official guide JSON does not contain an apis array")
    return guide


def select_derivatives(guide: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        api for api in guide["apis"]
        if any("선물/옵션" in str(category) for category in api.get("categories", []))
    ]


def flatten_fields(fields: Iterable[dict[str, Any]], prefix: str = ""):
    for field in fields:
        element = str(field.get("element", ""))
        path = f"{prefix}.{element}" if prefix and element else element or prefix
        children = field.get("fields")
        if children:
            yield from flatten_fields(children, path)
        else:
            yield path, field


def field_table(title: str, blocks: list[dict[str, Any]]) -> list[str]:
    lines = [f"#### {title}", "", "| 필드 경로 | 자료형 | 길이 | 설명 |", "|---|---|---:|---|"]
    count = 0
    for block in blocks or []:
        block_name = str(block.get("element", ""))
        for path, field in flatten_fields(block.get("fields", []), block_name):
            description = str(field.get("description", "")).replace("\n", "<br>").replace("|", "\\|")
            lines.append(
                f"| `{path}` | {field.get('type', '')} | {field.get('length', '')} | {description} |"
            )
            count += 1
    if not count:
        lines.append("| 명세에 필드 없음 | | | |")
    lines.append("")
    return lines


def build_snapshot(guide: dict[str, Any], apis: list[dict[str, Any]], downloaded_at: str) -> dict[str, Any]:
    return {
        "source_url": SOURCE_URL,
        "guide_version": guide.get("version"),
        "downloaded_at_utc": downloaded_at,
        "defaults": guide.get("defaults", {}),
        "servers": guide.get("servers", []),
        "api_group_count": len(apis),
        "transaction_count": sum(len(api.get("transactions", [])) for api in apis),
        "apis": apis,
    }


def build_markdown(snapshot: dict[str, Any]) -> str:
    default_method = snapshot.get("defaults", {}).get("method", "")
    lines = [
        "# 국내 선물·옵션 API 명세", "",
        f"- 공식 가이드 버전: `{snapshot.get('guide_version')}`",
        f"- 생성 시각(UTC): `{snapshot.get('downloaded_at_utc')}`",
        f"- API 그룹: {snapshot.get('api_group_count')}개",
        f"- TR: {snapshot.get('transaction_count')}개",
        f"- 서버: `{json.dumps(snapshot.get('servers', []), ensure_ascii=False)}`",
        f"- 전역 기본값: `{json.dumps(snapshot.get('defaults', {}), ensure_ascii=False)}`",
        f"- 원본: [{SOURCE_URL}]({SOURCE_URL})", "",
        "> 공식 가이드 JSON에서 국내 `선물/옵션` 카테고리 전체를 추출했습니다. JSON 스냅샷에는 선택된 API의 전체 구조를 보존합니다.", "",
    ]
    for api in snapshot["apis"]:
        description = str(api.get("description", "")).replace("\n", " ")
        lines += [
            f"## {api.get('name', '이름 없음')}", "",
            f"- 카테고리: {', '.join(api.get('categories', []))}",
            f"- 프로토콜: {api.get('protocol', '')}",
            f"- 메서드: {api.get('method', default_method)}",
            f"- 콘텐츠 타입: {api.get('contentType', '')}",
            f"- 경로: `{api.get('path', '')}`",
            f"- 설명: {description}", "",
        ]
        for tr in api.get("transactions", []):
            lines += [
                f"### {tr.get('code', '')} — {tr.get('name', '')}", "",
                f"- 초당 호출 제한: {tr.get('transactionPerSec', '')}", "",
            ]
            request = tr.get("request", {})
            response = tr.get("response", {})
            lines += field_table("요청 헤더", request.get("headers", []))
            lines += field_table("요청 본문", request.get("body", []))
            lines += field_table("응답 헤더", response.get("headers", []))
            lines += field_table("응답 본문", response.get("body", []))
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    guide = download_guide()
    apis = select_derivatives(guide)
    downloaded_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    snapshot = build_snapshot(guide, apis, downloaded_at)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.markdown_output.write_text(build_markdown(snapshot), encoding="utf-8")
    print(
        f"Imported official guide {snapshot['guide_version']}: "
        f"{snapshot['api_group_count']} API groups, {snapshot['transaction_count']} TRs"
    )
    print(f"JSON: {args.json_output}")
    print(f"Markdown: {args.markdown_output}")


if __name__ == "__main__":
    main()
